# Google Colab Setup Guide

## Prerequisites

You need a Google account to use Google Colab. No installation required!

## Step-by-Step Setup

### 1. Enable GPU

**CRITICAL**: The analysis requires GPU to run efficiently.

1. Open [Google Colab](https://colab.research.google.com/)
2. Click **Runtime** → **Change runtime type**
3. Select **T4 GPU** from Hardware accelerator dropdown
4. Click **Save**

### 2. Upload the Notebook (Easiest Method)

1. Download `colab_analysis.ipynb` from this repository
2. In Colab: **File** → **Upload notebook**
3. Select the downloaded notebook
4. Click **Run all** (Ctrl+F9 or Cmd+F9)

### 3. Manual Setup (Alternative)

If you prefer to work directly in a new notebook:

```python
# Cell 1: Check GPU
!nvidia-smi

# Cell 2: Clone the analyzer
!git clone https://github.com/your-username/code-analysis.git
%cd code-analysis

# Cell 3: Install dependencies
!pip install -e . -q

# Cell 4: Run analysis
!analyze analyze https://github.com/user/repo.git --keep-summaries

# Cell 5: View results
import json
with open('summaries.json', 'r') as f:
    summaries = json.load(f)
print(f"Analyzed {len(summaries)} files")

# Cell 6: Download results
from google.colab import files
files.download('summaries.json')
```

## Common Issues

### "No GPU available"
- Make sure you selected T4 GPU in Runtime settings
- Restart the runtime: Runtime → Restart runtime

### "Out of memory"
- The DeepSeek model requires ~15GB VRAM
- T4 GPU has 16GB, should be enough
- If it fails, try a smaller repository first

### "Installation failed"
- Check internet connection
- Try restarting runtime
- Ensure all dependencies are compatible

## Performance Tips

1. **Use `--skip-summaries` for testing**: Test the structure first without running the model
   ```python
   !analyze analyze <repo-url> --skip-summaries
   ```

2. **Start with small repositories**: Test with repos that have <100 files

3. **Monitor GPU usage**: Keep the nvidia-smi cell visible to monitor memory

## Expected Runtime

- **Small repo** (50-100 files): ~5-10 minutes
- **Medium repo** (100-300 files): ~15-30 minutes  
- **Large repo** (300+ files): ~30-60 minutes

Each file takes ~2-5 seconds to summarize.

## Saving Results

The `summaries.json` file is automatically saved. Download it with:

```python
from google.colab import files
files.download('summaries.json')
```

You can also mount Google Drive to save automatically:

```python
from google.colab import drive
drive.mount('/content/drive')

# Results will be saved to your Google Drive
!cp summaries.json /content/drive/MyDrive/
```

