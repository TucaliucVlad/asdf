from core.json_validator import JsonValidator
from core.retry_policy import retry_policy
from core.state_machine import StateMachine, ProjectState
from tools.llm_client import llm_call
import json
from pathlib import Path

def run(project_id: str, plan: dict) -> dict:
    """Implementer — FULLY GENERAL LLM + L1 retry (code_writing schema)."""
    schema_path = Path("schemas/code_writing.schema.json")
    schema_text = schema_path.read_text(encoding="utf-8") if schema_path.exists() else "Use exact code_writing schema."

    base_system = Path("init_prompt.txt").read_text(encoding="utf-8") if Path("init_prompt.txt").exists() else "You are a precise software engineering agent."

    system_prompt = f"""{base_system}

You MUST output ONLY a valid JSON object that matches EXACTLY this schema (no extra keys, no markdown, no explanations):

{schema_text}

Rules:
- Generate real implementation files based on the plan and user vision.
- "files" array must contain at least 1 file with full working code.
- Use exactly these field names: "batch_id", "task_ids", "files", "path", "content", "intent", "test_instructions", "self_healing_note"
- "task_ids" and "test_instructions" must be non-empty arrays.
- Output ONLY the JSON. Nothing else.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Project ID: {project_id}\nPlan: {json.dumps(plan)}\nGenerate full code_writing JSON NOW."}
    ]

    for attempt in range(4):
        try:
            response_text = llm_call(messages, max_tokens=8000, temperature=0.2)
            print(f"   [DEBUG LLM attempt {attempt}] {response_text[:500]}...")

            if response_text.strip().startswith("```"):
                response_text = response_text.split("```")[1].strip()
            output = json.loads(response_text.strip())

            validated = retry_policy.l1_validate_and_retry(output, "code_writing", f"impl-batch-{attempt}", plan.get("task_ids", []))
            StateMachine(project_id).transition(ProjectState.MATERIALIZE_FILES)
            print("✅ Implementation + L1/L2 protection + code materialized")
            return validated

        except ValueError as e:
            error_str = str(e)
            if "FIX ONLY THE STRUCTURE" in error_str or "L1 validation failed" in error_str:
                messages.append({"role": "user", "content": error_str + "\nFix only the structure using the exact field names above. Try again."})
                print(f"   → L1 retry {attempt+1}/3 - sending correction to Grok...")
                continue
            raise
        except json.JSONDecodeError:
            messages.append({"role": "user", "content": "Return ONLY valid JSON matching the schema. No markdown."})
            continue

    raise ValueError("L1 exhausted in implementer after 3 retries")