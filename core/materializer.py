from pathlib import Path
from typing import Dict, List

class Materializer:
    """Writes validated files to disk safely (playground/shared)."""
    
    @staticmethod
    def materialize(project_root: Path, files_list: List[Dict]):
        """Materializes every file from scaffolding or code_writing JSON."""
        for f in files_list:
            full_path = project_root / f["path"]
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(f.get("content", "# placeholder"), encoding="utf-8")
            print(f"   ✅ Materialized: {f['path']}")
        print(f"   📁 All files written to {project_root}")