from core.json_validator import JsonValidator
from core.retry_policy import retry_policy
from tools.llm_client import llm_call
import json
from pathlib import Path

def run(project_id: str, code_files: dict) -> dict:
    """Tester — FULLY GENERAL LLM + L1 retry (test_generation schema)."""
    schema_path = Path("schemas/test_generation.schema.json")
    schema_text = schema_path.read_text(encoding="utf-8") if schema_path.exists() else "Use exact test_generation schema."

    base_system = Path("init_prompt.txt").read_text(encoding="utf-8") if Path("init_prompt.txt").exists() else "You are a precise software engineering agent."

    system_prompt = f"""{base_system}

You MUST output ONLY a valid JSON object that matches EXACTLY this schema (no extra keys, no markdown, no explanations):

{schema_text}

Rules:
- Generate tests that cover the code from the previous stage.
- "test_files" array must contain at least 1 file.
- Use exactly these field names: "batch_id", "test_files", "path", "content", "covers"
- "covers" must be a non-empty array of strings.
- Output ONLY the JSON. Nothing else.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Project ID: {project_id}\nCode files: {json.dumps(code_files)}\nGenerate test_generation JSON NOW."}
    ]

    for attempt in range(4):
        try:
            response_text = llm_call(messages, max_tokens=3000, temperature=0.0)
            print(f"   [DEBUG LLM attempt {attempt}] {response_text[:500]}...")

            if response_text.strip().startswith("```"):
                response_text = response_text.split("```")[1].strip()
            output = json.loads(response_text.strip())

            validated = retry_policy.l1_validate_and_retry(output, "test_generation", f"test-batch-{attempt}", ["test-1"])
            print("✅ Tests generated")
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

    raise ValueError("L1 exhausted in tester after 3 retries")