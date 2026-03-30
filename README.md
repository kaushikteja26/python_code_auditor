# LLM-Powered Code Auditor 

An autonomous Python code auditing pipeline that combines deterministic linter parsing with a local LLM agent to analyze, correct, and safely execute code.

## Architecture Overview
This project demonstrates a closed-loop Agentic AI pipeline—translating non-deterministic LLM reasoning into strict, executable programmatic actions:

1. **Static Analysis (The Guardrail):** Uses `Ruff` to deterministically parse Python code for syntax and logic errors.
2. **Agentic Feedback Loop:** Extracts exact error tracebacks and feeds them as context into a local LLM agent.
3. **Self-Correction:** The LLM acts as a senior code analyst, generating the structurally corrected code.
4. **Safe Execution:** The pipeline validates and executes the corrected code.

## Tech Stack
* **Language:** Python 3.10+
* **LLM Inference:** [Ollama](https://ollama.com/) (Local deployment, zero external API dependencies)
* **Static Analysis:** [Ruff](https://docs.astral.sh/ruff/) (Extremely fast Python linter)

## Quick Start

**1. Install Requirements**
```bash
pip install ruff
