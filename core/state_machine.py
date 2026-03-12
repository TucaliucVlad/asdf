from enum import Enum, auto
from pathlib import Path
from typing import Dict, Any, Optional
import json
from core.retry_policy import retry_policy

class ProjectState(Enum):
    """Full state machine per Correction Pack — includes all L1/L2 retry paths."""
    CREATED = auto()
    REQUIREMENTS_FORMALIZED = auto()
    PLANNED = auto()
    
    # === L1 Protection Path ===
    L1_VALIDATE = auto()
    PROTECTION_LEVEL_1_RETRY_1 = auto()
    PROTECTION_LEVEL_1_RETRY_2 = auto()
    PROTECTION_LEVEL_1_RETRY_3 = auto()
    FAILED_L1_EXHAUSTED = auto()
    
    # === Materialization & L2 Protection Path ===
    MATERIALIZE_FILES = auto()
    RUN_TESTS = auto()
    PROTECTION_LEVEL_2_RETRY_1 = auto()
    PROTECTION_LEVEL_2_RETRY_2 = auto()
    PROTECTION_LEVEL_2_RETRY_3 = auto()
    FAILED_L2_EXHAUSTED = auto()
    
    REVIEW_BATCH = auto()
    COMPLETE = auto()
    FAILED = auto()  # terminal failure state

class StateMachine:
    """Deterministic state transitions with retry awareness + playground/shared support."""
    
    def __init__(self, project_id: str, mode: str = "playground"):
        self.project_id = project_id
        self.mode = mode
        self.project_root = Path(f"projects/{mode}/{project_id}")
        self.state_file = self.project_root / "state.json"
        self.project_root.mkdir(parents=True, exist_ok=True)
        self.current_state = self._load_state()
    
    def _load_state(self) -> ProjectState:
        if self.state_file.exists():
            data = json.loads(self.state_file.read_text(encoding="utf-8"))
            return ProjectState[data.get("state", "CREATED")]
        return ProjectState.CREATED
    
    def _save_state(self, new_state: ProjectState, metadata: Optional[Dict[str, Any]] = None) -> None:
        data = {
            "state": new_state.name,
            "project_id": self.project_id,
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        self.state_file.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        self.current_state = new_state
    
    def transition(self, next_state: ProjectState, batch_id: str = "", task_ids: list = None, metadata: Optional[Dict[str, Any]] = None) -> ProjectState:
        """Enforces valid transitions + auto-routes through protection levels."""
        task_ids = task_ids or []
        
        if next_state in (ProjectState.MATERIALIZE_FILES, ProjectState.REVIEW_BATCH):
            self._save_state(ProjectState.L1_VALIDATE, {"batch_id": batch_id, "task_ids": task_ids})
            return ProjectState.L1_VALIDATE
        
        if next_state == ProjectState.RUN_TESTS:
            self._save_state(ProjectState.RUN_TESTS, {"batch_id": batch_id, "task_ids": task_ids})
            return ProjectState.RUN_TESTS
        
        self._save_state(next_state, metadata)
        return next_state
    
    def handle_l1_failure(self, retry_index: int, batch_id: str, task_ids: list) -> ProjectState:
        """Maps L1 retry exhaustion to state."""
        if retry_index >= retry_policy.MAX_L1_RETRIES:
            self._save_state(ProjectState.FAILED_L1_EXHAUSTED)
            return ProjectState.FAILED_L1_EXHAUSTED
        retry_state = {
            0: ProjectState.PROTECTION_LEVEL_1_RETRY_1,
            1: ProjectState.PROTECTION_LEVEL_1_RETRY_2,
            2: ProjectState.PROTECTION_LEVEL_1_RETRY_3
        }[retry_index]
        self._save_state(retry_state)
        return retry_state
    
    def handle_l2_failure(self, retry_index: int, batch_id: str, task_ids: list) -> ProjectState:
        """Maps L2 retry exhaustion to state."""
        if retry_index >= retry_policy.MAX_L2_RETRIES:
            self._save_state(ProjectState.FAILED_L2_EXHAUSTED)
            return ProjectState.FAILED_L2_EXHAUSTED
        retry_state = {
            0: ProjectState.PROTECTION_LEVEL_2_RETRY_1,
            1: ProjectState.PROTECTION_LEVEL_2_RETRY_2,
            2: ProjectState.PROTECTION_LEVEL_2_RETRY_3
        }[retry_index]
        self._save_state(retry_state)
        return retry_state
    
    def is_terminal(self) -> bool:
        return self.current_state in (ProjectState.COMPLETE, ProjectState.FAILED, ProjectState.FAILED_L1_EXHAUSTED, ProjectState.FAILED_L2_EXHAUSTED)

    @classmethod
    def exists(cls, project_id: str, mode: str = "playground"):
        """Used by status/list — NEVER creates any folder or file."""
        return (Path(f"projects/{mode}/{project_id}/state.json")).exists()