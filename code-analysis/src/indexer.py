import json
from pathlib import Path
from file_reader import FileReader
from llm_manager import LLMManager
from config import SUMMARY_PROMPT_TEMPLATE, MAX_FILE_SIZE_BYTES, SUMMARIES_FILE


class CodeIndexer:
    def __init__(self, repo_path, llm_manager):
        self.repo_path = Path(repo_path)
        self.llm_manager = llm_manager
        self.summaries = {}
    
    def generate_summaries(self, source_files, show_progress=True):
        total = len(source_files)
        
        for idx, file_path in enumerate(source_files, 1):
            relative_path = str(file_path.relative_to(self.repo_path))
            
            if show_progress:
                print(f"\r[{idx}/{total}] Processing: {relative_path[:60]:<60}", end="", flush=True)
            
            try:
                if file_path.stat().st_size > MAX_FILE_SIZE_BYTES:
                    self.summaries[relative_path] = "[File too large to process]"
                    continue
                
                code_content = FileReader.read_source_file(file_path)
                
                if code_content is None:
                    self.summaries[relative_path] = "[Unable to read file]"
                    continue
                
                if len(code_content.strip()) == 0:
                    self.summaries[relative_path] = "[Empty file]"
                    continue
                
                truncated_code = code_content[:8000]
                prompt = SUMMARY_PROMPT_TEMPLATE.format(code=truncated_code)
                
                summary = self.llm_manager.generate(prompt, max_new_tokens=150)
                self.summaries[relative_path] = summary
                
            except Exception as e:
                self.summaries[relative_path] = f"[Error: {str(e)}]"
        
        if show_progress:
            print("\n")
        
        return self.summaries
    
    def save_summaries(self, output_path=None):
        if output_path is None:
            output_path = self.repo_path.parent / SUMMARIES_FILE
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.summaries, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    @staticmethod
    def load_summaries(summaries_path):
        with open(summaries_path, 'r', encoding='utf-8') as f:
            return json.load(f)

