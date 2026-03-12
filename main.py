import typer
from core.orchestrator import Orchestrator
from core.state_machine import StateMachine
from pathlib import Path
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

@app.command()
def start(project_id: str):
    """Start NEW project in playground/ (ignored by git)."""
    Orchestrator(project_id, mode="playground").run_full_pipeline()

@app.command()
def run(project_id: str):
    """Run full protected pipeline."""
    Orchestrator(project_id).run_full_pipeline()

@app.command()
def status(project_id: str):
    """Show state — NEVER creates project."""
    for mode in ["playground", "shared"]:
        if StateMachine.exists(project_id, mode):
            sm = StateMachine(project_id, mode)
            console.print(f"[bold green]Project[/] {project_id} ([cyan]{mode}[/]) → [bold]{sm.current_state.name}[/]")
            return
    console.print(f"[red]Project {project_id} not found[/]")

@app.command()
def list():
    """Nice table of ALL projects with state."""
    table = Table(title="Projects Overview")
    table.add_column("Project ID", style="cyan")
    table.add_column("Location", style="magenta")
    table.add_column("State", style="green")
    table.add_column("Total Cost", style="yellow")

    for mode in ["playground", "shared"]:
        root = Path(f"projects/{mode}")
        if not root.exists():
            continue
        for p in root.iterdir():
            if p.is_dir():
                sm = StateMachine(p.name, mode)
                table.add_row(p.name, mode, sm.current_state.name, "N/A")
    console.print(table)

@app.command()
def promote(project_id: str):
    """Move playground → shared (now tracked by git)."""
    playground = Path(f"projects/playground/{project_id}")
    shared = Path(f"projects/shared/{project_id}")
    if not playground.exists():
        console.print("[red]Not in playground[/]")
        return
    shared.parent.mkdir(parents=True, exist_ok=True)
    playground.rename(shared)
    console.print(f"[bold green]✅ {project_id} promoted to shared/[/] (now on git)")

if __name__ == "__main__":
    app()