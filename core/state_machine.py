# core/state_machine.py
# Version: 2.1 - FINAL Phase 2 - clean stub messages + better execution feedback

from core.models import Project, ProjectState, CostEstimate
from tools.token_counter import count_tokens, estimate_cost
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

console = Console()

class StateMachine:
    def __init__(self, project: Project):
        self.project = project
        self.current_state = ProjectState.IDLE
        self.history: list[str] = []

    def transition_to(self, new_state: ProjectState):
        console.print(f"[blue]→ {self.current_state.name} → {new_state.name}[/]")
        self.current_state = new_state
        self.history.append(f"Entered {new_state.name}")

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
            model_used="groq/grok-beta"
        )

    def advance(self) -> bool:
        if self.current_state == ProjectState.COMPLETE:
            console.print("[green]Already complete.[/]")
            return False

        preview = self.preview_next_chunk()
        next_state = ProjectState(self.current_state.value + 1)

        console.print(Panel.fit(
            f"[bold]Next:[/] {next_state.name}\n"
            f"Input tokens: {preview.input_tokens:,}\n"
            f"Est. output:  {preview.estimated_output_tokens:,}\n"
            f"Est. cost:    ${preview.estimated_cost_usd:.6f}",
            title="Next Step Preview",
            border_style="cyan"
        ))

        if not Confirm.ask("Proceed?", default=True):
            console.print("[yellow]Cancelled.[/]")
            return False

        self.transition_to(next_state)
        self.run_current_state()
        return True

    def run_current_state(self):
        console.print(Panel.fit(
            f"[bold green]Executing {self.current_state.name}[/]",
            title="State Execution",
            border_style="green"
        ))

        if self.current_state == ProjectState.REQUIREMENTS and current_project_folder:
            from agents.requirements_engineer import run_requirements_engineer
            reqs = run_requirements_engineer(current_project_folder, self.project.initial_prompt)

        elif self.current_state == ProjectState.PLANNING and current_project_folder:
            from agents.planner import run_planner
            reqs = json.loads((current_project_folder / "requirements.json").read_text())
            run_planner(current_project_folder, reqs)

        else:
            console.print("[dim]→ State execution stub (to be implemented)[/]")

    def get_status(self):
        return {
            "project_name": self.project.name,
            "current_state": self.current_state.name,
            "history_length": len(self.history),
            "last_state": self.history[-1] if self.history else "None"
        }