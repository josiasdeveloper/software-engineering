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
        pass
    
    def phase_4_investigate_code(self):
        pass
    
    def phase_5_collect_evidence(self):
        pass
    
    def cleanup(self, keep_summaries=True):
        self.llm_manager.unload_model()
        
        if not keep_summaries and self.summaries_path and self.summaries_path.exists():
            self.summaries_path.unlink()
        
        self.repo_manager.cleanup()

