from pathlib import Path
import yaml

class WorkflowLoader:
    """Loads deterministic workflow stages from YAML (Correction Pack)."""
    
    def __init__(self):
        self.workflow_path = Path("workflows/default.yaml")
    
    def get_stages(self):
        if self.workflow_path.exists():
            data = yaml.safe_load(self.workflow_path.read_text())
            return data.get("stages", [])
        # Fallback deterministic sequence
        return [
            {"name": "requirements", "next_state": "REQUIREMENTS_FORMALIZED", "protection": "L1"},
            {"name": "planning", "next_state": "PLANNED", "protection": "L1"},
            {"name": "implementation", "next_state": "MATERIALIZE_FILES", "protection": "L1_L2"},
            {"name": "testing", "next_state": "RUN_TESTS", "protection": "L2"},
        ]