#!/usr/bin/env python3
from __future__ import annotations
import os, re, json, difflib, datetime
from pathlib import Path
from typing import Iterable, List, Tuple, Optional, Any, Dict

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax

from openai import OpenAI

app = typer.Typer(add_completion=False)
console = Console()
STATE_PATH = Path.home() / ".edge_assistant_state.json"

# --- Core ---------------------------------------------------------------

def client() -> OpenAI:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise SystemExit("OPENAI_API_KEY not set")
    return OpenAI(api_key=key)

def load_state() -> Dict[str, Any]:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            return {}
    return {}

def save_state(data: Dict[str, Any]) -> None:
    STATE_PATH.write_text(json.dumps(data, indent=2))

def nowstamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# --- Utilities ----------------------------------------------------------

def unified(a: str, b: str, path: str) -> str:
    diff = difflib.unified_diff(
        a.splitlines(True),
        b.splitlines(True),
        fromfile=f"{path} (original)",
        tofile=f"{path} (proposed)",
        lineterm=""
    )
    return "".join(diff)

def extract_between_tags(text: str, start_tag: str, end_tag: str) -> Optional[str]:
    m = re.search(re.escape(start_tag) + r"(.*?)" + re.escape(end_tag),
                  text, flags=re.DOTALL)
    return m.group(1) if m else None

def dedupe(seq: Iterable[str]) -> List[str]:
    seen = set(); out = []
    for x in seq:
        if x not in seen:
            seen.add(x); out.append(x)
    return out

def extract_urls_from_response(resp: Any) -> List[Tuple[str, str]]:
    """
    Pull url citations from Responses API output if present.
    Falls back to regex from text.
    """
    urls: List[Tuple[str, str]] = []

    # 1) Try structured annotations (Cookbook shows content[].annotations[].type=='url_citation')
    try:
        outputs = getattr(resp, "output", []) or []
        for item in outputs:
            content = getattr(item, "content", []) or []
            for c in content:
                anns = c.get("annotations") if isinstance(c, dict) else getattr(c, "annotations", None)
                if not anns: continue
                for a in anns:
                    atype = a.get("type") if isinstance(a, dict) else getattr(a, "type", "")
                    if atype == "url_citation":
                        title = a.get("title") if isinstance(a, dict) else getattr(a, "title", "")
                        url   = a.get("url") if isinstance(a, dict) else getattr(a, "url", "")
                        if url:
                            urls.append((title or "", url))
    except Exception:
        pass

    # 2) Fallback: scrape URLs from text
    text = getattr(resp, "output_text", "") or ""
    for u in re.findall(r"https?://\S+", text):
        urls.append(("", u.rstrip(").,]")))

    # Dedup by URL
    seen = set(); out: List[Tuple[str,str]] = []
    for title, u in urls:
        if u not in seen:
            seen.add(u); out.append((title, u))
    return out

# --- Commands -----------------------------------------------------------

@app.command("ask")
def ask(
    prompt: str = typer.Argument(..., help="Your question / instruction."),
    model: str = typer.Option("gpt-4o-mini", "--model", "-m"),
    continue_thread: bool = typer.Option(False, "--continue", "-c", help="Continue from last response in state."),
    system: Optional[str] = typer.Option(None, "--system", help="Optional system instructions."),
):
    """
    General Q/A (no tools). Optionally continue the last thread.
    """
    st = load_state()
    prev_id = st.get("last_response_id") if continue_thread else None

    kwargs = dict(model=model, input=prompt)
    if system:
        kwargs["instructions"] = system
    if prev_id:
        kwargs["previous_response_id"] = prev_id

    resp = client().responses.create(**kwargs)

    console.print(Markdown(resp.output_text))
    st["last_response_id"] = resp.id
    save_state(st)

@app.command("research")
def research(
    query: str = typer.Argument(..., help="Research query"),
    model: str = typer.Option("gpt-4o", "--model", "-m"),
    bullets: int = typer.Option(7, "--bullets", "-b", help="Target bullet count"),
    region: Optional[str] = typer.Option(None, "--region", help="Optional region hint in prompt"),
):
    """
    Quick web-backed research with citations (hosted web_search).
    """
    prompt = (
        f"Summarize the latest on: {query}\n"
        f"- Output {bullets} tight bullets.\n"
        f"- Include inline bracketed citations where appropriate.\n"
        f"- End with a short 'Risks & Unknowns' section.\n"
        + (f"- Assume region={region} if relevant.\n" if region else "")
    )

    resp = client().responses.create(
        model=model,
        input=prompt,
        tools=[{"type": "web_search"}],  # hosted tool
    )

    console.print(Panel.fit(Markdown(resp.output_text), title="Summary"))

    urls = extract_urls_from_response(resp)
    if urls:
        console.print("\n[bold]Sources[/bold]")
        for i, (title, url) in enumerate(urls, 1):
            label = f"{i}. {title} — {url}" if title else f"{i}. {url}"
            console.print(label)

@app.command("edit")
def edit(
    path: Path = typer.Argument(..., exists=True, dir_okay=False, resolve_path=True),
    instruction: str = typer.Argument(..., help="Describe the change you want."),
    model: str = typer.Option("gpt-4o-mini", "--model", "-m"),
    apply: bool = typer.Option(False, "--apply", help="Write changes to disk (default: dry-run)"),
    backup: bool = typer.Option(True, "--backup/--no-backup", help="Save .bak before writing"),
):
    """
    Edit a file safely: model returns full new content; we show a diff, then optional apply.
    """
    original = path.read_text(encoding="utf-8")
    sys_prompt = (
        "You are a precise editor. Produce the full, final file content for the given file.\n"
        "Rules:\n"
        "1) Return ONLY the new file content wrapped exactly between:\n"
        "<BEGIN_FILE>\n"
        "(content)\n"
        "<END_FILE>\n"
        "2) Keep formatting stable. If no change is needed, return the original content."
    )
    user_prompt = (
        f"File: {path.name}\n"
        f"Instruction: {instruction}\n\n"
        f"--- ORIGINAL START ---\n{original}\n--- ORIGINAL END ---"
    )

    resp = client().responses.create(
        model=model,
        instructions=sys_prompt,
        input=user_prompt,
    )

    text = resp.output_text
    new_content = extract_between_tags(text, "<BEGIN_FILE>", "<END_FILE>") or text.strip()
    diff = unified(original, new_content, str(path))

    if not diff:
        console.print("[green]No changes proposed.[/green]")
        return

    # show diff with syntax highlight
    console.print(Syntax(diff, "diff", theme="ansi_dark", word_wrap=True))

    if apply:
        if backup:
            bak = path.with_suffix(path.suffix + f".{nowstamp()}.bak")
            bak.write_text(original, encoding="utf-8")
            console.print(f"[dim]Backup -> {bak}[/dim]")
        path.write_text(new_content, encoding="utf-8")
        console.print("[bold green]Applied.[/bold green]")
    else:
        console.print("[yellow]Dry run. Use --apply to write changes.[/yellow]")

if __name__ == "__main__":
    app()
