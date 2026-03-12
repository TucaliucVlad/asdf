from core.json_validator import JsonValidator
from core.retry_policy import retry_policy
from core.state_machine import StateMachine, ProjectState
from tools.llm_client import llm_call
import json
from pathlib import Path

def run(project_id: str, user_prompt: str) -> dict:
    """Requirements Engineer — 100% GENERAL + FORCES COMPLETE PROJECT SKELETON."""
    schema_path = Path("schemas/scaffolding.schema.json")
    schema_text = schema_path.read_text(encoding="utf-8") if schema_path.exists() else ""

    base_system = Path("init_prompt.txt").read_text(encoding="utf-8") if Path("init_prompt.txt").exists() else "You are a precise software engineering agent."

    system_prompt = f"""{base_system}

You MUST create a COMPLETE, runnable project that matches the user vision.

ALWAYS include these files (no exceptions):
- requirements.txt (list all dependencies needed)
- src/main.py (full working code)
- tests/test_main.py (unit tests)
- Proper folders: src, tests

Output EXACTLY this schema:

{schema_text}

Rules:
- "files" array MUST have at least 3 files (requirements.txt + src/main.py + tests/test_main.py)
- Content must be real and complete for the vision
- Output ONLY the JSON. Nothing else.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Project ID: {project_id}\nVision: {user_prompt}\nGenerate scaffolding JSON NOW."}
    ]

    for attempt in range(4):
        try:
            response_text = llm_call(messages, max_tokens=3500, temperature=0.0)
            print(f"   [DEBUG LLM attempt {attempt}] {response_text[:600]}...")

            if response_text.strip().startswith("```"):
                response_text = response_text.split("```")[1].strip()
            output = json.loads(response_text.strip())

            validated = retry_policy.l1_validate_and_retry(output, "scaffolding", f"req-batch-{attempt}", ["req-1"])
            StateMachine(project_id).transition(ProjectState.REQUIREMENTS_FORMALIZED)
            print("✅ Requirements formalized + full skeleton materialized")
            return validated

        except ValueError as e:
            error_str = str(e)
            if "FIX ONLY THE STRUCTURE" in error_str or "L1 validation failed" in error_str:
                messages.append({"role": "user", "content": error_str + "\nInclude requirements.txt + src/main.py + tests/test_main.py. Fix now."})
                print(f"   → L1 retry {attempt+1}/3")
                continue
            raise
        except json.JSONDecodeError:
            messages.append({"role": "user", "content": "Return ONLY valid JSON matching the schema."})
            continue

    raise ValueError("L1 exhausted in requirements_engineer")