import os

MODEL_NAME = os.getenv("LLM_MODEL", "deepseek-ai/deepseek-coder-6.7b-instruct")
MAX_CONTEXT_TOKENS = 16000
MAX_FILE_SIZE_BYTES = 100000

# Chat configuration
SUMMARIZE_THRESHOLD = 0.7  # Summarize when 70% of context is used
MAX_HISTORY_BEFORE_SUMMARY = 10  # Max messages before forcing summarization
RESERVED_TOKENS_FOR_RESPONSE = 512  # Tokens reserved for model response
