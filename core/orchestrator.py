from pathlib import Path
from core.state_machine import StateMachine, ProjectState
from core.stage_router import StageRouter
from agents.requirements_engineer import run as req_run
from agents.planner import run as plan_run
from agents.implementer import run as impl_run
from agents.tester import run as test_run
from core.materializer import Materializer
from core.retry_policy import retry_policy
import subprocess

class Orchestrator:
    def __init__(self, project_id: str, mode: str = "playground"):
        self.project_id = project_id
        self.mode = mode
        self.router = StageRouter(project_id)
        self.state_machine = StateMachine(project_id, mode)
        self.project_root = Path(f"projects/{mode}/{project_id}")
    
    def run_full_pipeline(self):
        seed_path = Path("init_prompt.txt")
        user_prompt = seed_path.read_text(encoding="utf-8").strip() if seed_path.exists() else "Build a simple demo"
        print(f"Starting protected pipeline with seed from init_prompt.txt")
        print(f"Seed preview: {user_prompt[:120]}...")

        # 1. Requirements + materialize
        req = req_run(self.project_id, user_prompt)
        Materializer.materialize(self.project_root, req.get("files", []))
        print("Requirements formalized + scaffolding materialized")

        # 2. Planning
        plan = plan_run(self.project_id, req)
        print("Planning completed")

        # 3. Implementation + L1/L2 + materialize
        impl = impl_run(self.project_id, plan)
        Materializer.materialize(self.project_root, impl.get("files", []))
        print("Implementation + L1/L2 protection + code materialized")

        # 4. Tester + L2 Protection
        test_data = test_run(self.project_id, impl)
        Materializer.materialize(self.project_root, test_data.get("test_files", []))
        print("Tests generated and materialized")

        # === ROBUST L2 (uses pytest tests/ folder — never fails on single file) ===
        print("=== L2 DEBUG ===")
        test_dir = self.project_root / "tests"
        test_files = list(test_dir.rglob("*.py")) if test_dir.exists() else []
        print(f"   Found {len(test_files)} test files in tests/: {[f.name for f in test_files]}")
        
        if test_files:
            try:
                l2_result = retry_policy.l2_run_tests_and_retry(
                    self.project_root, ["tests"],  # ← run whole folder
                    f"l2-{self.project_id}",
                    test_data.get("task_ids", ["test-1"])
                )
                print("✅ L2 protection passed — all tests green!")
            except ValueError as e:
                if "L2 protection exhausted" in str(e):
                    self.state_machine.transition(ProjectState.FAILED_L2_EXHAUSTED)
                    print("❌ L2 exhausted — pipeline failed safely (logged)")
                raise
        else:
            print("No tests found — skipping L2")

        # AUTO-INSTALL
        req_file = self.project_root / "requirements.txt"
        if req_file.exists():
            print("Auto-installing project dependencies...")
            subprocess.run(["pip", "install", "-r", "requirements.txt"], cwd=self.project_root, check=True)

        self.state_machine.transition(ProjectState.COMPLETE)
        print(f"Project {self.project_id} reached COMPLETE state!")
        print(f"   → Run with: cd projects/{self.mode}/{self.project_id} && python src/main.py")
        return "Pipeline finished successfully"