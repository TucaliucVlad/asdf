# PROJECT GENESIS — Complete Planning Document

## 1. Purpose

This document translates the PROJECT GENESIS vision into an executable engineering plan. It turns the high-level concept into:

- a concrete system architecture,
- a deterministic workflow model,
- an implementation roadmap,
- explicit responsibilities per agent,
- measurable test and acceptance criteria,
- operational safeguards for autonomous execution,
- and a staged path from MVP to self-evolving desktop product.

The scope of this plan is intentionally broader and more concrete than the original prompt. The goal is not merely to restate the vision, but to close the missing engineering gaps that would otherwise block implementation.

---

## 2. Mission Definition

PROJECT GENESIS is a local-first, workflow-driven autonomous software factory. It starts from a single user idea and converts that idea into a complete implemented project through a strict sequence of:

1. requirement discovery,
2. domain expansion and clarification,
3. exhaustive requirements synthesis,
4. implementation planning,
5. deterministic execution in task batches,
6. automatic testing,
7. review and gap detection,
8. documentation and cost tracking,
9. safe self-improvement.

The system is CLI-first, state-machine-driven, and workflow-configured via YAML. LLMs do not directly manipulate the repository arbitrarily; they emit structured JSON which is validated and then materialized by deterministic tooling.

The final product evolves into a desktop application with pluggable model providers, monetization primitives, and a safe self-evolution engine.

---

## 3. Guiding Principles

### 3.1 Determinism over improvisation
Every important stage must be represented as an explicit workflow definition and an explicit state in the state machine.

### 3.2 Structured generation only
LLM outputs are never trusted as raw code patches. They must pass through a strict JSON contract and deterministic writers/scaffolders.

### 3.3 Autonomous, but bounded
Autonomy is the default, but protected by hard safety rails:

- maximum three retries per protection level,
- schema validation before file writes,
- test-gated progression,
- immutable logs,
- dependency checks before core changes,
- human approval only where explicitly required.

### 3.4 Total traceability
Every prompt, response, token count, dollar estimate, retry, file write, test run, and review action must be logged.

### 3.5 Self-improvement without regression
The system may improve itself only through the same controlled pipeline it uses for user projects, and only after sandbox validation.

### 3.6 Reusability before proliferation
New agents are created only when existing agents do not meet the reuse threshold. Agent reuse is intentional and measurable.

---

## 4. Product Objectives

## 4.1 Functional objectives
The system must:

- accept a user idea as the initiating prompt,
- decompose the idea across domains and subdomains,
- run a structured clarification loop,
- generate exhaustive requirements,
- create a complete implementation plan with tests and skill requirements,
- execute work in batches,
- generate and run tests automatically,
- self-correct structural and runtime failures,
- produce detailed documentation throughout execution,
- track cost locally before execution and cumulatively after execution,
- compute pricing reports from execution logs,
- support future self-rebuild and desktop packaging.

## 4.2 Non-functional objectives
The system must be:

- deterministic in control flow,
- auditable,
- modular,
- extensible for new workflows and agents,
- safe for self-modification,
- provider-agnostic across LLM backends,
- suitable for local desktop deployment.

---

## 5. System Scope

## 5.1 In scope for the foundation and MVP

- CLI orchestration
- workflow YAML loading and execution
- requirements and planning pipeline
- JSON extraction, validation, and writing
- scaffolding engine
- test generation and pytest execution
- protection loops for malformed outputs and failing code
- execution log and pricing engine
- project-level implementation folders
- documentation tracking
- self-build proof using computePricing

## 5.2 Deferred but planned

- desktop GUI with Tauri/Electron
- multi-provider API key management UI
- credit marketplace and monetization engine
- agent-pack marketplace
- white-label project generation
- automated dependency graphing for self-evolution
- sandbox self-evolution pipeline
- analytics dashboard

---

## 6. Proposed Repository Architecture

This section fills in a missing practical layer: where the components should live.

```text
repo_root/
├─ main.py
├─ requirements.txt
├─ README.md
├─ core/
│  ├─ __init__.py
│  ├─ state_machine.py
│  ├─ workflow_loader.py
│  ├─ workflow_executor.py
│  ├─ execution_context.py
│  ├─ retry_policy.py
│  ├─ stage_router.py
│  └─ coverage_gate.py
├─ agents/
│  ├─ __init__.py
│  ├─ base_agent.py
│  ├─ registry.py
│  ├─ reuse_matcher.py
│  ├─ requirements_engineer.py
│  ├─ brainstormer.py
│  ├─ planner.py
│  ├─ implementer.py
│  ├─ tester.py
│  ├─ reviewer.py
│  ├─ documenter.py
│  ├─ protection_agent.py
│  └─ self_evolution_agent.py
├─ tools/
│  ├─ __init__.py
│  ├─ scaffolder.py
│  ├─ json_writer.py
│  ├─ pricing_engine.py
│  ├─ prompt_builder.py
│  ├─ token_counter.py
│  ├─ log_writer.py
│  ├─ test_runner.py
│  ├─ schema_validator.py
│  ├─ csv_exporter.py
│  └─ dependency_graph.py
├─ workflows/
│  ├─ 01_scaffolding.yaml
│  ├─ 02_code_writing.yaml
│  ├─ 03_testing.yaml
│  ├─ 04_review.yaml
│  └─ 05_documentation.yaml
├─ schemas/
│  ├─ scaffolding.schema.json
│  ├─ code_writing.schema.json
│  ├─ execution_log.schema.json
│  ├─ workflow.schema.json
│  └─ documentation_report.schema.json
├─ projects/
│  └─ <project-id>/
│     ├─ input/
│     ├─ implementation/
│     ├─ docs/
│     ├─ reports/
│     ├─ logs/
│     │  └─ execution_log.json
│     ├─ tests/
│     └─ artifacts/
├─ tests/
│  ├─ unit/
│  ├─ integration/
│  ├─ regression/
│  └─ fixtures/
└─ scripts/
   ├─ bootstrap.sh
   ├─ run_tests.sh
   └─ export_pricing.sh
```

This structure separates orchestration, agents, tools, schemas, workflows, and per-project outputs. It also gives a clean path for later desktop wrapping without disturbing the engine.

---

## 7. Core Domain Model

A missing requirement in the prompt is a formal domain model. The following entities should exist explicitly in code and/or schema.

## 7.1 Project
Represents one autonomous build initiated from one client prompt.

Suggested fields:

- `project_id`
- `project_name`
- `created_at`
- `status`
- `client_prompt`
- `autonomous`
- `current_stage`
- `active_workflow`
- `requirements_version`
- `plan_version`
- `repo_root`
- `implementation_root`
- `execution_log_path`

## 7.2 Agent Definition
Represents a reusable agent capability.

Suggested fields:

- `agent_id`
- `agent_name`
- `agent_role`
- `description`
- `skills`
- `model_preferences`
- `supported_workflows`
- `history_path`
- `reuse_score_metadata`

## 7.3 Task
Represents a unit of planned work.

Suggested fields:

- `task_id`
- `requirement_id`
- `title`
- `description`
- `batch_id`
- `dependencies`
- `owner_agent`
- `skills_required`
- `files_expected`
- `tests_required`
- `acceptance_criteria`
- `status`

## 7.4 Workflow Definition
Loaded from YAML.

Suggested fields:

- `workflow_id`
- `name`
- `stage`
- `model`
- `prompt_template`
- `max_tokens`
- `input_schema`
- `output_schema`
- `success_criteria`
- `test_procedure`
- `retry_policy`
- `handoff_rules`

## 7.5 Execution Log Entry
The execution log must be append-only and structured.

Suggested fields:

- `timestamp`
- `project_id`
- `stage`
- `workflow_id`
- `agent_name`
- `attempt_number`
- `retry_level`
- `prompt_full`
- `response_full`
- `prompt_tokens`
- `response_tokens`
- `total_tokens`
- `usd_cost`
- `action_type`
- `action_status`
- `files_written`
- `tests_run`
- `tests_passed`
- `tests_failed`
- `error_summary`
- `duration_ms`

## 7.6 Documentation Record
Tracks why a piece of documentation exists.

Suggested fields:

- `doc_id`
- `related_task_id`
- `created_by_agent`
- `artifact_type`
- `purpose`
- `consumer`
- `storage_path`
- `summary`
- `commit_message_candidate`

---

## 8. Agent Architecture

The original prompt names multiple agent roles but does not fully define their contracts. This section closes that gap.

## 8.1 Requirements Engineer Agent
### Responsibilities
- parse the client prompt,
- identify primary domains and subdomains,
- synthesize domain-specific interpretations,
- formulate clarification questions,
- decide when clarification is sufficient,
- produce the exhaustive requirements document,
- review the planner’s plan for full coverage.

### Inputs
- client prompt,
- brainstorm outputs,
- prior clarification answers,
- repository and system context.

### Outputs
- domain map,
- clarification list,
- complete requirements document,
- plan review decision.

### Acceptance criteria
- every major domain activated by the idea is represented,
- requirements are testable and implementation-linked,
- no ambiguous “nice to have” statements remain unclassified.

## 8.2 Brainstormer Agents
Multiple agents working in parallel.

### Responsibilities
- propose completions,
- identify missing adjacent domains,
- surface implementation risks,
- produce clarification prompts,
- propose architecture alternatives.

### Acceptance criteria
- output is additive, not repetitive,
- each brainstorm contribution either clarifies, expands, or derisks.

## 8.3 Planner Agent
### Responsibilities
- transform requirements into tasks and batches,
- define tests for each task,
- define required skills,
- perform agent reuse matching,
- create new agent stubs when needed,
- plan resource and dependency sequencing.

### Acceptance criteria
- every requirement maps to at least one task,
- every task has acceptance criteria and tests,
- traceability requirement-to-task is complete.

## 8.4 Implementer Agent
### Responsibilities
- generate JSON-only code change proposals,
- include file intent and test instructions,
- embed try-except logic where appropriate,
- keep implementation within the task scope.

### Acceptance criteria
- valid JSON,
- files align to intent,
- generated code is testable and bounded.

## 8.5 Tester Agent
### Responsibilities
- generate pytest tests from task intent and acceptance criteria,
- add regression tests when failures occur,
- ensure tests are isolated and deterministic.

### Acceptance criteria
- tests meaningfully validate the requirement,
- regression tests capture prior failures,
- flaky tests are rejected or repaired.

## 8.6 Reviewer Agent
### Responsibilities
- inspect batch outputs,
- verify requirement coverage,
- detect omissions or shallow implementations,
- approve progression or send back gaps.

### Acceptance criteria
- evidence-based decisions tied to requirements,
- no progression on partial coverage.

## 8.7 Documenter Agent
### Responsibilities
- maintain documentation records,
- explain why artifacts were created,
- produce per-task reports,
- prepare git-friendly change summaries,
- support auditability and later onboarding.

### Acceptance criteria
- every significant task has a report,
- reports describe purpose, method, result, and impact.

## 8.8 Protection Agent
### Responsibilities
- handle malformed or schema-invalid responses,
- handle runtime and test failures,
- enforce bounded retries,
- escalate or fail safely after retry exhaustion.

### Levels
- **Level 1:** format/schema/parsing failure
- **Level 2:** runtime/test failure

### Acceptance criteria
- corrective prompts are scoped narrowly,
- retries do not mutate validated content unnecessarily,
- failure reason remains traceable.

## 8.9 Self-Evolution Agent
### Responsibilities
- analyze post-delivery execution history,
- inspect dependency graph,
- propose bounded improvements,
- run changes in sandbox,
- escalate for approval on core modifications.

### Acceptance criteria
- no direct unsafe mutation of core without approval,
- all changes go through full pipeline.

---

## 9. Agent Reuse and Matching Policy

The prompt references a 75 percent reuse threshold. This requires a concrete scoring method.

## 9.1 Proposed reuse score formula
For each candidate agent, compute a weighted score:

- role similarity: 30%
- skill overlap: 30%
- workflow overlap: 20%
- historical success on similar tasks: 10%
- domain familiarity: 10%

`reuse_score = weighted sum * 100`

## 9.2 Reuse rule
- `>= 75`: reuse existing agent
- `< 75`: create new stub agent

## 9.3 New stub agent initialization
When creating a new stub:

- generate `agent_id`
- assign role and skill profile
- create history file
- link candidate workflows
- initialize with zero-shot or example-driven prompt profile

## 9.4 Required implementation detail
The planner must record in the plan:

- all candidate agents evaluated,
- reuse score breakdown per candidate,
- final reuse/create decision.

---

## 10. Workflow System Design

The entire engine depends on workflow YAML files. Their schema must be uniform.

## 10.1 Required YAML fields
Each workflow YAML must contain at minimum:

```yaml
workflow_id: string
name: string
stage: string
description: string
model: string
max_tokens: integer
prompt_template: string
input_contract:
  required_fields: []
output_contract:
  schema_ref: string
success_criteria: []
test_procedure: []
retry_policy:
  max_retries: 3
  protection_level: level1|level2|mixed
handoff_rules:
  next_on_success: string
  next_on_failure: string
telemetry:
  log_prompt: true
  log_response: true
  log_tokens: true
  log_cost: true
```

## 10.2 Mandatory workflows for Phase 2
Exactly five files:

1. `01_scaffolding.yaml`
2. `02_code_writing.yaml`
3. `03_testing.yaml`
4. `04_review.yaml`
5. `05_documentation.yaml`

## 10.3 Execution semantics
The state machine must:

- load workflows from the folder dynamically,
- validate YAML against workflow schema,
- register corresponding executable stages,
- reject startup if mandatory workflows are missing or invalid.

---

## 11. State Machine Design

The state machine is described in the prompt as immense, but that is not actionable until formalized.

## 11.1 Minimum state set for MVP

- `INIT`
- `LOAD_PROJECT`
- `LOAD_WORKFLOWS`
- `PRICE_PREVIEW`
- `REQUIREMENTS_ANALYSIS`
- `BRAINSTORMING`
- `CLARIFICATION`
- `REQUIREMENTS_FINALIZATION`
- `PLANNING`
- `PLAN_REVIEW`
- `SCAFFOLDING`
- `CODE_WRITING`
- `TESTING`
- `REVIEW_BATCH`
- `DOCUMENTATION`
- `PROTECTION_LEVEL_1`
- `PROTECTION_LEVEL_2`
- `BATCH_COMPLETE`
- `PROJECT_COMPLETE`
- `SELF_EVOLUTION_PENDING`
- `FAILED`

## 11.2 Required transitions
Examples:

- `LOAD_WORKFLOWS -> PRICE_PREVIEW`
- `PRICE_PREVIEW -> REQUIREMENTS_ANALYSIS`
- `CLARIFICATION -> REQUIREMENTS_FINALIZATION` when clarity threshold reached
- `CODE_WRITING -> TESTING` after valid JSON write
- `TESTING -> REVIEW_BATCH` if green
- `TESTING -> PROTECTION_LEVEL_2` if red
- `CODE_WRITING -> PROTECTION_LEVEL_1` on malformed JSON
- `REVIEW_BATCH -> CODE_WRITING` if gaps detected
- `REVIEW_BATCH -> PROJECT_COMPLETE` when all tasks complete

## 11.3 Clarification completion policy
The prompt implies either the user or an autonomous decider ends the clarification loop. This should be made explicit.

Proposed rule:

Clarification exits when all conditions are true:

- all critical ambiguities classified as resolved or assumed,
- requirements engineer confidence score >= threshold,
- no unresolved ambiguity blocks planning,
- maximum clarification cycles not exceeded.

## 11.4 Retry semantics
All yes/no prompts are replaced by internal control rules:

- each correction loop max 3 retries,
- after 3 failures, route to `FAILED` or `ESCALATION_REQUIRED`,
- all retries logged with cause and delta.

---

## 12. LLM Interaction Contract

A critical engineering gap in systems like this is prompt contract drift. The contract should be fixed.

## 12.1 General contract
For any file-generating stage, the LLM must return exactly one fenced JSON block and no prose outside it.

## 12.2 Scaffolding response contract
Minimum fields:

```json
{
  "project_name": "string",
  "folders": ["path1", "path2"],
  "files": [
    {
      "path": "relative/path.py",
      "content": "full file content",
      "intent": "why this file exists",
      "test_instructions": ["instruction 1", "instruction 2"]
    }
  ]
}
```

## 12.3 Code writing response contract
Minimum fields:

```json
{
  "task_batch_id": "string",
  "files": [
    {
      "path": "relative/path.py",
      "content": "full file content",
      "intent": "purpose",
      "test_instructions": ["tests to create"]
    }
  ],
  "self_healing_note": "what try-except protection was added and why"
}
```

## 12.4 Validation rules
The `json_writer` must reject outputs that:

- are missing the fenced JSON block,
- contain invalid JSON,
- violate schema,
- attempt path traversal,
- include duplicate paths with conflicting content,
- omit mandatory fields,
- exceed configured file limits.

---

## 13. Logging and Cost Tracking

The execution log is not a side utility. It is part of the core control plane.

## 13.1 Log location
`projects/<project-id>/logs/execution_log.json`

## 13.2 Log policy
- append-only,
- never rewritten in-place except safe append operation,
- log creation at project start,
- each event logged as a structured record.

## 13.3 Events that must be logged
- state transitions,
- LLM calls,
- token counts,
- cost estimates,
- file writes,
- schema validation failures,
- retry invocations,
- pytest executions,
- review decisions,
- documentation report creation,
- pricing report generation,
- self-evolution proposals.

## 13.4 computePricing command
Command:

```bash
python main.py computePricing <project-id> [--csv]
```

Expected outputs:

- per interaction pricing,
- grouped totals by stage,
- grouped totals by workflow,
- grouped totals by agent,
- grand total,
- optional CSV export.

## 13.5 Token/cost engine requirements
Use local tokenization only:

- `tiktoken` for token counting,
- `tokencost` for pricing map or pricing calculation support.

The engine must support model-aware pricing tables and versioned pricing metadata so historical logs remain interpretable even after pricing changes.

---

## 14. Testing Strategy

The prompt asks for tests but does not define the quality bar deeply enough. This plan does.

## 14.1 Test categories
### Unit tests
Validate individual modules and classes.

### Integration tests
Validate interactions across state machine, workflow loader, JSON writer, scaffolder, and log writer.

### Regression tests
Lock in fixes after failures.

### End-to-end tests
Simulate a small project creation and one execution batch.

## 14.2 Mandatory Phase 2 test files
At minimum:

- `test_state_machine.py`
- `test_scaffolder.py`
- `test_json_writer.py`
- `test_protection_agent.py`
- `test_pricing_engine.py`

## 14.3 Additional recommended tests
- `test_workflow_loader.py`
- `test_retry_policy.py`
- `test_log_writer.py`
- `test_compute_pricing_command.py`
- `test_schema_validator.py`
- `test_path_safety.py`

## 14.4 Coverage target
- `>= 80%` on all new code
- no critical module under `70%`
- branch coverage enabled where practical for protection loops

## 14.5 Test execution policy
Pytest must run:

- after each generated batch,
- after each level 2 correction,
- after self-build phase,
- after self-evolution sandbox proposal.

---

## 15. Protection and Self-Healing Design

This system will fail often during development unless recovery is precise. The prompt names two levels; this plan defines them.

## 15.1 Level 1: format/protocol failures
Triggers:

- malformed JSON,
- missing required fields,
- invalid fence extraction,
- workflow output violating schema.

Response:

- build corrective prompt,
- preserve original intent and content request,
- request structure-only correction,
- retry same task up to 3 times,
- log each retry as level 1.

## 15.2 Level 2: runtime/test failures
Triggers:

- pytest failures,
- import errors,
- syntax/runtime exceptions,
- deterministic acceptance failure.

Response:

- attach failing tests and error trace,
- notify Implementer and Tester workflows,
- regenerate implementation and/or tests,
- require permanent regression test,
- retry up to 3 times,
- log each retry as level 2.

## 15.3 Failure exhaustion policy
After 3 retries:

- mark task batch as failed,
- write failure summary,
- stop autonomous progression for that project unless failure policy explicitly allows skip,
- do not silently continue.

---

## 16. Detailed Phase-by-Phase Planning

# Phase 0 — Preparatory Architecture Decisions

This phase is not named in the prompt but is necessary before Phase 2 can be executed safely.

## Objectives
- freeze architecture conventions,
- define schemas,
- define repository layout,
- define coding standards,
- define log contract.

## Deliverables
- architecture decision record,
- JSON schemas,
- workflow schema,
- log schema,
- coding standard doc.

## Acceptance criteria
- all later phases can implement against stable contracts.

---

# Phase 1 — Requirements Consolidation and Plan Freeze

This is conceptually upstream of the build phases.

## Objectives
- turn the project prompt into implementation requirements for the Genesis engine itself,
- identify missing assumptions,
- define MVP boundaries,
- approve architecture baseline.

## Key outputs
- Genesis engine requirements document,
- domain decomposition,
- gap analysis,
- implementation roadmap.

## Risks addressed
- overbuilding too early,
- mixing long-term product with short-term core engine,
- unclear success criteria.

---

# Phase 2 — Core Infrastructure (3 to 4 days)

This must be built first.

## 16.2.1 Objectives
- install foundational dependencies,
- create core tools,
- create test harness,
- make workflows loadable,
- make state machine capable of deterministic execution,
- add cost tracking and pricing report generation.

## 16.2.2 Work packages

### WP2.1 Dependency update
Update `requirements.txt` with:

- `pytest>=8`
- `tiktoken`
- `tokencost`

Recommended additions for robustness:

- `pyyaml`
- `jsonschema`
- `pytest-cov`
- `pydantic` or equivalent schema helper, if compatible with repo style

### WP2.2 Test infrastructure
Create root `tests/` and organize into:

- `tests/unit`
- `tests/integration`
- `tests/regression`
- `tests/fixtures`

### WP2.3 Implement tools/scaffolder.py
Required behavior:

- accepts `project_id` and validated scaffolding dictionary,
- creates `projects/<project-id>/implementation/` tree,
- creates nested folders first,
- writes files exactly as specified,
- refuses unsafe paths,
- returns materialization report.

### WP2.4 Implement tools/json_writer.py
Required behavior:

- extracts fenced JSON block,
- validates schema,
- validates safe paths,
- writes via scaffolder or file writer,
- appends execution record.

### WP2.5 Implement tools/protection_agent.py
Required behavior:

- expose `handle_level_1(...)`
- expose `handle_level_2(...)`
- build corrective prompts,
- enforce 3-retry max,
- emit retry logs and summaries.

### WP2.6 Implement tools/pricing_engine.py
Required behavior:

- token count prompt and response locally,
- map model to price,
- compute exact estimated USD cost,
- return per-message and total cost object,
- support command reuse for computePricing.

### WP2.7 Populate workflows folder
Create exactly five YAML files.

Each must include:

- full prompt template,
- model,
- max tokens,
- success criteria,
- test procedure,
- interconnect rules.

### WP2.8 Update core/state_machine.py
Required changes:

- auto-load workflows,
- register stages,
- add states:
  - scaffolding,
  - code writing,
  - testing,
  - review batch,
  - protection level 1,
  - protection level 2,
- replace yes/no prompts with internal retry logic.

### WP2.9 Update main.py
Required changes:

- add `--autonomous` flag default true,
- add `computePricing` command,
- create fresh append-only execution log at project start.

### WP2.10 Run and pass tests
Required:

- run all new unit tests,
- confirm passing state,
- confirm coverage >=80% on new code.

## 16.2.3 Test procedures
For each module:

- nominal case
- invalid input case
- boundary case
- append-only logging verification
- retry exhaustion verification
- pricing calculation correctness

## 16.2.4 Acceptance criteria
Phase 2 is complete only if:

- mandatory workflows load automatically,
- execution log is created for new project,
- pricing engine returns deterministic output,
- protection loops work with capped retries,
- scaffolder and JSON writer pass tests,
- `computePricing` outputs full priced report,
- coverage target reached.

---

# Phase 3 — Stage 1 Project Scaffolding (2 days)

## 16.3.1 Objectives
- make the first real project generation stage operational,
- convert requirements/planning outputs into an implementation folder automatically.

## 16.3.2 Work packages

### WP3.1 Requirements analysis execution
Requirements Engineer:

- analyze prompt,
- identify domains/subdomains,
- select appropriate agent set,
- define scaffolding intent.

### WP3.2 Strict JSON scaffolding prompt
Build prompt templates with:

- system message forcing JSON only,
- examples of valid/invalid outputs,
- schema reminders,
- no prose rule.

### WP3.3 JSON validation and scaffolding materialization
Flow:

1. LLM returns scaffolding JSON.
2. `json_writer` extracts and validates.
3. `scaffolder` creates folders/files.
4. log entry appended.
5. Documenter records scaffold purpose.

### WP3.4 Level 1 protection integration
If malformed:

- trigger level 1,
- attempt structure-only repair up to 3 times,
- fail visibly if exhausted.

### WP3.5 Completion signaling
State machine marks `SCAFFOLDING_COMPLETE` and routes forward.

## 16.3.3 Acceptance criteria
- strict JSON-only scaffolding accepted,
- folder tree created correctly,
- every file has intent and test instructions,
- exact cost logged,
- malformed JSON triggers level 1 immediately.

---

# Phase 4 — Stage 2 Code Writing + Self-Healing + Testing + Review (5 to 7 days)

This is the core execution engine.

## 16.4.1 Objectives
- implement batch-based execution,
- automatically generate tests,
- recover from structural and runtime failures,
- ensure review closes requirement gaps.

## 16.4.2 Work packages

### WP4.1 Batch planner
Planner must output batches of 5 to 10 tasks.

Each task must include:

- requirement trace ID,
- title,
- description,
- dependencies,
- files expected,
- tests expected,
- skills required,
- acceptance criteria.

### WP4.2 Implementer JSON output
Implementer must produce JSON only with:

- files,
- content,
- intent,
- test instructions,
- self-healing note.

### WP4.3 File materialization
`json_writer` writes to `implementation/`.

### WP4.4 Tester generation
Tester reads file intents and creates pytest tests in project tests folder.

### WP4.5 Automatic pytest execution
Pytest runs after each batch. Results are captured in execution log.

### WP4.6 Level 2 protection loop
On test failure:

- pass failing tests and traces back to Implementer and Tester,
- regenerate only affected outputs,
- add permanent regression tests,
- repeat until green or retry limit reached.

### WP4.7 Reviewer gap analysis
Reviewer maps completed outputs back to original requirements.

If any requirement is incompletely covered:

- add missing tasks back to Planner,
- do not advance as complete.

### WP4.8 Documentation generation
Per task, Documenter produces:

- purpose,
- files changed,
- method,
- tests executed,
- result,
- possible commit summary.

## 16.4.3 Batch execution cycle
Canonical cycle:

1. select batch
2. build code-writing prompt
3. get JSON output
4. validate/write files
5. generate tests
6. run pytest
7. protect and heal if needed
8. review for completeness
9. document
10. advance to next batch

## 16.4.4 Acceptance criteria
Phase 4 is complete when:

- all planned tasks are executed,
- all tests pass,
- all failures are either fixed or explicitly failed after retry exhaustion,
- reviewer signs off coverage,
- documentation exists for every batch and task,
- execution log contains complete trace.

---

# Phase 5 — First Self-Build + Polish (3 days)

This phase validates the central thesis: version 1 can safely improve itself.

## 16.5.1 Objectives
- use the system to modify its own codebase,
- validate the pricing engine against the self-build itself,
- improve UX visibility for spend reporting.

## 16.5.2 Mandatory scenario
Feed this task through the full pipeline:

- “Add the computePricing command to main.py”

Even if already present from earlier implementation, treat this as a formal self-build validation scenario by either:

- implementing missing pieces, or
- reconstructing the feature through the pipeline in sandbox and verifying identical result.

## 16.5.3 Work packages

### WP5.1 Self-build project instance
Create internal project instance for the self-build.

### WP5.2 Full stage 1 + stage 2 execution
Run the exact scaffolding/code/testing/review workflow on the system’s own repo or sandbox fork.

### WP5.3 Full repo test run
Run complete pytest suite with coverage.

### WP5.4 Status command enhancement
Update `status` command to show:

- live spend so far,
- estimated remaining cost.

### WP5.5 Project report generation
Documenter generates end-to-end project report.

### WP5.6 Pricing verification
Use `computePricing` to verify the self-build cost report includes the self-build interactions.

## 16.5.4 Acceptance criteria
- self-build runs through the same pipeline used for clients,
- repo passes full test suite,
- coverage >=80% on target code,
- pricing report includes self-build costs accurately,
- status command surfaces spend data.

---

# Phase 6 — Self-Evolution Engine

## 16.6.1 Objectives
- move from one-shot self-build to controlled recurring self-improvement.

## 16.6.2 Work packages

### WP6.1 Execution-log-driven analysis
Self-Evolution Agent reads logs and identifies recurring inefficiencies, failure clusters, and high-cost hotspots.

### WP6.2 Dependency graph construction
Use static analysis to build dependency graph.

Targets:

- imports,
- workflow dependencies,
- agent-to-tool dependencies,
- critical core files.

### WP6.3 Improvement proposal generation
Agent proposes changes in the same JSON output format as normal implementation.

### WP6.4 Sandbox validation
All proposals execute in sandbox project first.

### WP6.5 Core-file approval rule
Human approval required only when proposal touches core files such as:

- `main.py`
- `core/state_machine.py`
- security-critical config
- pricing logic affecting billing accuracy

### WP6.6 Safe apply
Only after green tests and review sign-off can proposal apply to mainline.

## 16.6.3 Acceptance criteria
- self-evolution never bypasses standard pipeline,
- sandbox verification is mandatory,
- dependency graph reviewed before any core mutation.

---

# Phase 7 — Desktop Productization

## 16.7.1 Objectives
- wrap the CLI engine in a distributable desktop app,
- maintain exact orchestration semantics.

## 16.7.2 Technology choice
Preferred order:

1. **Tauri** for lighter footprint and better native distribution,
2. **Electron** if team expertise or plugin ecosystem justifies it.

## 16.7.3 Desktop feature scope
- project creation UI,
- API key configuration per model provider,
- live workflow visualization,
- spend dashboard,
- execution log viewer,
- one-click self-rebuild button,
- marketplace browsing surface.

## 16.7.4 Acceptance criteria
- desktop app uses same backend orchestration,
- no second orchestration logic duplicated in UI layer.

---

# Phase 8 — Monetization Layer

This should not block the core engine, but the architecture must not preclude it.

## 16.8.1 Objectives
- introduce revenue primitives without disturbing core execution safety.

## 16.8.2 Features
- freemium desktop tier,
- credit system,
- 20% platform cut,
- agent-pack marketplace,
- white-label generator,
- analytics dashboard.

## 16.8.3 Architectural requirement
Billing, credits, and marketplace logic must be layered above orchestration, not mixed into core execution control.

## 16.8.4 Acceptance criteria
- spend tracking from execution logs can feed billing,
- provider-agnostic orchestration remains intact.

---

## 17. Planner Output Specification

The Planner is central and must produce more than a generic task list.

## 17.1 Required plan sections
The Planner’s output should include:

1. requirement trace matrix
2. task decomposition
3. task dependency graph
4. test plan by task
5. skill matrix by phase
6. agent reuse analysis
7. resource and model selection rationale
8. batch schedule
9. risk register
10. acceptance gate per phase

## 17.2 Skill planning requirement
The prompt states “often 12 or more skills per phase.”

Representative skills to track:

- Python architecture
- JSON schema design
- YAML workflow design
- CLI engineering
- state machine design
- prompt engineering
- LLM output validation
- pytest authoring
- regression testing
- logging and observability
- token accounting
- pricing/billing logic
- file system safety
- sandboxing
- dependency analysis
- desktop packaging
- security review
- technical documentation

---

## 18. Requirements Traceability Matrix

A traceability system is mandatory for coverage claims.

## 18.1 Matrix structure
Each requirement must map to:

- planner task IDs,
- implementation files,
- test files,
- review evidence,
- documentation report IDs.

## 18.2 Example columns
- `requirement_id`
- `requirement_text`
- `phase`
- `task_ids`
- `file_paths`
- `test_paths`
- `review_status`
- `doc_ids`

## 18.3 Completion rule
A requirement is complete only if:

- implementation exists,
- tests pass,
- reviewer approves,
- documentation exists.

---

## 19. Data Contracts and Schemas

The project will become fragile without early schema formalization.

## 19.1 Mandatory schemas
- scaffolding output schema
- code-writing output schema
- workflow YAML schema
- execution log entry schema
- documentation report schema
- pricing report schema
- agent definition schema
- plan task schema

## 19.2 Validation layer
Use schema validation at all important boundaries:

- LLM output -> JSON writer
- workflow YAML -> workflow loader
- execution log append -> log writer
- pricing report generation -> exporter

---

## 20. CLI Design

The original vision is CLI-centered. The CLI should be explicit and composable.

## 20.1 Recommended commands
```bash
python main.py createProject "<client prompt>" [--project-id X] [--autonomous true]
python main.py status <project-id>
python main.py computePricing <project-id> [--csv]
python main.py runStage <project-id> <stage>
python main.py runAll <project-id>
python main.py showLog <project-id>
python main.py reviewPlan <project-id>
python main.py sandboxEvolve <project-id>
```

## 20.2 CLI rules
- deterministic outputs,
- machine-readable option where relevant,
- no unnecessary interactive confirmation after initial approval.

---

## 21. Documentation System Design

The Documenter is not merely a markdown writer. It is a traceability subsystem.

## 21.1 Documentation outputs
For each small task:

- task report markdown,
- commit summary suggestion,
- artifact rationale record,
- dependency/impact note if relevant.

## 21.2 Storage recommendation
Inside `projects/<project-id>/docs/`:

```text
/docs/
  /requirements/
  /planning/
  /batch_reports/
  /task_reports/
  /reviews/
  /pricing/
```

## 21.3 Acceptance criteria
- every batch documented,
- every significant file change attributable,
- reports usable for git history or release notes.

---

## 22. Risk Register

## 22.1 Technical risks
### Risk: prompt drift causes invalid JSON
Mitigation:
- schema-aware prompting,
- few-shot valid/invalid examples,
- level 1 retries.

### Risk: tests become weak and self-confirming
Mitigation:
- reviewer inspects test adequacy,
- regression test requirement,
- intent-derived test generation with acceptance criteria anchors.

### Risk: state machine complexity becomes unmanageable
Mitigation:
- explicit state enum,
- transition table,
- transition tests.

### Risk: cost estimates become inaccurate over time
Mitigation:
- versioned model pricing metadata,
- pricing snapshot stored in logs.

### Risk: unsafe self-modification
Mitigation:
- sandbox first,
- dependency graph check,
- core-file approval.

### Risk: runaway retry loops
Mitigation:
- max three retries,
- hard fail after exhaustion.

### Risk: agent sprawl
Mitigation:
- 75% reuse policy,
- registry and scoring.

## 22.2 Product risks
### Risk: monetization pollutes core architecture too early
Mitigation:
- isolate commercial layer above orchestration.

### Risk: desktop wrapper duplicates logic
Mitigation:
- keep CLI engine as single source of orchestration truth.

---

## 23. Security and Safety Considerations

## 23.1 File safety
- reject path traversal (`../`),
- restrict writes to project implementation roots,
- protect core repo paths unless explicitly allowed.

## 23.2 Log sensitivity
Logs contain full prompts and responses. Therefore:

- define local storage policy,
- consider redaction strategy for secrets,
- never store raw API keys in logs.

## 23.3 Execution safety
- generated code should not auto-execute outside test harness,
- sandbox self-evolution changes,
- isolate destructive file operations.

## 23.4 Provider abstraction safety
- API keys stored securely,
- provider choice separated from workflow logic.

---

## 24. Recommended Implementation Order Inside Each Phase

This ordering reduces rework.

## 24.1 Build order for Phase 2
1. schemas
2. log writer
3. pricing engine
4. scaffolder
5. JSON writer
6. workflow schema + loader
7. state machine updates
8. main.py CLI updates
9. tests
10. coverage gate

## 24.2 Build order for Phase 4
1. planner batch format
2. implementer JSON prompt contract
3. tester generation
4. pytest runner integration
5. protection level 2 loop
6. reviewer coverage check
7. documenter outputs

## 24.3 Build order for self-evolution
1. dependency graph
2. sandbox orchestration
3. proposal generation
4. core-file approval handling
5. apply pipeline

---

## 25. Definition of Done

A phase is done only if all are true:

- implementation completed,
- automated tests passing,
- coverage target met,
- reviewer approves requirement coverage,
- documentation written,
- execution log complete,
- pricing data recoverable.

A project is done only if all requirements in the traceability matrix are closed.

---

## 26. Gaps Resolved by This Planning Document

The original prompt had strong vision but left several engineering ambiguities. This plan resolves them by explicitly defining:

- repository structure,
- domain entities,
- agent contracts,
- reuse scoring method,
- workflow schema,
- state machine states and transitions,
- JSON contracts,
- execution log schema,
- testing taxonomy,
- failure exhaustion rules,
- CLI command set,
- documentation storage strategy,
- self-evolution gating,
- security boundaries,
- implementation ordering.

These are necessary to turn the prompt into an executable build program instead of a conceptual manifesto.

---

## 27. Immediate Next Actions

If this plan is used as the execution baseline, the next concrete steps should be:

1. freeze the repository structure,
2. define schemas under `schemas/`,
3. implement Phase 2 foundational modules,
4. create all mandatory tests,
5. validate workflow loader and state transitions,
6. run first end-to-end scaffolding scenario,
7. begin Stage 2 batch execution framework,
8. validate with Phase 5 self-build scenario.

---

## 28. Final Assessment

PROJECT GENESIS is feasible, but only if treated as a constrained orchestration engine rather than a vague autonomous coding system. The prompt already contains the right strategic concepts:

- requirements-first execution,
- planner-reviewed implementation,
- deterministic workflows,
- bounded self-healing,
- exhaustive logging,
- eventual self-evolution.

The highest-risk areas are not model capability, but orchestration correctness, schema discipline, coverage integrity, and self-modification safety. This plan addresses those directly.

A sensible delivery strategy is:

- first build a strict local CLI engine,
- then validate it on self-build use cases,
- then wrap it in desktop UX,
- only then add monetization and full self-evolution.

That path preserves engineering discipline while staying aligned with the original living-organism vision.
