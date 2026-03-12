import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
import os
import subprocess

class RetryPolicy:
    """Deterministic L1 (structural) + L2 (pytest) protection engine.
    MAX 3 retries each level — exactly per Correction Pack."""

    MAX_L1_RETRIES = 3
    MAX_L2_RETRIES = 3

    def __init__(self):
        self.log_path = Path("execution_log.jsonl")
        self.log_path.touch(exist_ok=True)

    def _append_log(self, entry: Dict[str, Any]) -> None:
        entry["timestamp"] = datetime.utcnow().isoformat()
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _build_correction_prompt(self, errors: List[str], retry_index: int, level: str, extra_context: str = "") -> str:
        max_retries = self.MAX_L1_RETRIES if level == "L1" else self.MAX_L2_RETRIES
        context = f"\nExtra context (test output/traceback): {extra_context}" if extra_context else ""
        return f"""FIX ONLY THE STRUCTURE OR CODE. Retry {retry_index + 1}/{max_retries} ({level}).
Errors: {'; '.join(errors)}{context}
Output ONLY valid JSON matching the schema. No explanations. No markdown. No extra text."""

    def l1_validate_and_retry(self, data: Dict[str, Any], agent_type: str, batch_id: str, task_ids: List[str]) -> Dict[str, Any]:
        for retry_index in range(self.MAX_L1_RETRIES + 1):
            try:
                # (L1 validator still works — unchanged)
                from core.json_validator import JsonValidator
                JsonValidator().validate(data, agent_type)
                self._append_log({"protection_level": "L1", "retry_index": retry_index, "batch_id": batch_id, "task_ids": task_ids, "status": "SUCCESS", "validation_errors": []})
                return data
            except Exception as e:
                errors = [str(e)]
                self._append_log({"protection_level": "L1", "retry_index": retry_index, "batch_id": batch_id, "task_ids": task_ids, "status": "FAILED", "validation_errors": errors})
                if retry_index == self.MAX_L1_RETRIES:
                    raise ValueError(f"L1 protection exhausted after {self.MAX_L1_RETRIES} retries")
                raise ValueError(self._build_correction_prompt(errors, retry_index, "L1"))

    def l2_run_tests_and_retry(self, project_root: Path, test_args: List[str], batch_id: str, task_ids: List[str]) -> Dict[str, Any]:
        """L2 Protection — now with PYTHONPATH + python -m pytest (fixes src import errors)."""
        for retry_index in range(self.MAX_L2_RETRIES + 1):
            try:
                env = os.environ.copy()
                env["PYTHONPATH"] = str(project_root)  # ← makes 'src' importable
                
                result = subprocess.run(
                    ["python", "-m", "pytest", "-q", "--tb=short"] + test_args,
                    cwd=project_root,
                    capture_output=True,
                    text=True,
                    timeout=45,
                    env=env
                )
                passed = result.returncode == 0
                errors = [result.stdout + "\n" + result.stderr] if not passed else []

                self._append_log({
                    "protection_level": "L2",
                    "retry_index": retry_index,
                    "batch_id": batch_id,
                    "task_ids": task_ids,
                    "status": "SUCCESS" if passed else "FAILED",
                    "validation_errors": errors
                })

                if passed:
                    return {"status": "success", "output": result.stdout}

                if retry_index == self.MAX_L2_RETRIES:
                    raise ValueError(f"L2 protection exhausted after {self.MAX_L2_RETRIES} retries. Test failures: {errors[0] if errors else 'unknown'}")

                raise ValueError(self._build_correction_prompt(
                    ["Tests failed"], retry_index, "L2", extra_context=errors[0][:800] if errors else ""
                ))

            except Exception as e:
                self._append_log({
                    "protection_level": "L2",
                    "retry_index": retry_index,
                    "batch_id": batch_id,
                    "task_ids": task_ids,
                    "status": "ERROR",
                    "validation_errors": [str(e)]
                })
                raise

retry_policy = RetryPolicy()