# edge-assistant

A small CLI assistant for fast research, local KB indexing, and safe file edits using the OpenAI Responses API.

Quickstart
----------

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install the project in editable mode:

```bash
pip install --upgrade pip
pip install -e .
```

3. Configure your OpenAI key (choose one option):

**Option A: Environment variable**
```bash
export OPENAI_API_KEY="sk-..."
```

**Option B: .env file (recommended)**
```bash
echo 'OPENAI_API_KEY="sk-..."' > .env
```

4. See available commands:

```bash
edge-assistant --help
```

Examples
--------

- Research the web:

```bash
edge-assistant research "state of LLM evals for code agents"
```


- Index a docs folder for local KB search:

```bash
edge-assistant kb-index ./docs
```

- Ask a quick question:

```bash
edge-assistant ask "What's new in retrieval-augmented generation?" --thread notes
```

- Safely edit a file (dry-run):

```bash
edge-assistant edit README.md "Add a concise Quickstart"
```

- Analyze an image:

```bash
edge-assistant analyze-image photo.jpg "Describe what you see in this image"
edge-assistant analyze-image document.png "Extract all text" --system "You are an OCR specialist"
```

Dev notes   
---------

- The code is split into: `cli.py` (Typer CLI), `engine.py` (Responses wrapper), `tools.py` (diffs + tool registry), and `state.py` (XDG-based state).
- Add deps to your environment: `openai`, `typer`, `rich`, `platformdirs`.

Testing helper
--------------

There is a small pytest that invokes the Typer app using a CliRunner. You can run it after installing test deps:

```bash
pip install pytest
pytest -q
```
