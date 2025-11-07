SUPPORTED_EXTENSIONS = {'.py', '.java', '.js', '.ts', '.cpp', '.c', '.h', '.cs', '.go', '.rb'}

IGNORE_DIRS = {
    '__pycache__', 
    'node_modules', 
    '.git', 
    'venv', 
    'env', 
    '.venv',
    'dist',
    'build',
    '.pytest_cache',
    '.mypy_cache',
    'target'
}

MODEL_NAME = "deepseek-ai/deepseek-coder-6.7b-instruct"
MAX_CONTEXT_TOKENS = 16000
MAX_FILE_SIZE_BYTES = 100000
SUMMARIES_FILE = "summaries.json"

SUMMARY_PROMPT_TEMPLATE = """You are a code analysis assistant. Summarize the following code file in 3 sentences.
Focus on: main classes/functions, their responsibilities, and key inheritance/dependencies.

Code:
{code}

Summary:"""

