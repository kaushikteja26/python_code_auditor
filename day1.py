import subprocess
import json

print("Paste your Python code below.")
print("Type END on a new line to finish.\n")

lines = []
while True:
    line = input()
    if line.strip() == "END":
        break
    lines.append(line)

code_string = "\n".join(lines)

# Write temp file
with open("temp_code.py", "w") as f:
    f.write(code_string)

# Run Ruff
result = subprocess.run(
    ["ruff", "check", "temp_code.py", "--output-format=json"],
    capture_output=True,
    text=True
)
# Runtime execution
print("\n--- Runtime Execution ---")

run_result = subprocess.run(
    ["python", "temp_code.py"],
    capture_output=True,
    text=True
)

if run_result.returncode == 0:
    print("Program executed successfully.")
    if run_result.stdout:
        print("Output:")
        print(run_result.stdout)
else:
    print("Runtime Error Detected:")
    print(run_result.stderr)

# Handle execution error
if result.stderr:
    print("Fatal error running Ruff:")
    print(result.stderr)
else:
    try:
        errors = json.loads(result.stdout)
        
        if not errors:
            print("No lint issues found.")
        else:
            print("Lint issues detected:")
            for err in errors:
                print(f"Rule: {err['code']}")
                print(f"Message: {err['message']}")
                print(f"Line: {err['location']['row']}")
                print("-" * 30)
    except json.JSONDecodeError:
        print("Failed to parse Ruff output.")