# agents/requirements_engineer.py
# Version: 1.0 - Phase 3

from tools.llm_client import llm_call
import json
from pathlib import Path
from rich.console import Console

console = Console()

def run_requirements_engineer(project_folder: Path, initial_prompt: str):
    console.print("[bold cyan]Requirements Engineer Agent running...[/]")

    messages = [
        {"role": "system", "content": Path("prompts/requirements_system.md").read_text(encoding="utf-8")},
        {"role": "user", "content": f"User prompt:\n{initial_prompt}"}
    ]

    response = llm_call(messages, model="groq/grok-beta", max_tokens=4000)

    try:
        reqs = json.loads(response)
        (project_folder / "requirements.json").write_text(json.dumps(reqs, indent=2))
        console.print("[green]✓ Requirements saved as requirements.json[/]")
        return reqs
    except:
        console.print("[red]Failed to parse requirements JSON.[/]")
        return None