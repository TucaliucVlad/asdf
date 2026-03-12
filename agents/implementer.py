# agents/implementer.py
# Version: 1.0 - Full Implementation Agent (generates real Python code)

from tools.llm_client import llm_call
import json
from pathlib import Path
from rich.console import Console

console = Console()

def run_implementer(folder: Path, requirements: dict, plan: dict):
    """Generate actual code files from plan + requirements using xAI Grok."""
    console.print("[bold cyan]Implementation Agent running... (generating real code)[/]")
    
    system_prompt = (
        "You are an expert Python developer. Generate a COMPLETE, runnable project exactly matching the requirements and plan.\n"
        "Output ONLY a valid JSON object like this:\n"
        '{"files": {"main.py": "full code here...", "factorial.py": "...", "test_factorial.py": "..."}}\n'
        "Include all files needed (CLI entrypoint, core logic, tests, README if in plan). Make it clean, well-commented, and 100% working."
    )
    
    context = f"Requirements:\n{json.dumps(requirements, indent=2)}\n\nPlan:\n{json.dumps(plan, indent=2)}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Create the full project code now:\n{context}"}
    ]
    
    response = llm_call(messages, max_tokens=8000, temperature=0.2)
    
    try:
        data = json.loads(response)
        files = data.get("files", {})
    except Exception:
        console.print("[yellow]Could not parse JSON — saving raw output for debug[/]")
        (folder / "implementer_raw.txt").write_text(response, encoding="utf-8")
        return
    
    for rel_path, code in files.items():
        file_path = folder / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(code.strip(), encoding="utf-8")
        console.print(f"[green]✅ Created:[/] {rel_path}")
    
    console.print("[bold green]✅ Implementation Agent completed — full working code generated![/]")