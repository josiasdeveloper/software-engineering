from pathlib import Path


class FileReader:
    @staticmethod
    def read_source_file(file_path: Path) -> str:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            return f"Erro ao ler arquivo: {str(e)}"
    
    @staticmethod
    def find_documentation_files(root_path):
        root = Path(root_path)
        doc_files = {}
        
        for pattern in ['README.md', 'README.rst', 'ARCHITECTURE.md', 'DESIGN.md']:
            matches = list(root.rglob(pattern))
            for match in matches:
                try:
                    with open(match, 'r', encoding='utf-8') as f:
                        doc_files[str(match.relative_to(root))] = f.read()
                except (UnicodeDecodeError, PermissionError):
                    continue
        
        return doc_files

