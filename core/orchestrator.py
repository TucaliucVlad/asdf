from pathlib import Path
from core.state_machine import StateMachine, ProjectState
from core.stage_router import StageRouter
from agents.requirements_engineer import run as req_run
from agents.planner import run as plan_run
from agents.implementer import run as impl_run
from agents.tester import run as test_run

class Orchestrator:
    """Full end-to-end protected pipeline (init → L1 → L2 → complete)."""
    
    def __init__(self, project_id: str, mode: str = "playground"):
        self.project_id = project_id
        self.router = StageRouter(project_id)
        self.state_machine = StateMachine(project_id, mode)
    
    def run_full_pipeline(self):
        seed_path = Path("init_prompt.txt")
        user_prompt = seed_path.read_text(encoding="utf-8").strip() if seed_path.exists() else "Build a simple demo project"
        print(f"🚀 Starting protected pipeline with seed from init_prompt.txt")
        print(f"Seed preview: {user_prompt[:120]}...")
        
        # 1. Requirements
        req = req_run(self.project_id, user_prompt)
        print("✅ Requirements formalized")
        
        # 2. Planning
        plan = plan_run(self.project_id, req)
        print("✅ Planning completed")
        
        # 3. Implementation + L1/L2 protection
        impl = impl_run(self.project_id, plan)
        print("✅ Implementation + L1/L2 protection completed")
        
        # 4. Tester
        test_run(self.project_id, impl)
        print("✅ Tests generated")
        
        self.state_machine.transition(ProjectState.COMPLETE)
        print(f"🎉 Project {self.project_id} reached COMPLETE state!")
        return "Pipeline finished successfully (Master Plan compliant)"