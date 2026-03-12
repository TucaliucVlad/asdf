# main.py
# Version: 3.1 - Fixed load_dotenv + safe loading

import typer
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from typing import Optional
from dotenv import load_dotenv   # ← FIXED: this line was missing

from core.state_machine import StateMachine
from core.models import Project
from tools.project_manager import (
    create_project_folder, get_active_project, set_active_project,
    load_project, save_project_state
)
from tools.token_counter import count_tokens, estimate_cost

# Safe dotenv loading (never crashes)
try:
    load_dotenv()
except Exception as e:
    print(f"[yellow]Warning: Could not load .env ({e}) — continuing anyway[/]")

console = Console()
app = typer.Typer(help="Agent Company MVP CLI")

@app.command()
def start(name: Optional[str] = typer.Option(None, "--name", "-n")):
    """Start new project + auto-activate + first ANALYZE."""
    prompt = Path("init_prompt.txt").read_text(encoding="utf-8").strip()
    project_name = name or prompt[:50].strip() + "..."
    console.print(Panel.fit(f"Prompt loaded ({len(prompt)} chars)\nProposed name: {project_name}", title="New Project Preview", border_style="blue"))
    if not Confirm.ask("Proceed?", default=True):
        return
    # Cost preview (same as before)
    temp_project = Project(name=project_name, initial_prompt=prompt)
    preview = StateMachine(temp_project, Path("/tmp")).preview_next_chunk() # temp for preview
    console.print(Panel.fit(
        f"First step: ANALYZE\nInput: {preview.input_tokens:,}\nEst. cost: ${preview.estimated_cost_usd:.6f}",
        title="Initial Cost Preview", border_style="cyan"
    ))
    if not Confirm.ask("Create project?", default=True):
        return
    folder = create_project_folder(project_name)
    (folder / "initial_prompt.txt").write_text(prompt)
    # Save initial state
    sm = StateMachine(temp_project, folder)
    save_project_state(folder, temp_project, sm.current_state, sm.history)
    set_active_project(folder.name)
    console.print(Panel.fit(f"[bold green]Project {project_name} created & ACTIVE[/]\nFolder: {folder}\n\nRun [bold]proceed[/] for first API call (ANALYZE)", border_style="green"))

@app.command()
def proceed():
    """Advance next step (works in any shell)."""
    slug = get_active_project()
    if not slug:
        console.print("[red]No active project. Use 'start' or 'use <name>' first.[/]")
        return
    project, folder = load_project(slug)
    sm = StateMachine(project, folder)
    if sm.advance():
        console.print("[green]Step completed & state saved.[/]")

@app.command()
def use(slug: str):
    """Switch to another project."""
    if (Path("projects") / slug).exists():
        set_active_project(slug)
    else:
        console.print("[red]Project not found.[/]")

@app.command()
def list():
    """List all projects."""
    projects = [p.name for p in Path("projects").iterdir() if p.is_dir() and not p.name.startswith(".")]
    console.print("[bold]Projects:[/]\n" + "\n".join(f"• {p}" for p in projects) or "None yet")

@app.command()
def status():
    """Show active project status."""
    slug = get_active_project()
    if not slug:
        console.print("[red]No active project.[/]")
        return
    project, folder = load_project(slug)
    sm = StateMachine(project, folder)
    console.print(Panel.fit(
        f"Project: {project.name}\nFolder: {folder}\nState: {sm.current_state.name}\nHistory: {len(sm.history)} steps",
        title="Status", border_style="blue"
    ))

if __name__ == "__main__":
    app()