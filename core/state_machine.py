# core/state_machine.py
# Version: 5.2 - Implementation Agent integrated (runs on IMPLEMENTED for current projects)

import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from core.models import Project, ProjectState, CostEstimate
from tools.token_counter import count_tokens, estimate_cost
from tools.project_manager import save_project_state

console = Console()

class StateMachine:
    def __init__(self, project: Project, folder: Path):
        self.project = project
        self.folder = folder
        self.current_state = ProjectState.CREATED
        self.history: list[str] = []

        state_file = folder / "state.json"
        if state_file.exists():
            data = json.loads(state_file.read_text())
            old_state = data["current_state"]
            mapping = {
                "IDLE": "CREATED",
                "ANALYZE": "REQUIREMENTS_FORMALIZED",
                "REQUIREMENTS": "REQUIREMENTS_FORMALIZED",
                "CLARIFY": "REQUIREMENTS_FORMALIZED",
                "PLANNING": "PLANNED",
                "IMPLEMENTING": "IMPLEMENTED",   # backward compat for your project2
            }
            self.current_state = ProjectState(mapping.get(old_state, old_state))
            self.history = data.get("history", [])

    def preview_next_chunk(self) -> CostEstimate:
        messages = [
            {"role": "system", "content": "You are starting analysis."},
            {"role": "user", "content": self.project.initial_prompt[:2000]}
        ]
        input_tokens = count_tokens(messages)
        est_output = min(1500, len(self.project.initial_prompt) // 4 + 500)
        cost_usd = estimate_cost(input_tokens, est_output)

        return CostEstimate(
            input_tokens=input_tokens,
            estimated_output_tokens=est_output,
            estimated_cost_usd=cost_usd,
            model_used="xai/grok-3-mini-beta"
        )

    def advance(self) -> bool:
        if self.current_state == ProjectState.COMPLETE:
            console.print("[green]Project already complete.[/]")
            return False

        STATE_FLOW = {
            ProjectState.CREATED: ProjectState.REQUIREMENTS_FORMALIZED,
            ProjectState.REQUIREMENTS_FORMALIZED: ProjectState.PLANNED,
            ProjectState.PLANNED: ProjectState.IMPLEMENTED,
            ProjectState.IMPLEMENTING: ProjectState.IMPLEMENTED,  # for your current project2
            ProjectState.IMPLEMENTED: ProjectState.TESTED,
            ProjectState.TESTED: ProjectState.COMPLETE,
        }
        next_state = STATE_FLOW.get(self.current_state, ProjectState.COMPLETE)

        preview = self.preview_next_chunk()

        console.print(Panel.fit(
            f"[bold]Next step:[/] {next_state.name}\n"
            f"Input tokens: {preview.input_tokens:,}\n"
            f"Est. output:  {preview.estimated_output_tokens:,}\n"
            f"Est. cost:    ${preview.estimated_cost_usd:.6f}",
            title="Cost Preview - Proceed?",
            border_style="cyan"
        ))

        if not Confirm.ask("Proceed with this cost?", default=True):
            console.print("[yellow]Cancelled.[/]")
            return False

        self.transition_to(next_state)
        self.run_current_state()
        save_project_state(self.folder, self.project, self.current_state, self.history)
        return True

    def transition_to(self, new_state: ProjectState):
        console.print(f"[blue]→ {self.current_state.name} → {new_state.name}[/]")
        self.current_state = new_state
        self.history.append(f"Entered {new_state.name}")

    def run_current_state(self):
        console.print(Panel.fit(
            f"[bold green]Executing {self.current_state.name}[/]",
            title="State Execution",
            border_style="green"
        ))

        if self.current_state == ProjectState.REQUIREMENTS_FORMALIZED:
            from agents.requirements_engineer import run_requirements_engineer
            run_requirements_engineer(self.folder, self.project.initial_prompt)
            console.print("[green]✅ Requirements Engineer completed (requirements.json saved)[/]")

        elif self.current_state == ProjectState.PLANNED:
            from agents.planner import run_planner
            req_file = self.folder / "requirements.json"
            if req_file.exists():
                reqs = json.loads(req_file.read_text(encoding="utf-8"))
                run_planner(self.folder, reqs)
            else:
                console.print("[red]requirements.json missing![/]")

        elif self.current_state == ProjectState.IMPLEMENTED:
            from agents.implementer import run_implementer
            req_file = self.folder / "requirements.json"
            plan_file = self.folder / "plan.json"
            if req_file.exists() and plan_file.exists():
                reqs = json.loads(req_file.read_text(encoding="utf-8"))
                plan = json.loads(plan_file.read_text(encoding="utf-8"))
                run_implementer(self.folder, reqs, plan)
            else:
                console.print("[red]Missing requirements or plan![/]")

        else:
            console.print("[dim]→ State execution stub (next phase coming soon)[/]")