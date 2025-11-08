import os
from pathlib import Path
from config import SUPPORTED_EXTENSIONS, IGNORE_DIRS


class DirectoryTreeBuilder:
    def __init__(self, root_path):
        self.root_path = Path(root_path)
        self.tree_lines = []
        self.source_files = []
    
    def build(self):
        self.tree_lines = []
        self.source_files = []
        self._walk_directory(self.root_path, prefix="")
        return "\n".join(self.tree_lines), self.source_files
    
    def _walk_directory(self, path, prefix="", is_last=True):
        if path.name in IGNORE_DIRS:
            return
        
        connector = "+-- " if is_last else "|-- "
        self.tree_lines.append(f"{prefix}{connector}{path.name}/")
        
        try:
            entries = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
        except PermissionError:
            return
        
        dirs = [e for e in entries if e.is_dir() and e.name not in IGNORE_DIRS]
        files = [e for e in entries if e.is_file() and e.suffix in SUPPORTED_EXTENSIONS]
        
        extension = "    " if is_last else "|   "
        
        for i, directory in enumerate(dirs):
            is_last_dir = (i == len(dirs) - 1) and len(files) == 0
            self._walk_directory(directory, prefix + extension, is_last_dir)
        
        for i, file in enumerate(files):
            is_last_file = i == len(files) - 1
            file_connector = "+-- " if is_last_file else "|-- "
            self.tree_lines.append(f"{prefix}{extension}{file_connector}{file.name}")
            self.source_files.append(file)

