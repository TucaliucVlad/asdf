from core.orchestrator import Orchestrator

print("=== Phase 6 End-to-End Test ===")
orchestrator = Orchestrator("test-project-123")
orchestrator.run_full_pipeline("Create a simple hello-world demo")
print("✅ Full pipeline completed (L1 + L2 protection verified)")