# Agent Company MVP Handover Document

## Project Overview
**Project Name:** Agent Company MVP  
**Initiation Date:** March 12, 2026  
**Handover Date:** March 12, 2026  
**Handover From:** Grok AI Assistant  
**Handover To:** User/Developer  

This document provides a clear overview of the project's purpose, current progress, and the structured phases required to achieve a Minimum Viable Product (MVP). The goal is to ensure seamless continuation of development for this scalable, self-evolving agent orchestration system.

## Project Purpose
The Agent Company MVP is designed to create a self-bootstrapping, company-like multi-agent orchestration system that transforms vague user prompts (ideas or client requests) into fully implemented, tested, documented, and deployable deliverables. It mimics a real engineering organization, starting from domain analysis and clarification, through requirements engineering, planning, execution, testing, and documentation.

Key objectives:
- **Core Functionality:** Enable deterministic workflows driven by a state machine, with agents handling specific roles (e.g., Analyzer, Planner, Executor, Tester, Documenter).
- **Scalability and Evolution:** Build a "living organism" system that self-improves through controlled evolutionary mechanisms, ensuring safe changes with dependency analysis and regression testing.
- **Multi-LLM Support:** Integrate with various LLM providers (e.g., Grok, OpenAI, Anthropic) via a unified interface, allowing users to configure API keys and route tasks intelligently.
- **User Experience:** Begin as a personal CLI tool for the developer, evolving into a downloadable desktop app (using Tauri or similar) that users can monetize or expand.
- **Robustness:** Incorporate cost previews, budget guardrails, human approval gates, and protections against failures (e.g., missing files, empty prompts) to prevent technical debt and ensure production-grade reliability.
- **Monetization Potential:** Position the system for agency services, pre-built workflows, or a SaaS/desktop app, focusing on scientific, engineering, and app development domains.
- **Long-Term Vision:** A self-replicating, adaptive platform that can build and improve itself, handling massive projects across domains like control engineering, physics, and full-stack apps.

The system emphasizes structure, traceability, and safety to handle complexity without overwhelming the developer.

## What Was Done So Far
Development has focused on establishing a solid foundation with a structured, scalable codebase. Progress includes:

- **Environment Setup (Phase 0):** Created a virtual environment with key dependencies (litellm, pydantic, pyyaml, typer, rich, python-dotenv, gitpython). Configured `.env` for API keys and `.gitignore` for clean repository management.
- **Core Structure and CLI Skeleton (Phase 1):** Implemented the initial folder structure (`core/`, `tools/`, `workflows/`, `prompts/`, `projects/`), state machine basics (enum-based FSM with transitions), Pydantic models for projects and states, LiteLLM wrapper for multi-LLM support, and Typer CLI commands (`start`, `status`, `proceed`, `budget`). Fixed a syntax error related to reserved keyword usage.
- **Testing and Validation:** Ran initial CLI tests in Visual Studio, confirming state transitions, stub executions, and no crashes. The system can start a project, transition to ANALYZE, and display status.
- **Discussions and Planning:** Defined protections (e.g., for missing/empty prompts, cost confirmations), multi-LLM routing, self-evolution concepts, and monetization strategies. Agreed on a robust, additive development approach with JSON/YAML for configurations to ensure scalability.

No LLM calls or file writing occur yet; the focus has been on a clean, debt-free skeleton.

## Phases Necessary for the MVP
The MVP will be a functional CLI tool capable of orchestrating agents to plan, execute, test, and document simple projects (e.g., building a small app from a prompt). Below are the sequential phases, with goals, key deliverables, and success criteria. Each phase builds additively on the previous.

### Phase 2 – Real Cost Preview + State Advancement
**Goal:** Enable accurate token/cost estimation and safe state progression with user confirmations and prompt validations.  
**Key Deliverables:** Updated CLI (`start` reads from `init_prompt.txt`, supports `--name`), project folder creation with protections, real token counting via LiteLLM, cost panels, confirmation gates.  
**Success Criteria:** Running `start` validates prompt file, shows preview, creates folder only on confirmation; `proceed` advances states safely.

### Phase 3 – Requirements Engineer + Planner Agents
**Goal:** Generate structured requirements and detailed plans with tasks, tests, and agent matching.  
**Key Deliverables:** `agents/requirements_engineer.py`, `agents/planner.py`, workflow YAMLs, prompt templates.  
**Success Criteria:** From a prompt, produces `plan.md` with requirements, subtasks, test procedures, and 75% skill matching.

### Phase 4 – Executor + File Writing + Git Integration
**Goal:** Allow independent execution of plans, creating real files and git repos.  
**Key Deliverables:** `agents/executor.py`, file/git tools, sandboxed project folders.  
**Success Criteria:** Executes a simple task to create and commit code files in `projects/`.

### Phase 5 – Tester + Validation Loop
**Goal:** Independently test executed code against planned procedures.  
**Key Deliverables:** `agents/tester.py`, integration with pytest/subprocess.  
**Success Criteria:** Runs tests, reports pass/fail, loops on failures.

### Phase 6 – Documenter + End-to-End Smoke Test
**Goal:** Complete the full cycle with documentation and traceability.  
**Key Deliverables:** `agents/documenter.py`, full-cycle testing.  
**Success Criteria:** End-to-end run produces a working mini-app with code, tests, docs, and git history.

Post-MVP (after Phase 6): Add self-evolution (Phase 7), GUI app building, and monetization features.

## Next Steps for Continuation
- Complete Phase 2 implementations and tests.  
- Use Visual Studio for debugging and refactoring to maintain structure.  
- Track all changes in git for version control.  
- If issues arise, reference this document and conversation history for context.  

This handover ensures the project remains organized and scalable. Contact for any clarifications.