import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
from core.json_validator import JsonValidator

class RetryPolicy:
    """Deterministic L1 (structural) + L2 (pytest) protection engine.
    MAX 3 retries each level — exactly per Correction Pack."""
    
    MAX_L1_RETRIES = 3
    MAX_L2_RETRIES = 3
    
    def __init__(self):
        self.validator = JsonValidator()
        self.log_path = Path("execution_log.jsonl")
        self.log_path.touch(exist_ok=True)  # create if missing
    
    def _append_log(self, entry: Dict[str, Any]) -> None:
        """Append-only execution_log.jsonl with all required fields."""
        entry["timestamp"] = datetime.utcnow().isoformat()
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    def _build_correction_prompt(self, errors: List[str], retry_index: int, level: str) -> str:
        """Structure-only correction prompt (no commentary, no extra text)."""
        return f"""FIX ONLY THE STRUCTURE. Retry {retry_index + 1}/{self.MAX_L1_RETRIES if level == "L1" else self.MAX_L2_RETRIES}.
Errors: {'; '.join(errors)}
Output ONLY valid JSON matching the schema. No explanations. No markdown."""

    def l1_validate_and_retry(self, data: Dict[str, Any], agent_type: str, batch_id: str, task_ids: List[str]) -> Dict[str, Any]:
        """L1 Protection: structural validation + up to 3 retries."""
        for retry_index in range(self.MAX_L1_RETRIES + 1):
            try:
                self.validator.validate(data, agent_type)
                self._append_log({
                    "protection_level": "L1",
                    "retry_index": retry_index,
                    "batch_id": batch_id,
                    "task_ids": task_ids,
                    "status": "SUCCESS",
                    "validation_errors": []
                })
                return data  # valid → proceed
            except Exception as e:
                errors = [str(e)]
                self._append_log({
                    "protection_level": "L1",
                    "retry_index": retry_index,
                    "batch_id": batch_id,
                    "task_ids": task_ids,
                    "status": "FAILED",
                    "validation_errors": errors
                })
                if retry_index == self.MAX_L1_RETRIES:
                    raise ValueError(f"L1 exhausted after {self.MAX_L1_RETRIES} retries: {errors}")
                # Return correction prompt for agent to retry
                raise ValueError(self._build_correction_prompt(errors, retry_index, "L1"))
    
    def l2_run_tests_and_retry(self, project_root: Path, test_files: List[str], batch_id: str, task_ids: List[str]) -> Dict[str, Any]:
        """L2 Protection: run pytest + up to 3 retries (materialized files already on disk)."""
        import subprocess
        for retry_index in range(self.MAX_L2_RETRIES + 1):
            try:
                result = subprocess.run(
                    ["pytest", "-q", "--tb=no"] + test_files,
                    cwd=project_root,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                passed = result.returncode == 0
                log_entry = {
                    "protection_level": "L2",
                    "retry_index": retry_index,
                    "batch_id": batch_id,
                    "task_ids": task_ids,
                    "status": "SUCCESS" if passed else "FAILED",
                    "validation_errors": [result.stdout + result.stderr] if not passed else []
                }
                self._append_log(log_entry)
                
                if passed:
                    return {"result": "success", "output": result.stdout}
                if retry_index == self.MAX_L2_RETRIES:
                    raise ValueError(f"L2 exhausted after {self.MAX_L2_RETRIES} retries")
                # Return correction prompt for next agent retry
                raise ValueError(self._build_correction_prompt(["pytest failed"], retry_index, "L2"))
            except Exception as e:
                self._append_log({"protection_level": "L2", "retry_index": retry_index, "status": "ERROR", "validation_errors": [str(e)]})
                raise

# Auto-init singleton for easy import
retry_policy = RetryPolicy()