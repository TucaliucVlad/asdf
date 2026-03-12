# agents/planner.py
# Version: 1.0 - Full Planner Agent using your xAI Grok + $50 credits

from tools.llm_client import llm_call
import json
from pathlib import Path
from rich.console import Console

console = Console()

def run_planner(folder: Path, requirements: dict):
    """Generate a complete development plan from requirements.json"""
    console.print("[bold cyan]Planner Agent running...[/]")
    
    # Load system prompt (uses your existing prompts/planner_system.md)
    prompt_file = Path("prompts") / "planner_system.md"
    system_prompt = prompt_file.read_text(encoding="utf-8") if prompt_file.exists() else (
        "You are an expert software architect. Create a detailed, phased development plan "
        "with tasks, files to create/modify, and exact implementation order."
    )
    
    req_text = json.dumps(requirements, indent=2)
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Requirements:\n{req_text}\n\n"
                                    f"Output a JSON plan with: phases (array), tasks per phase, "
                                    f"files_to_create, estimated_steps, and priority order."}
    ]
    
    response = llm_call(messages, max_tokens=3000, temperature=0.6)
    
    # Parse JSON safely
    try:
        plan = json.loads(response)
    except json.JSONDecodeError:
        plan = {"raw_plan": response, "phases": [{"name": "Raw Output", "tasks": [response]}]}
    
    plan_path = folder / "plan.json"
    plan_path.write_text(json.dumps(plan, indent=2))
    
    console.print("[green]✅ Planner completed — plan.json saved[/]")
    console.print(f"[dim]Plan contains {len(plan.get('phases', []))} phases[/]")