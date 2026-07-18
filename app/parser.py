import os
from pathlib import Path
from typing import List, Tuple

def parse_repo(repo_path: str) -> List[Tuple[str, str]]:

    valid_extensions = {
        ".py", ".js", ".ts", ".jsx", ".tsx",
        ".c", ".h", ".cpp", ".hpp",
        ".java", ".go", ".rs",
        ".md", ".txt", ".json", ".yaml", ".yml"
    }

    exclude_dirs = {
        ".git", "__pycache__", ".venv", "venv", "env",
        "node_modules", "dist", "build", "target",
        ".pytest_cache", ".mypy_cache", "vendor",
        ".idea", ".vscode", "egg-info"
    }

    res = []

    for dirpath, dirnames, filenames in os.walk(repo_path):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        for file in filenames:
            file_path = Path(dirpath) / file
            
            if file_path.suffix not in valid_extensions:
                continue
        
            try: 
                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = f.read()

            except UnicodeDecodeError:
                print(f"Skipping non-UTF-8 file: {file_path}")
                continue

            res.append((str(file_path), contents))

    return res

