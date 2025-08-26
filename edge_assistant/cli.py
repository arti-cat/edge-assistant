#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax

from .engine import Engine
from .state import get_thread_id, set_thread_id, kb_ids, add_kb_ids
from .tools import unified, extract_between, extract_urls_from_response, function_tools

app = typer.Typer(add_completion=False)
console = Console()
eng = Engine()

# ---------- ASK ----------
@app.command("ask")
def ask(
    prompt: str = typer.Argument(..., help="Your question/instruction."),
    model: str = typer.Option(None, "--model", "-m"),
    thread: Optional[str] = typer.Option(None, "--thread", "-t", help="Thread name to maintain context."),
    stream: bool = typer.Option(False, "--stream", "-s", help="Stream tokens as they arrive"),
    system: Optional[str] = typer.Option(None, "--system", help="Optional system instructions.")
):
    prev = get_thread_id(thread)
    resp = eng.send(
        input=prompt,
        model=model,
        instructions=system,
        previous_response_id=prev,
        stream=stream
    )
    if not stream:
        console.print(Markdown(resp.output_text))
    if getattr(resp, "id", None):
        set_thread_id(resp.id, thread)

# ---------- RESEARCH (web_search) ----------
@app.command("research")
def research(
    query: str = typer.Argument(...),
    bullets: int = typer.Option(6, "--bullets", "-b"),
    model: str = typer.Option("gpt-4o", "--model", "-m"),
    as_json: bool = typer.Option(False, "--json", help="Return JSON instead of markdown"),
    stream: bool = typer.Option(False, "--stream", "-s"),
):
    schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "ResearchSummary",
            "schema": {
                "type": "object",
                "properties": {
                    "bullets": {"type": "array", "items": {"type": "string"}},
                    "sources": {"type": "array", "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "url": {"type": "string", "format": "uri"}
                        },
                        "required": ["url"],
                        "additionalProperties": False
                    }},
                    "risks_unknowns": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["bullets", "sources"],
                "additionalProperties": False
            },
            "strict": True
        }
    }

    prompt = (
        f"Summarize the latest on: {query}\n"
        f"- Output {bullets} terse bullets.\n"
        f"- Use bracketed citations inline.\n"
        f"- End with 'Risks & Unknowns'."
    )
    kwargs = dict(
        input=prompt, model=model,
        tools=[{"type": "web_search"}],
        stream=stream
    )
    if as_json:
        kwargs["response_format"] = schema

    resp = eng.send(**kwargs)
    if as_json:
        data = json.loads(resp.output_text)
        console.print_json(data=data)
    else:
        console.print(Panel.fit(Markdown(resp.output_text), title="Summary"))
        urls = extract_urls_from_response(resp)
        if urls:
            console.print("\n[bold]Sources[/bold]")
            for i, (title, url) in enumerate(urls, 1):
                console.print(f"{i}. {(title + ' — ') if title else ''}{url}")

# ---------- KB INDEX / KB RESEARCH (file_search) ----------
@app.command("kb-index")
def kb_index(folder: Path = typer.Argument(..., exists=True, file_okay=False)):
    count = 0
    ids = []
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".txt", ".pdf", ".py", ".rst"}:
            fid = eng.upload_for_kb(p)
            ids.append(fid); count += 1
    add_kb_ids(ids)
    console.print(f"[green]Indexed {count} files ({len(ids)} new).[/green]")

@app.command("kb-research")
def kb_research(
    query: str = typer.Argument(...),
    model: str = typer.Option("gpt-4o", "--model", "-m"),
    stream: bool = typer.Option(False, "--stream", "-s"),
):
    files = kb_ids()
    if not files:
        raise typer.Exit("No KB files. Run: edge-assistant kb-index ./docs")

    resp = eng.send(
        model=model,
        input=f"Answer using the provided knowledge files. Cite sources clearly. Q: {query}",
        tools=[{"type": "file_search"}],
        attachments=[{"file_id": fid, "tools": [{"type":"file_search"}]} for fid in files],
        stream=stream,
    )
    if not stream:
        console.print(Markdown(resp.output_text))

# ---------- EDIT ----------
@app.command("edit")
def edit(
    path: Path = typer.Argument(..., exists=True, dir_okay=False, resolve_path=True),
    instruction: str = typer.Argument(..., help="Describe the change you want."),
    model: str = typer.Option("gpt-4o-mini", "--model", "-m"),
    apply: bool = typer.Option(False, "--apply", help="Write changes to disk"),
    backup: bool = typer.Option(True, "--backup/--no-backup"),
):
    original = path.read_text(encoding="utf-8")
    sys_prompt = (
        "You are a precise editor. Produce the FULL new file content only.\n"
        "Wrap it strictly between <BEGIN_FILE> and <END_FILE>."
    )
    user_prompt = (
        f"File: {path.name}\nInstruction: {instruction}\n\n"
        f"--- ORIGINAL START ---\n{original}\n--- ORIGINAL END ---"
    )
    resp = eng.send(
        model=model,
        instructions=sys_prompt,
        input=user_prompt,
    )
    text = resp.output_text
    new_content = extract_between(text, "<BEGIN_FILE>", "<END_FILE>") or text.strip()
    diff = unified(original, new_content, str(path))

    if not diff:
        console.print("[green]No changes proposed.[/green]")
        return

    console.print(Syntax(diff, "diff", theme="ansi_dark", word_wrap=True))
    if apply:
        if backup:
            bak = path.with_suffix(path.suffix + ".bak")
            bak.write_text(original, encoding="utf-8")
            console.print(f"[dim]Backup -> {bak}[/dim]")
        path.write_text(new_content, encoding="utf-8")
        console.print("[bold green]Applied.[/bold green]")
    else:
        console.print("[yellow]Dry run. Use --apply to write changes.[/yellow]")

# ---------- AGENT (optional tool calls with guardrails) ----------
@app.command("agent")
def agent(task: str, approve: bool = typer.Option(False, "--approve")):
    resp = eng.send(
        model="gpt-4o-mini",
        instructions="You may call tools to modify files. Prefer minimal diffs and safe paths.",
        input=task,
        tools=function_tools(),
    )
    acted = False
    for item in getattr(resp, "output", []) or []:
        if getattr(item, "type", None) == "function_call" and item.name == "fs_write":
            args = json.loads(item.arguments)
            p = Path(args["path"]).expanduser().resolve()
            before = p.read_text(encoding="utf-8") if p.exists() else ""
            diff = unified(before, args["content"], str(p))
            console.print(Syntax(diff, "diff", theme="ansi_dark"))
            if approve:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(args["content"], encoding="utf-8")
                console.print(f"[green]Wrote {p}[/green]")
            else:
                console.print("[yellow]Dry run. Re-run with --approve to apply.[/yellow]")
            acted = True
    if not acted:
        console.print(Markdown(getattr(resp, "output_text", "")))

# ---------- IMAGE ANALYSIS ----------
@app.command("analyze-image")
def analyze_image(
    image_path: Path = typer.Argument(..., exists=True, dir_okay=False, resolve_path=True),
    prompt: str = typer.Argument(..., help="Description of what you want to analyze in the image."),
    system: Optional[str] = typer.Option(None, "--system", "-s", help="System/developer prompt for analysis context."),
    model: str = typer.Option("gpt-4o", "--model", "-m", help="Vision model to use.")
):
    """Analyze an image using GPT-4 Vision with custom prompts."""
    try:
        result = eng.analyze_image(
            image_path=str(image_path),
            user_prompt=prompt,
            system_prompt=system,
            model=model
        )
        console.print(Markdown(result))
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error analyzing image: {e}[/red]")
        raise typer.Exit(1)

def main():
    app()

if __name__ == "__main__":
    main()
