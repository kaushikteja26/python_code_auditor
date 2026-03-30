import subprocess
import json
import requests
import os
import re


# ==============================
# INPUT
# ==============================

def get_user_code():
    print("Paste your Python code. Type END on a new line to finish.\n")
    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)


# ==============================
# FILE HANDLING
# ==============================

def write_temp_file(code):
    file_path = "temp_code.py"
    with open(file_path, "w") as f:
        f.write(code)
    return file_path


# ==============================
# STATIC ANALYSIS
# ==============================

def run_ruff(file_path):
    return subprocess.run(
        ["ruff", "check", file_path, "--output-format=json"],
        capture_output=True,
        text=True
    )


# ==============================
# RUNTIME EXECUTION
# ==============================

def run_python(file_path):
    try:
        return subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(
            args=["python", file_path],
            returncode=1,
            stdout="",
            stderr="Error: Execution timed out (5s limit)."
        )


# ==============================
# LOCAL LLM CALL
# ==============================

def run_llm_review(code, lint_json, runtime_error):

    prompt = f"""
You are a strict Python correction engine.

Original Code:
{code}

Static Errors:
{lint_json}

Runtime Error:
{runtime_error}

STRICT RULES:
- Preserve original program intent.
- You MAY remove unused imports.
- You MAY remove unnecessary code.
- Do NOT change numeric literals.
- Do NOT modify arithmetic values.
- Do NOT introduce new imports unless absolutely required.
- Handle runtime errors safely without altering numbers.
- Return a complete corrected program.

FORMAT:

EXPLANATION:
<brief explanation>

CORRECTED_CODE:
<full corrected program>
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "temperature": 0
            },
            timeout=180
        )

        result = response.json()
        return result.get("response", "")

    except Exception as e:
        return f"LLM call failed: {e}"


# ==============================
# EXTRACTION
# ==============================

def extract_corrected_code(output):

    import re

    # Extract after explicit marker
    if "CORRECTED_CODE:" in output:
        after = output.split("CORRECTED_CODE:", 1)[1]

        # Remove explanation section if included
        if "EXPLANATION:" in after:
            after = after.split("EXPLANATION:", 1)[0]

        return after.strip()

    # Extract fenced python block
    matches = re.findall(r"```python(.*?)```", output, re.DOTALL)
    if matches:
        code = matches[-1]

        if "EXPLANATION:" in code:
            code = code.split("EXPLANATION:", 1)[0]

        return code.strip()

    return None
# ==============================
# SEMANTIC VALIDATION
# ==============================

def semantic_validation(original, corrected):

    # 1. Numeric literals preserved
    original_numbers = re.findall(r'\d+', original)
    corrected_numbers = re.findall(r'\d+', corrected)

    if original_numbers != corrected_numbers:
        return False, "Numeric literals were modified."

    # 2. No new imports
    original_imports = re.findall(r'^import\s+\w+', original, re.MULTILINE)
    corrected_imports = re.findall(r'^import\s+\w+', corrected, re.MULTILINE)

    for imp in corrected_imports:
        if imp not in original_imports:
            return False, "New imports were introduced."

    # 3. Preserve print logic
    if "print" in original and "print" not in corrected:
        return False, "Core print logic removed."

    return True, ""


# ==============================
# MAIN
# ==============================

def main():

    code = get_user_code()
    if not code.strip():
        print("No code provided.")
        return

    file_path = write_temp_file(code)

    try:
        print("\n--- Static Analysis ---")
        ruff_result = run_ruff(file_path)

        lint_json = ruff_result.stdout if ruff_result.stdout else "[]"

        try:
            errors = json.loads(lint_json) if lint_json else []
            if not errors:
                print("No lint issues.")
            else:
                for e in errors:
                    print(f"{e['code']} - {e['message']} (Line {e['location']['row']})")
        except:
            print("Could not parse Ruff output.")

        print("\n--- Runtime Execution ---")
        python_result = run_python(file_path)

        runtime_error = ""
        if python_result.returncode == 0:
            print("Execution successful.")
            if python_result.stdout:
                print("Output:\n", python_result.stdout)
        else:
            runtime_error = python_result.stderr
            print("Runtime error:\n", runtime_error)

        if errors or runtime_error:
            print("\n--- LLM Review ---\n")

            max_attempts = 2
            attempt = 0
            validation_passed = False

            current_review = run_llm_review(code, lint_json, runtime_error)
            print(current_review)

            while attempt < max_attempts and not validation_passed:

                print(f"\n--- Validation Attempt {attempt + 1} ---\n")

                corrected_code = extract_corrected_code(current_review)

                if not corrected_code:
                    print("No corrected code found.")
                    break

                valid, reason = semantic_validation(code, corrected_code)

                if not valid:
                    print("Semantic validation failed:", reason)
                    attempt += 1
                    current_review = run_llm_review(
                        code,
                        lint_json,
                        runtime_error + "\nValidation Failure: " + reason
                    )
                    print(current_review)
                    continue

                write_temp_file(corrected_code)

                new_ruff = run_ruff("temp_code.py")
                try:
                    new_errors = json.loads(new_ruff.stdout) if new_ruff.stdout else []
                except:
                    new_errors = ["Parsing error"]

                new_runtime = run_python("temp_code.py")

                if not new_errors and new_runtime.returncode == 0:
                    print("✔ Correction validated successfully.")
                    validation_passed = True
                else:
                    print("Static or runtime errors still exist.")
                    attempt += 1
                    current_review = run_llm_review(
                        code,
                        lint_json,
                        runtime_error + "\nValidation Failure: Static/Runtime errors remain."
                    )
                    print(current_review)

            if not validation_passed:
                print("\n⚠ Auto-correction failed after retries.")
                print("Returning structured explanation only.")

        else:
            print("\nCode looks clean. No correction needed.")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


if __name__ == "__main__":
    main()