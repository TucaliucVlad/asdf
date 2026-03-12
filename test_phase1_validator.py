from core.json_validator import JsonValidator

validator = JsonValidator()

print("=== Phase 1 Validator Smoke Test ===")

# TEST 1: Valid scaffolding (must PASS)
valid_data = {
    "project_name": "test-project",
    "folders": ["src", "tests"],
    "files": [{
        "path": "src/main.py",
        "content": 'print("hello")',
        "intent": "entry point",
        "test_instructions": ["run main"]
    }]
}
try:
    validator.validate(valid_data, "scaffolding")
    print("✅ L1 VALID scaffolding — PASS")
except Exception as e:
    print("❌ VALID test failed:", e)

# TEST 2: Invalid data (extra field + unsafe path — must FAIL)
invalid_data = {
    "project_name": "test-project",
    "folders": ["src"],
    "files": [{
        "path": "../evil.py",           # unsafe
        "content": 'print("bad")',
        "intent": "bad",
        "test_instructions": ["run"],
        "extra_field": "should_fail"    # additionalProperties: false
    }]
}
try:
    validator.validate(invalid_data, "scaffolding")
    print("❌ Should have failed")
except Exception as e:
    print("✅ L1 INVALID correctly caught — PASS")