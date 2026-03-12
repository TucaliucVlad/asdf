from pathlib import Path
from typing import Dict, List, Union

class Materializer:
    """Writes validated files to disk safely. Now auto-creates __init__.py for src/ and tests/ packages."""

    @staticmethod
    def materialize(project_root: Path, files_list: Union[List[Dict], Dict[str, Any]]) -> None:
        if isinstance(files_list, dict):
            items = files_list.get("files", []) or files_list.get("test_files", [])
        else:
            items = files_list

        for f in items:
            if not isinstance(f, dict) or "path" not in f:
                continue
            full_path = project_root / f["path"]
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # AUTO-CREATE __init__.py for packages (fixes import errors)
            if full_path.parent.name in ("src", "tests"):
                init_file = full_path.parent / "__init__.py"
                if not init_file.exists():
                    init_file.write_text("# Auto-generated package marker for src/tests layout\n", encoding="utf-8")
                    print(f"   ✅ Created package marker: {init_file.relative_to(project_root)}")
            
            content = f.get("content", "# placeholder (L1-protected)")
            full_path.write_text(content, encoding="utf-8")
            print(f"   ✅ Materialized: {f['path']}")
        
        print(f"   All files written safely to {project_root}")