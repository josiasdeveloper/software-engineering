# Design Pattern Analysis Assistant

An interactive CLI tool for analyzing design patterns in codebases using a local LLM (Large Language Model).

## Features

- Interactive chat interface for code analysis
- Specialized in identifying and explaining design patterns
- Automatic conversation summarization for context management
- Maintains conversation history with smart token management
- Analyzes code snippets, documentation, and architectural decisions

## Requirements

- Python 3.8+
- CUDA-capable GPU (required for model inference)
- ~15GB GPU memory (for DeepSeek Coder 6.7B model)

## Installation

### 1. Install in development mode

```bash
make install-dev
```

This will:
- Create a virtual environment
- Install all dependencies
- Install the package in editable mode
- Register the `chat` command

### 2. Alternative: Manual installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .
```

## Usage

### Option 1: Command Line Interface

```bash
make chat
```

Or directly:

```bash
source .venv/bin/activate
chat
```

### Option 2: Jupyter Notebook

Open `run.ipynb` and run the cells:

1. **Configuration**: Set model via environment variable
2. **Clone/Update**: Clone or pull repository
3. **Install**: Install dependencies with `pip install -e .`
4. **Chat**: Start interactive chat with `!chat`
5. **Download**: Download conversation history (auto-detects Colab)

The notebook provides a simple 5-cell interface optimized for Google Colab.

### Available Commands

Once in the chat, you can use these commands:

- `/help` - Show help message
- `/clear` - Clear conversation history (keeps model loaded)
- `/restart` - Restart model and clear all context (frees GPU memory)
- `/save` - Save conversation with auto-generated timestamp filename
- `/context` - Display current context usage (tokens, messages)
- `/exit` - Exit the assistant

### Command Examples

```bash
# Save conversation (auto-generates: conversation_20240315_143022.txt)
/save

# Check context usage
/context

# Clear history but keep model loaded
/clear

# Free GPU memory completely
/restart
```

### Notebook Usage

In `run.ipynb`:
1. Run chat and use `/save` command (can save multiple times)
2. Exit chat with `/exit`
3. Run the download cell to get ALL conversation files

Each `/save` creates a new file with timestamp. The download cell automatically finds and downloads all `conversation_*.txt` files.

**Multiple iterations supported**: Chat → Save → Exit → Chat again → Save → Download all!

### Tips for Best Results

1. **Be specific**: Reference file paths, class names, and function names
2. **Provide context**: Share relevant documentation or issue descriptions
3. **Paste code**: Include actual code snippets, not just descriptions
4. **Ask follow-ups**: The assistant maintains conversation history
5. **Monitor context**: Use `/context` to check token usage
6. **Save progress**: Use `/save` to persist important conversations

## Configuration

You can customize the model and context settings in `src/manual/config.py`:

```python
MODEL_NAME = "deepseek-ai/deepseek-coder-6.7b-instruct"  # Model to use
MAX_CONTEXT_TOKENS = 16000                                # Maximum context window
SUMMARIZE_THRESHOLD = 0.7                                 # When to summarize (70%)
MAX_HISTORY_BEFORE_SUMMARY = 10                           # Max messages before summary
```

## Architecture

```
src/manual/
├── __init__.py
├── command.py         # CLI entry point with interactive loop
├── config.py          # Configuration settings
├── llm_manager.py     # Model loading and generation (Singleton)
├── orchestrator.py    # Conversation orchestration and context management
└── summarizer.py      # Conversation summarization logic
```

## How It Works

1. **Model Loading**: DeepSeek Coder model loads once and stays in memory
2. **Context Management**: Automatically tracks token usage
3. **Smart Summarization**: When context reaches 70% or 10 messages, conversation is summarized
4. **Continuous Chat**: History is maintained, enabling multi-turn conversations

## Development

```bash
# Clean cache files
make clean

# Remove everything including venv
make clean-all

# Reinstall
make install-dev
```

## License

MIT License - See LICENSE file for details
