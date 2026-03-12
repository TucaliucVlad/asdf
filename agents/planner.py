# agents/planner.py
# Version: 1.0 - Phase 3

from tools.llm_client import llm_call
import json
from pathlib import Path
from rich.console import Console

console = Console()

def run_planner(project_folder: Path, requirements: dict):
    console.print("[bold cyan]Planner Agent running...[/]")

    messages = [
        {"role": "system", "content": Path("prompts/planner_system.md").read_text(encoding="utf-8")},
        {"role": "user", "content": json.dumps(requirements, indent=2)}
    ]

    response = llm_call(messages, model="groq/grok-beta", max_tokens=6000)

    try:
        plan = json.loads(response)
        (project_folder / "plan.json").write_text(json.dumps(plan, indent=2))
        console.print("[green]✓ Detailed plan saved as plan.json[/]")
        return plan
    except:
        console.print("[red]Failed to parse plan JSON.[/]")
        return None