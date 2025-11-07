import subprocess
import os
import shutil
from pathlib import Path


class RepositoryManager:
    def __init__(self, target_dir="./target_repo"):
        self.target_dir = Path(target_dir)
    
    def clone(self, repo_url):
        if self.target_dir.exists():
            shutil.rmtree(self.target_dir)
        
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, str(self.target_dir)],
            check=True,
            capture_output=True
        )
        
        return self.target_dir
    
    def cleanup(self):
        if self.target_dir.exists():
            shutil.rmtree(self.target_dir)

