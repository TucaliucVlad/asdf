import traceback
import sys

print("=== PHASE 5 DEBUG START ===")
print("Python version:", sys.version.split()[0])
print("Current working directory:", __import__("os").getcwd())

# === IMPORTS ONE BY ONE ===
try:
    from agents.requirements_engineer import run as req_run
    print("✅ Imported requirements_engineer")
except Exception as e:
    print("❌ FAILED TO IMPORT requirements_engineer")
    traceback.print_exc()
    sys.exit(1)

try:
    from agents.planner import run as plan_run
    print("✅ Imported planner")
except Exception as e:
    print("❌ FAILED TO IMPORT planner")
    traceback.print_exc()
    sys.exit(1)

try:
    from agents.implementer import run as impl_run
    print("✅ Imported implementer")
except Exception as e:
    print("❌ FAILED TO IMPORT implementer")
    traceback.print_exc()
    sys.exit(1)

try:
    from agents.tester import run as test_run
    print("✅ Imported tester")
except Exception as e:
    print("❌ FAILED TO IMPORT tester")
    traceback.print_exc()
    sys.exit(1)

print("All imports succeeded. Now running agents...")

# === RUN EACH AGENT ===
try:
    req = req_run("test-project-123", "dummy prompt")
    print("✅ Requirements Engineer run OK")
except Exception as e:
    print("❌ Requirements Engineer run FAILED")
    traceback.print_exc()

try:
    plan = plan_run("test-project-123", req)
    print("✅ Planner run OK")
except Exception as e:
    print("❌ Planner run FAILED")
    traceback.print_exc()

try:
    impl = impl_run("test-project-123", plan)
    print("✅ Implementer run OK")
except Exception as e:
    print("❌ Implementer run FAILED")
    traceback.print_exc()

try:
    tst = test_run("test-project-123", impl)
    print("✅ Tester run OK")
except Exception as e:
    print("❌ Tester run FAILED")
    traceback.print_exc()

print("=== PHASE 5 DEBUG END ===")