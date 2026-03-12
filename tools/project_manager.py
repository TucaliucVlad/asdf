# tools/project_manager.py
# Version: 2.0 - Persistent active project + load/save state

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from rich.console import Console

from core.models import Project, ProjectState

console = Console()

ACTIVE_FILE = Path("projects") / ".active"
PROJECTS_ROOT = Path("projects")

def sanitize_slug(name: str) -> str:
    """Convert name to safe folder slug."""
    name = re.sub(r'[^a-zA-Z0-9\s-]', '', name.lower())
    name = re.sub(r'\s+', '-', name.strip())
    return name[:100]

def create_project_folder(project_name: str) -> Path:
    """Create unique project folder + initial files."""
    slug = sanitize_slug(project_name)
    base_folder = PROJECTS_ROOT / slug
    folder = base_folder
    counter = 1
    while folder.exists():
        folder = base_folder.with_name(f"{slug}-{counter}")
        counter += 1

    folder.mkdir(parents=True)
    console.print(f"[green]Created project folder:[/] {folder}")

    # project.json (metadata)
    metadata = {
        "name": project_name,
        "slug": folder.name,
        "created_at": datetime.now().isoformat(),
        "initial_prompt_file": "initial_prompt.txt"
    }
    (folder / "project.json").write_text(json.dumps(metadata, indent=2))

    return folder

def get_active_project() -> Optional[str]:
    """Return slug of currently active project or None."""
    if ACTIVE_FILE.exists():
        return ACTIVE_FILE.read_text(encoding="utf-8").strip()
    return None

def set_active_project(slug: str):
    """Set active project (creates .active file)."""
    ACTIVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    ACTIVE_FILE.write_text(slug, encoding="utf-8")
    console.print(f"[bold green]→ Project {slug} is now ACTIVE[/]")

def load_project(slug: str) -> Tuple[Project, Path]:
    """Load Project from folder + return folder path."""
    folder = PROJECTS_ROOT / slug
    if not folder.exists():
        console.print(f"[red]Project folder {slug} not found.[/]")
        raise typer.Exit(1)

    project_json = folder / "project.json"
    if not project_json.exists():
        console.print(f"[red]project.json missing in {slug}.[/]")
        raise typer.Exit(1)

    data = json.loads(project_json.read_text())
    # Load initial prompt if present
    prompt_file = folder / data.get("initial_prompt_file", "initial_prompt.txt")
    initial_prompt = prompt_file.read_text(encoding="utf-8") if prompt_file.exists() else ""

    project = Project(name=data["name"], initial_prompt=initial_prompt)
    return project, folder

def save_project_state(folder: Path, project: Project, current_state: ProjectState, history: list):
    """Save full state to state.json."""
    state_data = {
        "project": project.model_dump(),
        "current_state": current_state.name,
        "history": history,
        "updated_at": datetime.now().isoformat()
    }
    (folder / "state.json").write_text(json.dumps(state_data, indent=2))