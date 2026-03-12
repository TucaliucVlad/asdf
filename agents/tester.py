from pathlib import Path
from core.json_validator import JsonValidator
from core.retry_policy import retry_policy
from tools.llm_client import llm_call
import json

def run(project_id: str, previous_output: dict):
    """General tester using test_generation.schema.json — FORCES correct src import + robust tests only."""
    project_root = Path(f"projects/playground/{project_id}")
    main_code = (project_root / "src/main.py").read_text(encoding="utf-8") if (project_root / "src/main.py").exists() else ""

    schema_path = Path("schemas/test_generation.schema.json")
    schema = schema_path.read_text(encoding="utf-8") if schema_path.exists() else "{}"

    system = f"""Output ONLY valid JSON matching this schema exactly:

{schema}

CRITICAL RULES (general for ANY project — no exceptions):
- ALWAYS use path: "tests/test_main.py" (never root level)
- ALWAYS start test file with:
  import sys
  from pathlib import Path
  sys.path.insert(0, str(Path(__file__).parent.parent))
  import os
  os.environ['MPLBACKEND'] = 'Agg'
- ALWAYS import main class as: from src.main import YourClassName
- NEVER use 'from main' or relative imports
- Tests must be ROBUST behavioral only: hasattr, callable checks, "at least 1", grid enabled, mouse bind detection
- Test for a/b/c entries, canvas/figure, plot methods (single/append), mouse events (if present)
- Include full main.py context below:

=== MAIN CODE ===
{main_code[:2000]}
=== END ==="""

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"Project {project_id} — generate robust test JSON now."}
    ]

    for attempt in range(4):
        try:
            raw = llm_call(messages, model="xai/grok-code-fast-1", max_tokens=8000, temperature=0.0)
            print(f"   [DEBUG LLM attempt {attempt}] {raw[:300]}...")

            if "```" in raw:
                raw = raw.split("```")[1].strip()
            output = json.loads(raw)

            validated = retry_policy.l1_validate_and_retry(output, "test_generation", f"test-{attempt}", ["test-1"])
            print("✅ General robust convergence tests generated (correct src import + behavioral only)")
            return validated

        except Exception as e:
            messages.append({"role": "user", "content": str(e) + "\nFix ONLY JSON structure. Use 'from src.main import' and sys.path."})
            print(f"   → L1 retry {attempt+1}")

    raise ValueError("Tester convergence exhausted")