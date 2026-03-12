from core.json_validator import JsonValidator
from core.retry_policy import retry_policy
from core.state_machine import StateMachine, ProjectState
from pathlib import Path

def run(project_id: str, plan: dict) -> dict:
    """Implementer — L1 protected code writing + triggers L2 via router."""
    output = {
        "batch_id": "impl-1",
        "task_ids": plan.get("task_ids", []),
        "files": plan.get("files", []),
        "self_healing_note": "Code written with L1 protection"
    }
    # L1 enforcement (structural)
    validated = retry_policy.l1_validate_and_retry(output, "code_writing", "impl-batch-1", plan.get("task_ids", []))
    
    # Materialize + L2 will be handled by StageRouter in next phase
    StateMachine(project_id).transition(ProjectState.MATERIALIZE_FILES, "impl-batch-1", plan.get("task_ids", []))
    return validated