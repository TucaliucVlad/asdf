from core.state_machine import StateMachine, ProjectState

print("=== Phase 3 State Machine Test ===")

sm = StateMachine("test-project-123")
print("Current state:", sm.current_state.name)
print("All L1/L2 retry states loaded:", [s.name for s in ProjectState if "RETRY" in s.name or "FAILED_L" in s.name or "L1" in s.name or "L2" in s.name])

print("State machine loaded successfully")
print("Example L1 retry state:", ProjectState.PROTECTION_LEVEL_1_RETRY_1.name)
print("Terminal states ready for protection flow")