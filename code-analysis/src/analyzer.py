from pathlib import Path
from repository import RepositoryManager
from tree_builder import DirectoryTreeBuilder
from file_reader import FileReader
from llm_manager import LLMManager
from indexer import CodeIndexer


class PatternAnalyzer:
    def __init__(self, target_dir="./target_repo"):
        self.repo_manager = RepositoryManager(target_dir)
        self.llm_manager = LLMManager()
        self.indexer = None
        self.directory_tree = None
        self.source_files = []
        self.doc_files = {}
        self.summaries_path = None
        self.repo_path = None
    
    def phase_0_clone_and_map(self, repo_url):
        print("Cloning repository...")
        self.repo_path = self.repo_manager.clone(repo_url)
        
        print("Building directory tree...")
        tree_builder = DirectoryTreeBuilder(self.repo_path)
        self.directory_tree, self.source_files = tree_builder.build()
        
        print("Finding documentation files...")
        reader = FileReader()
        self.doc_files = reader.find_documentation_files(self.repo_path)
        
        return self.repo_path
    
    def phase_1_load_model(self):
        self.llm_manager.load_model()
    
    def phase_2_generate_summaries(self):
        if self.repo_path is None:
            raise RuntimeError("Repository not cloned. Run phase_0_clone_and_map() first.")
        
        print(f"\nGenerating summaries for {len(self.source_files)} files...")
        
        self.indexer = CodeIndexer(self.repo_path, self.llm_manager)
        self.indexer.generate_summaries(self.source_files, show_progress=True)
        
        self.summaries_path = self.indexer.save_summaries()
        
        print(f"Summaries saved to: {self.summaries_path}")
        
        return self.summaries_path
    
    def phase_3_analyze_documentation(self):
        if not self.doc_files:
            print("No documentation files found.")
            return {}
        
        print(f"\nAnalyzing {len(self.doc_files)} documentation files...")
        
        from config import DOCUMENTATION_ANALYSIS_PROMPT
        doc_patterns = {}
        
        for doc_path, doc_content in self.doc_files.items():
            print(f"Analyzing: {doc_path}")
            
            if len(doc_content.strip()) == 0:
                continue
                
            prompt = DOCUMENTATION_ANALYSIS_PROMPT.format(doc_content=doc_content[:4000])
            analysis = self.llm_manager.generate(prompt, max_new_tokens=200)
            doc_patterns[doc_path] = analysis
        
        return doc_patterns
    
    def phase_4_investigate_code(self):
        if not self.source_files:
            print("No source files found.")
            return {}
        
        print(f"\nInvestigating patterns in {len(self.source_files)} source files...")
        
        from config import PATTERN_ANALYSIS_PROMPT
        from file_reader import FileReader
        
        pattern_results = {}
        
        for idx, file_path in enumerate(self.source_files[:10], 1):  # Limit to first 10 files for testing
            relative_path = str(file_path.relative_to(self.repo_path))
            print(f"\r[{idx}/10] Analyzing: {relative_path[:50]:<50}", end="", flush=True)
            
            code_content = FileReader.read_source_file(file_path)
            if not code_content or len(code_content.strip()) == 0:
                continue
            
            # Truncate code for model context
            truncated_code = code_content[:6000]
            prompt = PATTERN_ANALYSIS_PROMPT.format(code=truncated_code)
            
            try:
                analysis = self.llm_manager.generate(prompt, max_new_tokens=300)
                pattern_results[relative_path] = analysis
            except Exception as e:
                pattern_results[relative_path] = f"Error: {str(e)}"
        
        print("\n")
        return pattern_results
    
    def phase_5_collect_evidence(self, doc_patterns, code_patterns):
        print("\nCollecting evidence and consolidating results...")
        
        from config import PATTERNS_TO_DETECT
        import json
        
        evidence = {
            "repository": "https://github.com/vanna-ai/vanna",
            "analysis_summary": {
                "total_files_analyzed": len(self.source_files),
                "documentation_files": len(self.doc_files),
                "patterns_detected": {}
            },
            "documentation_analysis": doc_patterns,
            "code_analysis": code_patterns
        }
        
        # Count pattern mentions
        pattern_count = {}
        for pattern in PATTERNS_TO_DETECT:
            count = 0
            files_with_pattern = []
            
            # Check in code analysis
            for file_path, analysis in code_patterns.items():
                if pattern.lower() in analysis.lower():
                    count += 1
                    files_with_pattern.append(file_path)
            
            # Check in documentation
            for doc_path, analysis in doc_patterns.items():
                if pattern.lower() in analysis.lower():
                    count += 1
                    files_with_pattern.append(f"doc:{doc_path}")
            
            if count > 0:
                pattern_count[pattern] = {
                    "mentions": count,
                    "files": files_with_pattern
                }
        
        evidence["analysis_summary"]["patterns_detected"] = pattern_count
        
        # Save evidence
        evidence_path = self.repo_path.parent / "pattern_evidence.json"
        with open(evidence_path, 'w', encoding='utf-8') as f:
            json.dump(evidence, f, indent=2, ensure_ascii=False)
        
        print(f"Evidence collected and saved to: {evidence_path}")
        return evidence, evidence_path
    
    def cleanup(self, keep_summaries=True):
        self.llm_manager.unload_model()
        
        if not keep_summaries and self.summaries_path and self.summaries_path.exists():
            self.summaries_path.unlink()
        
        self.repo_manager.cleanup()

