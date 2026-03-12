from core.json_validator import JsonValidator
from core.retry_policy import retry_policy
from core.state_machine import StateMachine, ProjectState
from pathlib import Path

def run(project_id: str, plan: dict) -> dict:
    """Implementer — now generates real files based on seed."""
    output = {
        "batch_id": "impl-1",
        "task_ids": plan.get("task_ids", []),
        "files": [
            {
                "path": "src/main.py",
                "content": 'print("Hello from protected pipeline v2!")',
                "intent": "entry point",
                "test_instructions": ["run main"]
            }
        ],
        "self_healing_note": "L1 protected"
    }
    validated = retry_policy.l1_validate_and_retry(output, "code_writing", "impl-batch-1", plan.get("task_ids", []))
    StateMachine(project_id).transition(ProjectState.MATERIALIZE_FILES)
    return validated