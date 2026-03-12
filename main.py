# main.py
# Version: 2.0 - Phase 2 with safe start, init_prompt.txt, cost preview, protections

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from core.state_machine import StateMachine, ProjectState
from core.models import Project, CostEstimate
from tools.project_manager import create_project_folder, sanitize_slug
from tools.token_counter import count_tokens, estimate_cost

load_dotenv()
console = Console()

app = typer.Typer(help="Agent Company MVP CLI")

state_machine: Optional[StateMachine] = None
current_project: Optional[Project] = None
current_project_folder: Optional[Path] = None

def load_init_prompt() -> str:
    prompt_path = Path("init_prompt.txt")
    if not prompt_path.exists():
        console.print("[red]Error: init_prompt.txt is missing in the root folder.[/]")
        console.print("Please create it and write your project prompt there.")
        raise typer.Exit(1)
    content = prompt_path.read_text(encoding="utf-8").strip()
    if not content:
        console.print("[red]Error: init_prompt.txt is empty or only whitespace.[/]")
        console.print("Please add your project description.")
        raise typer.Exit(1)
    return content

@app.command()
def start(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Short project name (optional)")
):
    """Start a new project using init_prompt.txt (required)."""
    global state_machine, current_project, current_project_folder

    if state_machine is not None:
        console.print("[yellow]A project is already running. Finish or reset first.[/]")
        return

    prompt = load_init_prompt()

    # Project name logic
    if name:
        project_name = name.strip()
    else:
        project_name = prompt[:50].strip() + "..." if len(prompt) > 50 else prompt.strip()

    console.print(Panel.fit(
        f"[bold]Prompt loaded from init_prompt.txt[/] ({len(prompt)} characters)\n"
        f"[bold]Proposed project name:[/] {project_name}",
        title="New Project Preview",
        border_style="blue"
    ))

    if not Confirm.ask("Proceed with this prompt?", default=True):
        console.print("[yellow]Aborted. No changes made.[/]")
        return

    # ─── Cost preview for FIRST step (ANALYZE) ───────────────────────────────
    console.print("[dim]Preparing cost preview for initial ANALYZE step...[/]")

    temp_project = Project(name=project_name, initial_prompt=prompt)
    temp_sm = StateMachine(project=temp_project)

    # Force transition to ANALYZE for preview purposes
    temp_sm.current_state = ProjectState.IDLE  # reset if needed
    #temp_sm.current_state = ProjectState.ANALYZE  # reset if needed
    preview = temp_sm.preview_next_chunk()

    console.print(Panel.fit(
        f"[bold]First step:[/] ANALYZE (Domain identification)\n"
        f"Input tokens: {preview.input_tokens:,}\n"
        f"Est. output:  {preview.estimated_output_tokens:,}\n"
        f"Est. cost:    ${preview.estimated_cost_usd:.6f}\n"
        f"Model:        {preview.model_used}",
        title="Initial Cost Preview - Approve to Create Project",
        border_style="cyan"
    ))

    if not Confirm.ask("Proceed with this cost and create the project?", default=True):
        console.print("[yellow]Aborted after cost review. No project created.[/]")
        return

    # ─── Only now create folder and finalize ────────────────────────────────
    current_project_folder = create_project_folder(project_name)
    (current_project_folder / "initial_prompt.txt").write_text(prompt, encoding="utf-8")

    current_project = temp_project
    state_machine = temp_sm

    console.print(Panel.fit(
        f"[bold green]Project fully initialized[/]: {project_name}\n"
        f"Folder: {current_project_folder}",
        border_style="green"
    ))

    # Execute the first state (already previewed)
    state_machine.run_current_state()

@app.command()
def status():
    """Show detailed current project status."""
    if current_project is None or state_machine is None:
        console.print("[red]No active project.[/]")
        return

    status_info = state_machine.get_status()
    console.print(Panel.fit(
        f"[bold]Project:[/] {status_info['project_name']}\n"
        f"[bold]Folder:[/] {current_project_folder}\n"
        f"[bold]State:[/] {status_info['current_state']}\n"
        f"[bold]Steps completed:[/] {status_info['history_length']}\n"
        f"[bold]Last action:[/] {status_info['last_state']}",
        title="Project Status",
        border_style="blue"
    ))

@app.command()
def proceed():
    """Advance to the next state after cost preview."""
    global state_machine
    if state_machine is None:
        console.print("[red]No active project.[/]")
        return

    if state_machine.advance():
        console.print("[green]Advanced successfully.[/]")
    else:
        console.print("[yellow]Advance cancelled.[/]")

if __name__ == "__main__":
    app()