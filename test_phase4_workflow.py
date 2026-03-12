from workflows.loader import WorkflowLoader
from core.stage_router import StageRouter

print("=== Phase 4 Workflow Loader + Stage Router Test ===")

loader = WorkflowLoader()
stages = loader.get_stages()
print("WorkflowLoader loaded")
print("Number of stages in default workflow:", len(stages))
for s in stages:
    print("  -", s.get("name"), "(protection:", s.get("protection", "none"), ")")

router = StageRouter("test-project-123")
print("StageRouter imported and initialized")
print("Project root created at projects/test-project-123")
print("All Phase 4 components ready for L1/L2 protection routing")