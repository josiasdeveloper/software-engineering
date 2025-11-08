import os

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

MODEL_NAME = os.getenv("LLM_MODEL", "microsoft/phi-2")  
MAX_CONTEXT_TOKENS = 1024
MAX_FILE_SIZE_BYTES = 50000  
SUMMARIES_FILE = "summaries.json"

SUMMARY_PROMPT_TEMPLATE = """You are a code analysis assistant. Summarize the following code file in 3 sentences.
Focus on: main classes/functions, their responsibilities, and key inheritance/dependencies.

Code:
{code}

Summary:"""

PATTERN_ANALYSIS_PROMPT = """Analyze this Python code for design patterns:

CODE:
{code}

Look for these patterns:
- Singleton (static instance, private constructor)
- Factory (object creation methods)  
- Builder (step-by-step construction)
- Adapter (interface conversion)
- Decorator (dynamic functionality)
- Observer (publish-subscribe)
- Strategy (interchangeable algorithms)
- MVC (Model-View-Controller)

Respond with specific patterns found and evidence from the code.
If no patterns, say "No clear patterns identified".

ANALYSIS:"""

DOCUMENTATION_ANALYSIS_PROMPT = """Analyze this documentation for software architecture patterns and design decisions.

Documentation:
{doc_content}

Extract:
- Architecture patterns mentioned
- Design decisions explained
- Framework or technology choices
- Code organization principles"""

SUMMARY_PROMPT_TEMPLATE = """Summarize this code file focusing on:
- Main classes/functions and their purposes
- Key relationships and dependencies
- Overall architecture role
- Notable design patterns if visible

Code:
{code}

Concise summary:"""

PATTERNS_TO_DETECT = [
    'Singleton', 'Factory', 'Builder', 'Abstract Factory',
    'Adapter', 'Decorator', 'Facade', 'Proxy', 'Composite',
    'Observer', 'Strategy', 'Command', 'Template Method', 'State',
    'MVC', 'Repository', 'Dependency Injection', 'Service Layer'
]