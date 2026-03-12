from pathlib import Path
from typing import Dict, Any
from core.state_machine import StateMachine, ProjectState
from core.retry_policy import retry_policy
from workflows.loader import WorkflowLoader

class StageRouter:
    """Central router that applies protection levels (L1/L2) between stages — exactly per Correction Pack."""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.state_machine = StateMachine(project_id)
        self.loader = WorkflowLoader()
        self.project_root = Path(f"projects/{project_id}")
        self.project_root.mkdir(parents=True, exist_ok=True)
    
    def process_stage(self, stage_name: str, agent_output: Dict[str, Any]) -> ProjectState:
        """Routes stage and applies L1 validation + L2 test protection when required."""
        stages = self.loader.get_stages()
        batch_id = agent_output.get("batch_id", "unknown")
        task_ids = agent_output.get("task_ids", [])
        
        for stage in stages:
            if stage["name"] == stage_name:
                next_state_name = stage.get("next_state", "REVIEW_BATCH")
                next_state = ProjectState[next_state_name]
                
                # Apply L1/L2 protection for implementation stage
                if stage.get("protection") == "L1_L2":
                    try:
                        validated = retry_policy.l1_validate_and_retry(
                            agent_output, "code_writing", batch_id, task_ids
                        )
                        self.state_machine.transition(ProjectState.MATERIALIZE_FILES, batch_id, task_ids)
                        return ProjectState.MATERIALIZE_FILES
                    except Exception as e:
                        if "L1 exhausted" in str(e):
                            return self.state_machine.handle_l1_failure(3, batch_id, task_ids)
                        raise
                
                return self.state_machine.transition(next_state, batch_id, task_ids)
        
        return self.state_machine.current_state