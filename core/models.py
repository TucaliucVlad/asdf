# core/models.py
from pydantic import BaseModel
from enum import Enum, auto
from typing import Optional, List

class ProjectState(Enum):
    IDLE = auto()
    ANALYZE = auto()
    CLARIFY = auto()
    REQUIREMENTS = auto()
    PLANNING = auto()
    EXECUTION = auto()
    TESTING = auto()
    DOCUMENT = auto()
    COMPLETE = auto()

class Project(BaseModel):
    name: str
    initial_prompt: str
    created_at: str = ""  # can add datetime later

class WorkflowStep(BaseModel):
    name: str
    description: str
    model_preference: str = "grok-4.1-fast"

    # ─── Additions for Phase 2 ────────────────────────────────────────

class CostEstimate(BaseModel):
    input_tokens: int
    estimated_output_tokens: int = 0
    estimated_cost_usd: float
    model_used: str