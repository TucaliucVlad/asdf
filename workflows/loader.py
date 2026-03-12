import yaml
from pathlib import Path
from typing import Dict, Any, List

class WorkflowLoader:
    """Loads workflow definitions exactly as per Correction Pack."""
    
    def __init__(self):
        self.workflows_dir = Path("workflows")
        self.workflows_dir.mkdir(exist_ok=True)
    
    def load(self, name: str = "default") -> Dict[str, Any]:
        path = self.workflows_dir / f"{name}.yaml"
        if not path.exists():
            raise FileNotFoundError(f"Workflow {name} not found")
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    def get_stages(self) -> List[Dict]:
        return self.load().get("stages", [])