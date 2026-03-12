import typer
from core.orchestrator import Orchestrator

app = typer.Typer()

@app.command()
def start(project_id: str):
    """Start new project with full protected pipeline."""
    Orchestrator(project_id).run_full_pipeline()
    print(f"Project {project_id} started and completed!")

@app.command()
def run(project_id: str):
    """Run full protected pipeline (requirements → L1 → L2 → complete)."""
    Orchestrator(project_id).run_full_pipeline()

@app.command()
def status(project_id: str):
    """Show current state."""
    from core.state_machine import StateMachine
    sm = StateMachine(project_id)
    print(f"Project {project_id} state: {sm.current_state.name}")

@app.command()
def proceed(project_id: str):
    """Resume pipeline (future expansion point)."""
    print("Proceed: use 'run' for full re-execution in this version.")

if __name__ == "__main__":
    app()