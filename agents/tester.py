from core.json_validator import JsonValidator
from core.retry_policy import retry_policy

def run(project_id: str, code_files: dict) -> dict:
    """Tester — generates tests and triggers L2 protection."""
    output = {
        "batch_id": "test-1",
        "test_files": [{
            "path": "tests/test_main.py",
            "content": "def test_main(): assert True",
            "covers": ["main.py"]
        }]
    }
    validated = retry_policy.l1_validate_and_retry(output, "test_generation", "test-batch-1", ["test-1"])
    return validated