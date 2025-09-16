# Edge Assistant CLI Guide for Beginners

A complete walkthrough for getting productive with edge-assistant - your AI-powered research and analysis companion.

## Quick Start (5 minutes)

### Step 1: Install and Setup

1. **Create a virtual environment** (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. **Install edge-assistant**:
```bash
pip install --upgrade pip
pip install -e .
```

3. **Set up your OpenAI API key** (.env file method recommended):
```bash
echo 'OPENAI_API_KEY="sk-your-actual-key-here"' > .env
```

### Step 2: Verify Your Setup

Test that everything works with a simple question:

```bash
edge-assistant ask "What is artificial intelligence?"
```

**Expected output**: You should see a formatted response explaining AI concepts.

If you see an error about API keys, double-check that your `.env` file is in the same directory and contains your valid OpenAI API key.

### Step 3: Your First Real Analysis

Try analyzing a file in your current directory:

```bash
edge-assistant analyze "Summarize the key points" --file README.md
```

**Success!** You're now ready to explore edge-assistant's powerful features.

## Installation & Setup

### Prerequisites

- **Python 3.10 or higher** - Check with `python3 --version`
- **OpenAI API key** - Get one from [platform.openai.com](https://platform.openai.com)
- **Terminal access** - Command line interface

### Complete Installation Process

1. **Clone or download** the edge-assistant project to your computer

2. **Navigate to the project directory**:
```bash
cd edge-assistant
```

3. **Create virtual environment** (isolates dependencies):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. **Install the package**:
```bash
pip install --upgrade pip
pip install -e .
```

### API Key Configuration

**Option A: .env file (Recommended)**
```bash
# Create .env file in the project directory
echo 'OPENAI_API_KEY="sk-your-actual-key-here"' > .env
```

**Option B: Environment variable**
```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export OPENAI_API_KEY="sk-your-actual-key-here"
```

### Validation

Confirm everything is working:

```bash
# Check the tool is installed
edge-assistant --help

# Test with a simple question
edge-assistant ask "Hello, are you working?"

# Verify file analysis
edge-assistant analyze "What type of file is this?" --file README.md
```

## Core Concepts

### Understanding Threading

**Threads** maintain conversation context across multiple interactions:

- **Fresh context** (default): Each command is independent
- **Threaded conversation**: Use `--thread name` to maintain context
- **Mixed content**: Same thread works with text, images, and documents

### Content Types

Edge-assistant automatically detects and handles:

- **Text**: Plain questions and conversations
- **Images**: JPEG, PNG, GIF, WebP files
- **Documents**: PDF, TXT, MD, Python files
- **Web searches**: Built-in research capabilities

### Safety Features

- **Dry-run by default**: File edits show preview before applying
- **Approval workflows**: Agent mode requires `--approve` for file writes
- **Backup creation**: Automatic backups when editing files

## Basic Commands

Start with these essential commands to build confidence:

### 1. Ask Questions (`ask`)

Simple text conversations:

```bash
# Basic question
edge-assistant ask "Explain quantum computing in simple terms"

# With conversation threading
edge-assistant ask "What is machine learning?" --thread learning
edge-assistant ask "How does it relate to AI?" --thread learning

# With custom instructions
edge-assistant ask "Review this code architecture" --system "You are a senior software architect"
```

### 2. Analyze Content (`analyze`)

The most powerful command - works with any content type:

```bash
# Text-only analysis
edge-assistant analyze "What are the benefits of renewable energy?"

# Image analysis
edge-assistant analyze "What safety issues do you see?" --file safety-inspection.jpg

# Document analysis
edge-assistant analyze "Summarize the main findings" --file research-paper.pdf

# Mixed conversation (images + documents in same thread)
edge-assistant analyze "Analyze this chart" --file chart.png --thread project
edge-assistant analyze "How does this report relate to the chart?" --file report.pdf --thread project
```

### 3. Web Research (`research`)

Get current information with citations:

```bash
# Basic research
edge-assistant research "latest developments in AI safety 2024"

# Structured output
edge-assistant research "best practices for remote work" --json

# Custom depth
edge-assistant research "climate change solutions" --bullets 10
```

### Practical Examples

**Document Workflow**:
```bash
# Start with overview
edge-assistant analyze "What is this document about?" --file contract.pdf --thread review

# Ask specific questions
edge-assistant analyze "What are the key terms and conditions?" --thread review

# Get summary
edge-assistant analyze "Summarize our discussion and highlight important points" --thread review
```

**Image Analysis Workflow**:
```bash
# Initial analysis
edge-assistant analyze "Describe what you see in detail" --file photo.jpg --thread inspection

# Follow-up questions
edge-assistant analyze "Are there any safety concerns visible?" --thread inspection

# Expert perspective
edge-assistant analyze "What would an engineer notice?" --thread inspection --system "You are a professional engineer"
```

## Intermediate Workflows

### Knowledge Base Management

Build and search your personal knowledge base:

**Step 1: Index your documents**
```bash
# Index a folder of documents
edge-assistant kb-index ./documents

# Index multiple folders
edge-assistant kb-index ./papers ./notes ./manuals
```

**Step 2: Check what's indexed**
```bash
edge-assistant kb-list
```

**Step 3: Search your knowledge base**
```bash
# Ask questions about your indexed content
edge-assistant kb-research "How do transformers work in natural language processing?"

# Get technical details
edge-assistant kb-research "What are the implementation details for attention mechanisms?"
```

### Thread Management

Organize your work with meaningful thread names:

```bash
# Project-specific threads
edge-assistant analyze "Review architecture" --file diagram.png --thread project-alpha
edge-assistant analyze "Check the code quality" --file main.py --thread project-alpha

# Topic-based learning
edge-assistant ask "Explain neural networks" --thread ml-learning
edge-assistant ask "What about convolutional networks?" --thread ml-learning

# Research sessions
edge-assistant research "quantum computing trends" --thread quantum-research
edge-assistant analyze "How does this paper relate?" --file quantum-paper.pdf --thread quantum-research
```

**Thread Management Commands**:
```bash
# Clear a thread to start fresh
edge-assistant analyze --clear-thread --thread project-alpha

# Set custom interaction limits
edge-assistant analyze "Complex analysis" --file data.csv --thread analysis --max-interactions 50
```

### Content Type Control

Override automatic detection when needed:

```bash
# Force image analysis on a PDF
edge-assistant analyze "Analyze as an image" --file diagram.pdf --type image

# Treat screenshot as document for text extraction
edge-assistant analyze "Extract all text" --file screenshot.png --type file

# Pure text analysis (no file)
edge-assistant analyze "Theoretical question about AI safety" --type text
```

## Advanced Features

### Safe File Editing

Preview changes before applying them:

```bash
# Preview changes (safe, dry-run by default)
edge-assistant edit README.md "Add a troubleshooting section"

# Review the diff, then apply if satisfied
edge-assistant edit README.md "Add a troubleshooting section" --apply

# Skip backup creation
edge-assistant edit config.py "Update the API endpoint" --apply --no-backup
```

### Agent Mode

AI assistant with file system access:

```bash
# Code generation (preview mode)
edge-assistant agent "Create a Python script that processes CSV files and generates plots"

# Apply with approval
edge-assistant agent "Create a data visualization dashboard" --approve

# System administration tasks
edge-assistant agent "Analyze log files and suggest optimizations" --approve
```

### Advanced Analysis Options

**Model Selection**:
```bash
# Use specific models for different tasks
edge-assistant analyze "Quick question" --file simple.txt --model gpt-4o-mini
edge-assistant analyze "Complex analysis" --file research.pdf --model gpt-4o
```

**Output Management**:
```bash
# Save analysis to file
edge-assistant analyze "Convert to markdown" --file document.pdf --save report.md

# Auto-generate filename
edge-assistant analyze "Summarize" --file data.csv --save auto
```

**System Instructions**:
```bash
# Role-specific analysis
edge-assistant analyze "Review for security issues" --file code.py --system "You are a cybersecurity expert"

# Domain expertise
edge-assistant analyze "Assess financial risks" --file report.pdf --system "You are a financial analyst"
```

## Troubleshooting

### Common Issues and Solutions

**Problem**: "API key not found" error
**Solution**:
1. Check your `.env` file exists and contains `OPENAI_API_KEY="sk-..."`
2. Verify the file is in the same directory where you run commands
3. Ensure no extra spaces or quotes in the key

**Problem**: "File not found" error
**Solution**:
1. Use absolute paths: `/home/user/documents/file.pdf`
2. Check file exists: `ls -la /path/to/file`
3. Verify permissions: ensure you can read the file

**Problem**: Thread context seems lost
**Solution**:
1. Use consistent thread names (case-sensitive)
2. Check thread status with any threaded command
3. Clear and restart thread if needed: `--clear-thread`

**Problem**: Commands hang or timeout
**Solution**:
1. Check internet connection for web research
2. Verify OpenAI API key has sufficient credits
3. Try with smaller files or simpler prompts

**Problem**: Unexpected output format
**Solution**:
1. Specify content type explicitly: `--type image` or `--type file`
2. Use system instructions to guide output format
3. Try different models for better results

### Error Messages Guide

**"No KB files found"**
- Run `edge-assistant kb-index ./your-documents` first
- Check that your folder contains supported files (.md, .txt, .pdf, .py, .rst)

**"Thread has reached max interactions"**
- Use `--clear-thread` to reset the thread
- Or set higher limit: `--max-interactions 50`

**"Invalid content type"**
- Check file extension is supported
- Try `--type auto` to let the system detect
- Ensure file is not corrupted

### Getting Help

```bash
# General help
edge-assistant --help

# Command-specific help
edge-assistant analyze --help
edge-assistant ask --help
edge-assistant research --help

# Check version
edge-assistant --version
```

## Best Practices

### Organizing Your Work

**1. Use meaningful thread names**:
```bash
# Good
edge-assistant analyze "Review design" --file ui-mockup.png --thread website-redesign

# Poor
edge-assistant analyze "Review design" --file ui-mockup.png --thread thread1
```

**2. Structure knowledge base thoughtfully**:
```bash
# Organize by topic
mkdir research-papers tutorials manuals
edge-assistant kb-index ./research-papers ./tutorials ./manuals
```

**3. Start with simple questions, build complexity**:
```bash
# Start broad
edge-assistant analyze "What is this document about?" --file report.pdf --thread review

# Get specific
edge-assistant analyze "What are the financial implications mentioned?" --thread review
```

### Effective Prompting

**1. Be specific about what you want**:
```bash
# Good
edge-assistant analyze "List all safety violations visible in this facility photo" --file facility.jpg

# Less effective
edge-assistant analyze "Look at this" --file facility.jpg
```

**2. Use system instructions for expertise**:
```bash
edge-assistant analyze "Review this code for security vulnerabilities" --file app.py --system "You are a cybersecurity expert"
```

**3. Leverage threading for complex analysis**:
```bash
# Build context progressively
edge-assistant analyze "Analyze the data trends" --file data.csv --thread analysis
edge-assistant analyze "What factors might explain these trends?" --thread analysis
edge-assistant analyze "What are the business implications?" --thread analysis
```

### File Management

**1. Use absolute paths for reliability**:
```bash
# Reliable
edge-assistant analyze "Summarize" --file /home/user/documents/report.pdf

# May fail depending on current directory
edge-assistant analyze "Summarize" --file ../documents/report.pdf
```

**2. Keep files organized**:
```bash
# Good structure
/home/user/projects/
├── documents/
├── images/
├── data/
└── outputs/
```

**3. Backup important files before editing**:
```bash
# Default behavior includes backup
edge-assistant edit important.py "Add error handling" --apply
# Creates important.py.bak automatically
```

### Performance Tips

**1. Choose appropriate models**:
- Use `gpt-4o-mini` for simple tasks and quick responses
- Use `gpt-4o` for complex analysis and high-quality output

**2. Manage thread length**:
- Clear threads when switching topics: `--clear-thread`
- Use descriptive thread names to track conversations

**3. Optimize file sizes**:
- Compress large images when possible
- Use PDF for text-heavy documents
- Break very large files into sections

### Security Considerations

**1. Protect sensitive information**:
- Review files before analysis to ensure no sensitive data
- Use local environment variables for API keys
- Be cautious with `agent` mode on sensitive systems

**2. Validate AI suggestions**:
- Always review generated code before execution
- Use dry-run mode for file edits first
- Verify research results with additional sources

**3. Manage access**:
- Keep API keys secure and don't share them
- Use appropriate file permissions
- Regular cleanup of temporary files and threads

---

## Quick Reference

### Essential Commands
```bash
# Basic interaction
edge-assistant ask "question"

# File analysis
edge-assistant analyze "prompt" --file path/to/file

# Research
edge-assistant research "topic"

# Knowledge base
edge-assistant kb-index ./documents
edge-assistant kb-research "query"

# Safe editing
edge-assistant edit file.txt "instruction" --apply
```

### Common Options
- `--thread name`: Maintain conversation context
- `--system "prompt"`: Add expert instructions
- `--model gpt-4o`: Choose specific model
- `--save filename`: Save output to file
- `--apply`: Apply file changes (editing)
- `--approve`: Allow file writes (agent mode)

### File Paths
- Use absolute paths for reliability: `/home/user/file.pdf`
- Supported formats: .md, .txt, .pdf, .py, .rst, .jpg, .png, .gif, .webp

### Thread Management
- `--clear-thread`: Reset conversation context
- `--max-interactions N`: Set conversation limits
- Thread names are case-sensitive

---

**Need more help?** Run `edge-assistant --help` or `edge-assistant [command] --help` for detailed command information.