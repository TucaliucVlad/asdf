# tools/project_manager.py
# Version: 1.0 - Phase 2
# Handles project folder creation, naming, and initial file copying with safeguards

import os
import json
import re
from datetime import datetime
from pathlib import Path
from rich.console import Console

console = Console()

def sanitize_slug(name: str) -> str:
    """Convert name to safe folder slug: lowercase, hyphens, no special chars."""
    name = re.sub(r'[^a-zA-Z0-9\s-]', '', name.lower())
    name = re.sub(r'\s+', '-', name.strip())
    return name[:100]  # max length safety

def create_project_folder(project_name: str, root_path: Path = Path("projects")) -> Path:
    """Create unique project folder after confirmation."""
    slug = sanitize_slug(project_name)
    base_folder = root_path / slug
    folder = base_folder

    # Handle name collision
    counter = 1
    while folder.exists():
        folder = base_folder.with_name(f"{slug}-{counter}")
        counter += 1

    folder.mkdir(parents=True, exist_ok=False)
    console.print(f"[green]Created project folder:[/] {folder}")

    # Write basic metadata
    metadata = {
        "name": project_name,
        "slug": str(folder.name),
        "created_at": datetime.now().isoformat(),
        "initial_prompt_file": "initial_prompt.txt",
        "state_history": []
    }
    (folder / "project.json").write_text(json.dumps(metadata, indent=2))

    return folder