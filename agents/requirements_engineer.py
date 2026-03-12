from core.json_validator import JsonValidator
from core.retry_policy import retry_policy
from core.state_machine import StateMachine, ProjectState   # ← enum imported

def run(project_id: str, user_prompt: str) -> dict:
    """Requirements Engineer — outputs ONLY valid scaffolding JSON."""
    output = {
        "project_name": project_id,
        "folders": ["src", "tests"],
        "files": [{
            "path": "src/main.py",
            "content": "# Entry point",
            "intent": "main module",
            "test_instructions": ["run main"]
        }]
    }
    # L1 enforcement
    validated = retry_policy.l1_validate_and_retry(output, "scaffolding", "req-batch-1", ["req-1"])
    
    # FIXED: use enum (not string)
    StateMachine(project_id).transition(ProjectState.REQUIREMENTS_FORMALIZED)
    return validated