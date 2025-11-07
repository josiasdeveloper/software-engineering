# Code Analysis - Design Pattern Detection

Automated detection of design patterns in codebases using Large Language Models.

## Overview

This tool analyzes a given repository and identifies implementation of software design patterns (Gang of Four patterns) using a pre-trained LLM. It runs in Google Colab to leverage free GPU acceleration.

## How It Works

The analysis runs in three phases:

1. **Phase 1: Directory Tree** - Maps the codebase structure and identifies source files
2. **Phase 2: File Summaries** - Uses LLM to generate brief descriptions of each file
3. **Phase 3: Pattern Analysis** - Combines all context to detect design patterns

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/code-analysis.git
cd code-analysis

# Install in editable mode
pip install -e .
```

## Usage in Google Colab

### Option 1: Using the Notebook (Recommended)

1. Go to [Google Colab](https://colab.research.google.com/)
2. File → Upload notebook → Select `colab_analysis.ipynb`
3. Runtime → Change runtime type → **T4 GPU**
4. Run all cells

### Option 2: Manual Setup

```python
# Step 1: Check GPU
!nvidia-smi

# Step 2: Clone this repository
!git clone https://github.com/your-username/code-analysis.git
%cd code-analysis

# Step 3: Install the package
!pip install -e . -q

# Step 4: Run analysis (replace URL with your target repo)
!analyze analyze https://github.com/vanna-ai/vanna.git --keep-summaries

# Step 5: View results
import json
with open('summaries.json', 'r') as f:
    summaries = json.load(f)
    
print(f"Total files: {len(summaries)}")
for path, summary in list(summaries.items())[:3]:
    print(f"{path}: {summary}")

# Step 6: Download results
from google.colab import files
files.download('summaries.json')
```

### Important: GPU Setup

**You MUST enable GPU in Colab:**
- Click "Runtime" → "Change runtime type"
- Select "T4 GPU" as Hardware accelerator
- Click "Save"

## Local Usage

```bash
# Install the package
make install

# Analyze a repository
make analyze URL=https://github.com/pallets/flask.git

# Generate tree for local directory
make tree DIR=./my-project

# Run test analysis
make test

# Clean up
make clean
```

### CLI Commands

```bash
# Full analysis
analyze analyze <repository-url>

# Keep repository after analysis
analyze analyze --keep-repo <repository-url>

# Generate tree only
analyze tree <local-directory>

# Show help
analyze --help
```

## Supported Languages

- Python (.py)
- Java (.java)
- JavaScript (.js)
- TypeScript (.ts)
- C/C++ (.c, .cpp, .h)
- C# (.cs)
- Go (.go)
- Ruby (.rb)

## Requirements

- Python 3.12+
- GPU recommended (Google Colab T4 or better)
- Internet connection for model download

## Limitations

The analysis focuses on patterns detectable within single files or clear file interactions. Complex multi-file patterns may be harder to detect depending on the model's context window.

