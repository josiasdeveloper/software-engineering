import subprocess
import os
import shutil
from pathlib import Path


class RepositoryManager:
    def __init__(self, target_dir="./target_repo"):
        self.target_dir = Path(target_dir)
    
    def clone(self, repo_url):
        if self.target_dir.exists():
            self._force_remove_directory(self.target_dir)
        
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, str(self.target_dir)],
            check=True,
            capture_output=True
        )
        
        return self.target_dir
    
    def cleanup(self):
        if self.target_dir.exists():
            self._force_remove_directory(self.target_dir)
    
    def _force_remove_directory(self, path):
        """Force remove directory on Windows with read-only files"""
        import stat
        
        def handle_remove_readonly(func, path, exc):
            if os.path.exists(path):
                os.chmod(path, stat.S_IWRITE)
                func(path)
        
        shutil.rmtree(path, onerror=handle_remove_readonly)

