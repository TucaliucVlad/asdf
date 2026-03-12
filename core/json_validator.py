import json
from pathlib import Path
from jsonschema import validate, ValidationError
from typing import Any, Dict

class JsonValidator:
    """L1 structural validator — exactly as per Correction Pack.
    Enforces additionalProperties: false + path-escape safety."""

    def __init__(self):
        self.schemas_dir = Path("schemas")
        self.schema_map = {
            "scaffolding": "scaffolding.schema.json",
            "code_writing": "code_writing.schema.json",
            "test_generation": "test_generation.schema.json",
            "documentation_report": "documentation_report.schema.json",
        }

    def _load_schema(self, schema_name: str) -> Dict[str, Any]:
        path = self.schemas_dir / self.schema_map[schema_name]
        if not path.exists():
            raise FileNotFoundError(f"Schema not found: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def _sanitize_path(self, path_str: str) -> str:
        """Protection against path traversal / absolute paths."""
        p = Path(path_str).resolve().relative_to(Path.cwd())
        if ".." in str(p) or p.is_absolute() or p.parts[0] == "..":
            raise ValueError(f"Unsafe path detected: {path_str}")
        return str(p)

    def validate(self, data: Dict[str, Any], agent_type: str) -> None:
        """Main L1 enforcement point."""
        if agent_type not in self.schema_map:
            raise ValueError(f"Unknown agent_type: {agent_type}")

        schema = self._load_schema(agent_type)

        # 1. JSON Schema validation (strict)
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            raise ValueError(f"L1 validation failed for {agent_type}: {e.message}")

        # 2. Extra path-escape protection on all file paths
        if agent_type in ("scaffolding", "code_writing"):
            for f in data.get("files", []):
                self._sanitize_path(f["path"])
        elif agent_type == "test_generation":
            for f in data.get("test_files", []):
                self._sanitize_path(f["path"])