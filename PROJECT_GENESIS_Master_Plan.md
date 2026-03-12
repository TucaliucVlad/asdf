# PROJECT GENESIS — Correction Pack

This document is a targeted supplement to **PROJECT_GENESIS_Master_Plan.md**. It corrects the three concrete weaknesses identified in review:

1. the original plan was still high-level around **Protection Level 1 / Level 2 retry logic** and **strict JSON schemas**;
2. the original plan referenced a few extra agents that were not yet specified at implementation level;
3. the original plan did not include enough **copy-paste-ready examples** for schema enforcement, YAML workflows, and critical control logic.

This addendum is intentionally narrow. It does **not** replace the master plan; it makes the previously vague parts operational.

---

## 1. Exact Protection Logic

The protection system has exactly two levels:

- **Level 1** = structural failure of the LLM output before file materialization.
- **Level 2** = semantic/runtime failure after file materialization and test execution.

The protection logic is deterministic and must be implemented as a finite retry policy with append-only logging.

### 1.1 Level 1 — Structural / Format Recovery

#### 1.1.1 Trigger conditions
Level 1 triggers if **any** of the following is true:

1. No fenced JSON block was found when JSON was required.
2. More than one fenced JSON block was found when a single block was required.
3. JSON parsing fails.
4. JSON root type is incorrect.
5. Required keys are missing.
6. Any field violates the schema type or cardinality.
7. A file path attempts escape (`..`, absolute path outside project root, drive prefix, null byte).
8. Duplicate file paths exist in the same payload.
9. Content is missing for a file entry.
10. Unknown top-level keys are present when `additionalProperties=false` is enforced.

#### 1.1.2 Retry budget
- `MAX_L1_RETRIES = 3`
- Retries are counted **per stage invocation**, not globally for the project.
- After the third failed structural correction, the batch enters `FAILED_L1_EXHAUSTED` and stops.

#### 1.1.3 Correction prompt policy
The correction prompt must:

- preserve all original semantic content,
- request **structure-only repair**,
- restate the exact schema contract,
- include the validation error list,
- forbid commentary outside the JSON block.

#### 1.1.4 Deterministic retry sequence

```text
Attempt 0: Original model response
  -> validate JSON envelope
  -> validate schema
  -> validate paths
  -> if all pass: SUCCESS
  -> else: Protection Level 1

Attempt 1: Send corrective prompt with original response + validation errors
  -> validate again

Attempt 2: Same model, stricter corrective prompt, include first failure + second failure
  -> validate again

Attempt 3: Same model OR designated fallback formatter model
  -> validate again

If still invalid:
  -> mark batch failed
  -> write immutable failure event
  -> do not materialize files
```

#### 1.1.5 State transitions

```text
CODE_WRITING -> L1_VALIDATE ->
  PASS -> MATERIALIZE_FILES
  FAIL -> PROTECTION_LEVEL_1_RETRY_1
  FAIL -> PROTECTION_LEVEL_1_RETRY_2
  FAIL -> PROTECTION_LEVEL_1_RETRY_3
  FAIL -> FAILED_L1_EXHAUSTED
```

#### 1.1.6 Required log fields for each Level 1 retry
Each retry appends a log entry with:

- `timestamp`
- `project_id`
- `stage`
- `protection_level = 1`
- `retry_index`
- `agent_name`
- `model_name`
- `validation_errors[]`
- `original_response_hash`
- `corrective_prompt_hash`
- `token_counts.prompt`
- `token_counts.response`
- `dollar_cost`
- `result = pass|fail`

---

### 1.2 Level 2 — Runtime / Test Recovery

#### 1.2.1 Trigger conditions
Level 2 triggers only **after** valid files were written and one of the following occurs:

1. `pytest` returns non-zero.
2. Import errors occur.
3. Syntax errors occur.
4. Runtime exceptions occur in the test phase.
5. Coverage gate fails for newly introduced modules.
6. Review detects that a requirement was not actually implemented, even though tests passed.

#### 1.2.2 Retry budget
- `MAX_L2_RETRIES = 3`
- Retries are counted **per batch**, not per file.
- Every Level 2 retry must add or preserve a regression test for the observed failure.

#### 1.2.3 Regeneration policy
At Level 2, the system must notify **both** the Implementer and the Tester.

Inputs to the regeneration prompt must include:

- original task description,
- exact failing test names,
- traceback,
- affected file paths,
- current implementation snippets,
- coverage shortfall if relevant,
- instruction that the fix must preserve already passing behavior.

#### 1.2.4 Deterministic retry sequence

```text
Run pytest
  -> PASS + coverage gate PASS + review PASS => SUCCESS
  -> FAIL => Protection Level 2

Retry 1:
  Implementer regenerates code delta in strict JSON
  Tester regenerates failing and regression tests in strict JSON
  materialize
  rerun pytest

Retry 2:
  same, with cumulative failure history added
  rerun pytest

Retry 3:
  same, with root-cause summary forced into prompt
  rerun pytest

If still failing:
  -> mark batch FAILED_L2_EXHAUSTED
  -> stop downstream progression
```

#### 1.2.5 Level 2 success condition
A Level 2 cycle is considered resolved only if **all** are true:

1. all tests in the batch pass,
2. no previously passing tests regress,
3. coverage for touched new modules remains at or above the configured threshold,
4. reviewer marks requirement coverage as complete for the batch.

#### 1.2.6 State transitions

```text
MATERIALIZE_FILES -> RUN_TESTS ->
  PASS -> REVIEW_BATCH
  FAIL -> PROTECTION_LEVEL_2_RETRY_1
  FAIL -> PROTECTION_LEVEL_2_RETRY_2
  FAIL -> PROTECTION_LEVEL_2_RETRY_3
  FAIL -> FAILED_L2_EXHAUSTED
```

#### 1.2.7 Required log fields for each Level 2 retry
Each retry appends a log entry with:

- `timestamp`
- `project_id`
- `stage`
- `protection_level = 2`
- `retry_index`
- `failing_tests[]`
- `traceback_excerpt`
- `affected_files[]`
- `coverage_before`
- `coverage_after`
- `prompt_hashes.implementer`
- `prompt_hashes.tester`
- `token_counts`
- `dollar_cost`
- `result = pass|fail`

---

### 1.3 Global retry rules

These are mandatory and supersede any local heuristics:

1. No stage may exceed **three retries**.
2. A failed Level 1 attempt does **not** consume Level 2 budget.
3. A failed Level 2 attempt does **not** reset Level 1 budget for the same cycle.
4. Each retry must be logged as a separate append-only event.
5. Retrying with the exact same prompt text is forbidden; each retry prompt must include incremental diagnostic information.
6. Retrying may switch to a fallback model **only** if the workflow YAML explicitly allows it.
7. If retries are exhausted, the project remains resumable from the failed batch.

---

## 2. Strict JSON Contracts

The system should use **formal JSON Schema files** under `schemas/`, but the following contracts define exactly what must be enforced.

---

### 2.1 Scaffolding Output Schema

File: `schemas/scaffolding.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ScaffoldingOutput",
  "type": "object",
  "additionalProperties": false,
  "required": ["project_name", "folders", "files"],
  "properties": {
    "project_name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 120,
      "pattern": "^[A-Za-z0-9._ -]+$"
    },
    "folders": {
      "type": "array",
      "uniqueItems": true,
      "items": {
        "type": "string",
        "minLength": 1
      }
    },
    "files": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["path", "content", "intent", "test_instructions"],
        "properties": {
          "path": {
            "type": "string",
            "minLength": 1
          },
          "content": {
            "type": "string"
          },
          "intent": {
            "type": "string",
            "minLength": 1
          },
          "test_instructions": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "string",
              "minLength": 1
            }
          }
        }
      }
    }
  }
}
```

#### Additional non-schema checks
These must be enforced in Python even if not expressed in JSON Schema:

- every file path must be relative,
- every file path must resolve under `projects/<project-id>/implementation/`,
- no duplicate normalized paths,
- every parent folder must either exist or be creatable under the same root,
- path separators are normalized before validation.

#### Minimal valid example

```json
{
  "project_name": "sample_project",
  "folders": [
    "src",
    "src/utils",
    "tests"
  ],
  "files": [
    {
      "path": "src/__init__.py",
      "content": "",
      "intent": "Mark src as a Python package.",
      "test_instructions": [
        "No direct unit test required.",
        "Import package in test_smoke_imports.py."
      ]
    }
  ]
}
```

---

### 2.2 Code-Writing Output Schema

File: `schemas/code_writing.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "CodeWritingOutput",
  "type": "object",
  "additionalProperties": false,
  "required": ["batch_id", "task_ids", "files", "self_healing_note"],
  "properties": {
    "batch_id": {
      "type": "string",
      "minLength": 1
    },
    "task_ids": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "string",
        "minLength": 1
      }
    },
    "files": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["path", "content", "intent", "test_instructions"],
        "properties": {
          "path": { "type": "string", "minLength": 1 },
          "content": { "type": "string" },
          "intent": { "type": "string", "minLength": 1 },
          "test_instructions": {
            "type": "array",
            "minItems": 1,
            "items": { "type": "string", "minLength": 1 }
          }
        }
      }
    },
    "self_healing_note": {
      "type": "string",
      "minLength": 1
    }
  }
}
```

#### Semantic constraints
- `task_ids` must match tasks currently active in the batch.
- Files outside the project implementation root are rejected.
- When editing an existing file, the full replacement content must be emitted; partial patch language is not allowed in MVP.
- `self_healing_note` must explain the defensive logic inserted (try/except, fallback paths, validation).

---

### 2.3 Test-Generation Output Schema

File: `schemas/test_generation.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "TestGenerationOutput",
  "type": "object",
  "additionalProperties": false,
  "required": ["batch_id", "test_files"],
  "properties": {
    "batch_id": {
      "type": "string",
      "minLength": 1
    },
    "test_files": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["path", "content", "covers"],
        "properties": {
          "path": { "type": "string", "minLength": 1 },
          "content": { "type": "string" },
          "covers": {
            "type": "array",
            "minItems": 1,
            "items": { "type": "string", "minLength": 1 }
          }
        }
      }
    }
  }
}
```

---

### 2.4 Documentation Report Schema

File: `schemas/documentation_report.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "DocumentationReport",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "project_id",
    "batch_id",
    "task_ids",
    "summary",
    "files_changed",
    "tests_run",
    "result",
    "usage_reason"
  ],
  "properties": {
    "project_id": { "type": "string", "minLength": 1 },
    "batch_id": { "type": "string", "minLength": 1 },
    "task_ids": {
      "type": "array",
      "minItems": 1,
      "items": { "type": "string", "minLength": 1 }
    },
    "summary": { "type": "string", "minLength": 1 },
    "files_changed": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 }
    },
    "tests_run": {
      "type": "array",
      "items": { "type": "string", "minLength": 1 }
    },
    "result": {
      "type": "string",
      "enum": ["success", "partial", "failure"]
    },
    "usage_reason": { "type": "string", "minLength": 1 }
  }
}
```

---

### 2.5 Execution Log Entry Schema

File: `schemas/execution_log.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ExecutionLogEntry",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "timestamp",
    "project_id",
    "agent_name",
    "stage",
    "event_type",
    "retry_count",
    "prompt",
    "response",
    "tokens",
    "dollars"
  ],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "project_id": { "type": "string", "minLength": 1 },
    "agent_name": { "type": "string", "minLength": 1 },
    "stage": { "type": "string", "minLength": 1 },
    "event_type": {
      "type": "string",
      "enum": [
        "llm_call",
        "validation",
        "file_write",
        "test_run",
        "retry",
        "review",
        "documentation",
        "failure"
      ]
    },
    "retry_count": { "type": "integer", "minimum": 0 },
    "prompt": { "type": "string" },
    "response": { "type": "string" },
    "tokens": {
      "type": "object",
      "additionalProperties": false,
      "required": ["prompt", "response", "total"],
      "properties": {
        "prompt": { "type": "integer", "minimum": 0 },
        "response": { "type": "integer", "minimum": 0 },
        "total": { "type": "integer", "minimum": 0 }
      }
    },
    "dollars": { "type": "number", "minimum": 0 }
  }
}
```

#### Append-only rule
The execution log is append-only at application level:

- existing entries may never be modified in place,
- new events are appended as new objects,
- corrections must be recorded as new events, not edits of earlier events.

---

## 3. Workflow YAML Contract

The original master plan required five YAML workflow files. This section defines the exact minimum schema they must follow.

### 3.1 Required workflow fields
Every workflow YAML must contain:

- `workflow_id`
- `name`
- `stage`
- `agent_role`
- `model`
- `max_tokens`
- `temperature`
- `input_contract`
- `output_schema`
- `success_criteria`
- `retry_policy`
- `test_procedure`
- `transitions`

### 3.2 Canonical example — `workflows/01_scaffolding.yaml`

```yaml
workflow_id: "01_scaffolding"
name: "Project Scaffolding"
stage: "scaffolding"
agent_role: "requirements_engineer"
model: "gpt-5.4-thinking"
max_tokens: 12000
temperature: 0.1
input_contract:
  required:
    - project_id
    - client_prompt
    - clarified_requirements
output_schema: "schemas/scaffolding.schema.json"
success_criteria:
  - "Exactly one fenced JSON block is returned."
  - "JSON validates against scaffolding.schema.json."
  - "All target paths remain under project implementation root."
  - "Scaffolder creates all folders and files without collision."
retry_policy:
  protection_level_1:
    max_retries: 3
    fallback_model: "gpt-5.4-thinking"
  protection_level_2:
    max_retries: 0
test_procedure:
  - "Validate JSON envelope extraction."
  - "Validate JSON schema."
  - "Run path normalization and path traversal checks."
  - "Create files in temp project root and assert existence."
transitions:
  on_success: "code_writing"
  on_l1_exhausted: "failed_l1_exhausted"
  on_error: "failed_l1_exhausted"
```

### 3.3 Canonical example — `workflows/02_code_writing.yaml`

```yaml
workflow_id: "02_code_writing"
name: "Code Writing"
stage: "code_writing"
agent_role: "implementer"
model: "gpt-5.4-thinking"
max_tokens: 18000
temperature: 0.15
input_contract:
  required:
    - project_id
    - batch_id
    - tasks
    - implementation_root
output_schema: "schemas/code_writing.schema.json"
success_criteria:
  - "Output validates against code_writing.schema.json."
  - "All files contain full replacement content."
  - "self_healing_note is present and non-empty."
retry_policy:
  protection_level_1:
    max_retries: 3
    fallback_model: "gpt-5.4-thinking"
  protection_level_2:
    max_retries: 3
    fallback_model: "gpt-5.4-thinking"
test_procedure:
  - "Validate envelope and schema."
  - "Write files to temp implementation root."
  - "Run pytest for batch-specific tests."
  - "Enforce coverage threshold for new modules."
transitions:
  on_success: "testing"
  on_l1_exhausted: "failed_l1_exhausted"
  on_l2_exhausted: "failed_l2_exhausted"
```

---

## 4. Missing Agents — Exact MVP Implementation Plan

The critique was correct: some agents were named before being specified. The following turns those agents into implementable MVP classes.

---

### 4.1 BrainstormerAgent

#### Purpose
Expand the domain map produced by the Requirements Engineer and return:

- completions,
- adjacent domains,
- risks,
- missing assumptions,
- clarification questions.

#### Minimum class contract

```python
class BrainstormerAgent(BaseAgent):
    def generate_completions(self, idea_packet: dict) -> dict:
        ...
```

#### Required input

```json
{
  "project_id": "proj_001",
  "root_idea": "user prompt text",
  "domains": ["control systems", "embedded software"],
  "subdomains": ["state machines", "CLI orchestration"],
  "constraints": ["local-first", "autonomous by default"]
}
```

#### Required output

```json
{
  "completions": ["..."],
  "adjacent_domains": ["..."],
  "risks": ["..."],
  "assumptions": ["..."],
  "clarification_questions": ["..."]
}
```

#### Acceptance criteria
- Output keys are always present.
- Empty lists are allowed only for `clarification_questions` once completeness is reached.
- No prose outside the JSON block.
- At least one adjacent domain must be proposed when the input contains more than one root domain.

#### Unit tests required
- `test_brainstormer_returns_all_keys`
- `test_brainstormer_handles_single_domain_input`
- `test_brainstormer_questions_can_be_empty_only_after_clear_signal`
- `test_brainstormer_json_is_schema_valid`

---

### 4.2 ReviewerAgent

#### Purpose
Perform post-batch gap analysis and answer one binary question:

> Does this batch fully satisfy the linked requirements without hidden omissions?

#### Minimum class contract

```python
class ReviewerAgent(BaseAgent):
    def review_batch(self, requirement_slice: list, batch_artifacts: dict) -> dict:
        ...
```

#### Required input

```json
{
  "requirement_ids": ["REQ-12", "REQ-13"],
  "requirements": [
    {"id": "REQ-12", "text": "..."},
    {"id": "REQ-13", "text": "..."}
  ],
  "changed_files": ["core/state_machine.py"],
  "tests_passed": ["tests/unit/test_state_machine.py::test_loads_workflows"],
  "coverage_summary": {
    "new_modules": 0.86
  }
}
```

#### Required output

```json
{
  "approved": true,
  "covered_requirements": ["REQ-12", "REQ-13"],
  "missing_requirements": [],
  "review_notes": ["All specified transitions are implemented and tested."],
  "follow_up_tasks": []
}
```

#### Decision rule
- `approved=true` only if `missing_requirements` is empty.
- If any requirement is only partially met, it must appear in `missing_requirements`.
- `follow_up_tasks` must be non-empty whenever `approved=false`.

#### Unit tests required
- `test_reviewer_approves_complete_batch`
- `test_reviewer_rejects_partial_requirement_coverage`
- `test_reviewer_emits_follow_up_tasks_when_rejected`
- `test_reviewer_json_is_schema_valid`

---

### 4.3 Agent registration and reuse matcher

The 75% reuse threshold must not remain conceptual. For MVP, implement it as weighted overlap.

#### Reuse score formula

```text
reuse_score =
  0.40 * skill_overlap_ratio +
  0.25 * workflow_overlap_ratio +
  0.20 * role_similarity_ratio +
  0.15 * tool_overlap_ratio
```

Reuse rule:

- if `reuse_score >= 0.75`: reuse existing agent;
- else: create new stub agent with history file initialized.

#### Minimum stub fields

```json
{
  "agent_id": "agent_017",
  "agent_name": "reviewer_v1",
  "agent_role": "reviewer",
  "skills": ["requirement coverage analysis", "gap detection"],
  "history_path": "agents/history/reviewer_v1.json"
}
```

---

## 5. Copy-Paste-Ready Control Snippets

These are not the full implementation, but they make the blueprint executable enough for coding.

---

### 5.1 ProtectionAgent skeleton

```python
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ProtectionResult:
    passed: bool
    level: int
    retry_index: int
    errors: List[str]
    corrected_response: str | None = None


class ProtectionAgent:
    MAX_L1_RETRIES = 3
    MAX_L2_RETRIES = 3

    def handle_level_1(
        self,
        *,
        original_prompt: str,
        response_text: str,
        validation_errors: List[str],
        llm_callable,
        retry_index: int,
    ) -> ProtectionResult:
        if retry_index >= self.MAX_L1_RETRIES:
            return ProtectionResult(False, 1, retry_index, validation_errors)

        corrective_prompt = self._build_l1_prompt(
            original_prompt=original_prompt,
            response_text=response_text,
            validation_errors=validation_errors,
            retry_index=retry_index,
        )
        corrected = llm_callable(corrective_prompt)
        return ProtectionResult(False, 1, retry_index + 1, validation_errors, corrected)

    def handle_level_2(
        self,
        *,
        task_bundle: Dict[str, Any],
        failing_tests: List[str],
        traceback_text: str,
        llm_implementer,
        llm_tester,
        retry_index: int,
    ) -> Dict[str, Any]:
        if retry_index >= self.MAX_L2_RETRIES:
            return {"passed": False, "level": 2, "retry_index": retry_index}

        implementer_prompt = self._build_l2_implementer_prompt(
            task_bundle, failing_tests, traceback_text, retry_index
        )
        tester_prompt = self._build_l2_tester_prompt(
            task_bundle, failing_tests, traceback_text, retry_index
        )

        code_json = llm_implementer(implementer_prompt)
        test_json = llm_tester(tester_prompt)
        return {
            "passed": False,
            "level": 2,
            "retry_index": retry_index + 1,
            "code_json": code_json,
            "test_json": test_json,
        }
```

---

### 5.2 JSON extraction and validation skeleton

```python
import json
import re
from pathlib import Path
from jsonschema import validate


JSON_BLOCK_RE = re.compile(r"```json\s*(\{.*?\})\s*```", re.DOTALL)


def extract_single_json_block(text: str) -> dict:
    matches = JSON_BLOCK_RE.findall(text)
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one fenced JSON block, found {len(matches)}")
    return json.loads(matches[0])


def assert_safe_relative_path(path_str: str, root: Path) -> Path:
    path = (root / path_str).resolve()
    if not str(path).startswith(str(root.resolve())):
        raise ValueError(f"Unsafe path detected: {path_str}")
    return path


def validate_payload(payload: dict, schema: dict) -> None:
    validate(instance=payload, schema=schema)
```

---

### 5.3 `computePricing` report skeleton

```python
import csv
import json
from pathlib import Path


def compute_pricing(log_path: Path, csv_path: Path | None = None) -> dict:
    entries = json.loads(log_path.read_text(encoding="utf-8"))

    total = 0.0
    by_stage = {}
    rows = []

    for entry in entries:
        dollars = float(entry["dollars"])
        stage = entry["stage"]
        total += dollars
        by_stage[stage] = by_stage.get(stage, 0.0) + dollars
        rows.append([
            entry["timestamp"],
            stage,
            entry["agent_name"],
            entry["tokens"]["prompt"],
            entry["tokens"]["response"],
            dollars,
        ])

    if csv_path is not None:
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "stage", "agent", "prompt_tokens", "response_tokens", "dollars"])
            writer.writerows(rows)

    return {
        "grand_total": round(total, 6),
        "stage_totals": {k: round(v, 6) for k, v in by_stage.items()},
        "entry_count": len(entries),
    }
```

---

## 6. Test Matrix for the Corrected Areas

These tests should be added immediately because they directly close the criticism.

### 6.1 Protection tests
- `test_l1_retries_stop_after_three_failures`
- `test_l1_does_not_write_files_before_schema_pass`
- `test_l2_retries_stop_after_three_failed_test_cycles`
- `test_l2_requires_regression_test_on_retry`
- `test_l1_and_l2_budgets_are_independent`

### 6.2 Schema tests
- `test_scaffolding_schema_rejects_unknown_top_level_keys`
- `test_scaffolding_schema_rejects_missing_test_instructions`
- `test_code_writing_schema_requires_self_healing_note`
- `test_json_writer_rejects_duplicate_paths`
- `test_json_writer_rejects_path_traversal`

### 6.3 Workflow tests
- `test_workflow_loader_requires_all_mandatory_fields`
- `test_workflow_loader_rejects_invalid_retry_policy`
- `test_scaffolding_yaml_points_to_existing_schema`

### 6.4 Agent tests
- `test_brainstormer_contract`
- `test_reviewer_contract`
- `test_reuse_matcher_reuses_agent_at_or_above_threshold`
- `test_reuse_matcher_creates_stub_below_threshold`

---

## 7. Immediate Implementation Order

To keep this correction pack practical, the next coding order should be exactly this:

1. create JSON Schema files under `schemas/`;
2. implement `json_writer.py` with extraction, schema validation, duplicate-path checks, and safe-path checks;
3. implement `protection_agent.py` with exact retry counters for Level 1 and Level 2;
4. implement `workflow_loader.py` validation for mandatory YAML keys;
5. implement `BrainstormerAgent` and `ReviewerAgent` MVP stubs plus tests;
6. add `computePricing` command and CSV export;
7. add protection, schema, workflow, and agent tests;
8. enforce 80% coverage gate on all newly added modules.

This order matters because it establishes the guardrails before the broader autonomy loops rely on them.

---

## 8. Definition of Done for This Correction Pack

The weaknesses identified by review are considered closed only when all of the following are true:

1. Level 1 and Level 2 retry logic are implemented exactly as specified above.
2. The scaffolding, code-writing, test-generation, documentation, and execution-log schemas exist as concrete files.
3. Workflow YAML files conform to the mandatory contract and at least the two canonical examples exist.
4. BrainstormerAgent and ReviewerAgent exist as concrete MVP classes with tests.
5. The codebase includes at least the provided skeleton-level implementations for protection, JSON handling, and pricing.
6. All new tests pass and coverage on new modules is at or above 80%.

Once these are true, the earlier criticism is no longer valid: the plan is no longer merely architectural, but operational enough to drive implementation directly.
