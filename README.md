# CodeSentinelAI

### AI-Powered Code Auditing, Correction & Validation

CodeSentinelAI is an autonomous code-auditing pipeline designed to detect, analyze, correct, and validate Python code using a combination of deterministic static analysis and AI reasoning.

The project explores how AI agents can move beyond simply explaining code errors and instead participate in a controlled **detect → analyze → correct → validate** loop.

---

## The Problem

Traditional linters are excellent at detecting known classes of issues, but they generally stop at reporting problems.

Developers still have to:

1. Understand the reported error
2. Identify the root cause
3. Modify the code
4. Run the code again
5. Verify that the correction actually works

CodeSentinelAI explores an automated workflow that closes this loop.

---

## How It Works

```text
             Python Source Code
                     │
                     ▼
             ┌───────────────┐
             │     Ruff      │
             │ Static Check  │
             └───────┬───────┘
                     │
             Errors / Tracebacks
                     │
                     ▼
             ┌───────────────┐
             │   AI Agent    │
             │ Code Analysis │
             └───────┬───────┘
                     │
              Corrected Code
                     │
                     ▼
             ┌───────────────┐
             │   Validation  │
             │ & Execution   │
             └───────┬───────┘
                     │
              Validated Result
```

### Pipeline

**1. Static Analysis**

Ruff performs deterministic analysis of the Python source code and identifies issues.

**2. Error Extraction**

Relevant errors and execution information are collected and provided to the AI reasoning layer.

**3. AI-Powered Analysis**

The language model analyzes the reported problem and determines how the code should be corrected.

**4. Self-Correction**

The agent generates a corrected version of the source code.

**5. Validation**

The corrected code is checked and executed to determine whether the proposed correction is valid.

---

## Current Architecture

The current implementation uses:

- **Python 3.10+**
- **Ruff** for deterministic static analysis
- **Ollama** for local LLM inference
- An agentic feedback loop for code analysis and correction

The current local-LLM architecture allows experimentation without requiring an external model API.

---

## Why CodeSentinelAI?

Most developer tools focus on one part of the development workflow:

- Linters detect problems
- IDEs highlight problems
- LLMs explain problems
- Developers manually apply and verify fixes

CodeSentinelAI explores a different approach:

> **Detect the problem → reason about the problem → generate a correction → validate the correction.**

The goal is not to replace deterministic developer tooling, but to combine deterministic checks with AI reasoning in a controlled workflow.

---

## Example Workflow

Given Python code containing an error:

```python
def calculate_total(items):
    total = 0

    for item in items
        total += item

    return total
```

The pipeline can:

1. Detect the syntax problem using static analysis.
2. Extract the relevant diagnostic information.
3. Provide the context to the AI reasoning layer.
4. Generate a corrected implementation.
5. Validate the corrected code.

---

## Project Structure

```text
python_code_auditor/
│
├── auditor.py       # Core auditing pipeline
├── day1.py          # Development / experimentation code
└── README.md        # Project documentation
```

---

## Getting Started

### Requirements

- Python 3.10+
- Ruff
- Ollama

### Install Ruff

```bash
pip install ruff
```

### Install Ollama

Download and install Ollama from:

https://ollama.com/

Then configure a local model suitable for code analysis.

---

## Current Status

### Implemented

- [x] Deterministic Python static analysis
- [x] Ruff integration
- [x] Error / traceback extraction
- [x] Local LLM integration
- [x] AI-assisted code correction
- [x] Corrected-code validation workflow

### In Development

- [ ] Web-based interface
- [ ] Repository-level auditing
- [ ] GitHub integration
- [ ] Pull-request code review
- [ ] Security-focused analysis
- [ ] Multi-file project analysis
- [ ] Automated test generation
- [ ] Production-grade sandboxed execution

---

## Roadmap

### Phase 1 — Core Auditor
Build a reliable detect → analyze → correct → validate pipeline.

### Phase 2 — Developer Workflow
Integrate the auditor into GitHub repositories and pull requests.

### Phase 3 — Security & Reliability
Expand analysis beyond syntax and linting into security vulnerabilities, unsafe patterns, and reliability issues.

### Phase 4 — AI Code Review Platform
Provide developers and teams with an automated AI-assisted code auditing workflow.

---

## Claude Integration

The current development version uses a local LLM through Ollama.

A planned direction for CodeSentinelAI is to integrate **Claude's API** for higher-quality code reasoning, remediation, and project-level analysis.

This would allow the system to combine:

- Deterministic static analysis
- Large-context code reasoning
- Automated remediation
- Validation and execution
- Repository-level analysis

Claude integration is currently part of the planned product direction and is not represented as an existing feature of this repository.

---

## Vision

CodeSentinelAI aims to make code auditing an active engineering workflow rather than a passive error-reporting step.

Instead of:

```text
Write Code
   ↓
Find Error
   ↓
Read Error
   ↓
Fix Manually
   ↓
Run Again
```

the goal is:

```text
Write Code
   ↓
Detect
   ↓
Analyze
   ↓
Correct
   ↓
Validate
   ↓
Verified Code
```

---

## Project

**CodeSentinelAI**

AI-powered code auditing and automated remediation.

GitHub:
https://github.com/kaushikteja26/python_code_auditor

Domain:
https://codesentinelai.dev

---

## License

This project is currently an experimental development project.
