# HANDOVER DOCUMENT — asdf Project[](https://github.com/TucaliucVlad/asdf.git)

**Date:** March 12, 2026  
**Status:** FAR OFF from target — major divergences from Master Plan + many regressions introduced during adaptation.  
**Warning to next AI:** **Deep dive required immediately.** Do **NOT** continue with new features until you have read every file, run GIT_FETCH, and re-aligned the entire codebase. We are currently in a broken/messy state.

## 1. Project Purpose (Fixed Core Only)
- Build a **deterministic, protected** AI software engineering pipeline.
- User puts **any** project vision in `init_prompt.txt` (dynamic seed — can be GUI, CLI, web app, anything).
- Pipeline must go: Requirements → Planning → L1-protected Implementation → L2 Tests → COMPLETE.
- All agent outputs **strictly** validated against `/schemas/*.schema.json`.
- L1 (structural) + L2 (pytest) protection with 3 retries each.
- New projects **always** start in `projects/playground/` (gitignored).
- Promote to `projects/shared/` when ready (git-tracked).
- No dynamic projects or old skeletons should interfere with the fixed core.

## 2. Master Plan Reference
- `PROJECT_GENESIS_Master_Plan.md` = the Correction Pack (L1/L2 retries, strict schemas, state machine with all retry states, execution_log.jsonl, etc.).
- We must be 100% compliant before any real project work.

## 3. What Was Implemented So Far (During This Chat)
- Phases 1-6 adaptation to Master Plan (schemas, retry_policy, state_machine, stage_router, orchestrator, agents with LLM calls).
- CLI commands: `start`, `run`, `status`, `list`, `promote`.
- Playground/shared split + `.gitignore` rule.
- Materializer + auto `pip install -r requirements.txt`.
- Basic LLM integration in all 4 agents (requirements_engineer, planner, implementer, tester).
- Some L1 retry loops added.

## 4. Current Critical Issues (We Are FAAAAR Off — Deep Dive Mandatory)
- **Duplicate folders** still appear (`projects/test-project-xxx` + `projects/playground/test-project-xxx`).
- No `req.json` or `plan.json` saved (only `requirements.txt` which is runtime deps, not planning artifact).
- Agents are weak/minimal — they often produce incomplete skeletons (missing full structure, tests, proper planning tasks).
- `requirements.txt` spelling/typos in past generations.
- No real unit tests for orchestrator, agents, or pipeline.
- StateMachine sometimes creates root-level projects despite playground mode.
- L1 exhaustion still happens frequently on complex prompts (GUI apps, etc.).
- Folder structure not enforced (src/, tests/, requirements.txt sometimes missing or wrong).
- No proper plan.json / requirements engineering output saved for debugging.
- Overall quality is worse than before the adaptation phases — mess introduced during LLM + retry integration.

## 5. Next Steps (Priority Order — Do Deep Dive First)
1. **Deep dive** — Run `GIT_FETCH`, read **every** file in repo + `PROJECT_GENESIS_Master_Plan.md` + `HAND_OVER.md`.
2. **Full reset** — Delete all `projects/*`, clean git, re-verify Master Plan alignment.
3. **Strengthen all agents** — Make them generate complete skeletons (requirements.txt + src/ + tests/ + plan.json + req.json) while staying 100% general.
4. **Add real unit tests** for orchestrator, state_machine, retry_policy, and each agent.
5. **Fix duplicates permanently** — Enforce `playground/` only.
6. **Test end-to-end** with a simple + complex prompt (GUI parabola example).
7. **Once clean** — Resume normal development (tester L2 integration, documentation_report, full `run` command).

**Current recommendation to next AI:**  
Start fresh from a clean state. Do **not** add new features until the pipeline reliably produces a complete, runnable project with `req.json`, `plan.json`, correct folder structure, auto-install, and no duplicates — for **any** vision in `init_prompt.txt`.

We are far off. Deep dive first.  
Fix the fundamentals before anything else.

— Grok (current session)