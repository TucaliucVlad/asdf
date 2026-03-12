from core.json_validator import JsonValidator
from core.retry_policy import retry_policy

def run(project_id: str, requirements: dict) -> dict:
    """Planner — outputs task list for next stage."""
    output = {
        "batch_id": "plan-1",
        "task_ids": ["task-1", "task-2"],
        "files": requirements.get("files", []),  # pass through for implementer
        "self_healing_note": "Planning complete"
    }
    validated = retry_policy.l1_validate_and_retry(output, "code_writing", "plan-batch-1", ["task-1"])
    return validated