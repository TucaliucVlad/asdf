# core/models.py
# Version: 2.0 - Achievement-oriented states (as you suggested)

from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

class ProjectState(Enum):
    CREATED = "CREATED"                    # after start
    REQUIREMENTS_FORMALIZED = "REQUIREMENTS_FORMALIZED"  # after Requirements Engineer
    PLANNED = "PLANNED"                    # after Planner Agent (exactly what you wanted)
    IMPLEMENTING = "IMPLEMENTING"
    IMPLEMENTED = "IMPLEMENTED"
    TESTED = "TESTED"
    COMPLETE = "COMPLETE"

class CostEstimate(BaseModel):
    input_tokens: int
    estimated_output_tokens: int
    estimated_cost_usd: float
    model_used: str

class Project(BaseModel):
    name: str
    initial_prompt: str