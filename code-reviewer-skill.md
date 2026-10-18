---
name: code-reviewer-secops
description: Comprehensive security and quality code review skill. Triggers when reviewing pull requests, inspecting source code for OWASP vulnerabilities (e.g., indirect prompt injection, SQLi, XSS), checking PII/GDPR compliance, code style, or running static analysis before deployment.
version: 1.1.0
allowed-tools:
  - run_command
  - view_file
  - list_dir
  - grep_search
author: AI Engineering SecOps Team
---

# Code Reviewer & Security Auditor Skill (`code-reviewer-secops`)

## Purpose
This skill guides the AI agent through a rigorous, two-pass code review process:
1. **Security, Privacy & Vulnerability Audit** (OWASP Top 10, OWASP Agentic ASI01-ASI10, Stage-Gate Port 4 PII & Port 9 Governance)
2. **Quality, Maintainability & Architecture Assessment** (Edward Tufte visual standards, FAST financial modeling, modularity)

---

## Workflow & Step-by-Step Procedure

### Step 1: Scope Identification & File Inspection
1. Discover the target files using `list_dir` or `grep_search`.
2. Inspect file structures and dependencies without dumping raw binaries.
3. If reviewing a diff or pull request, read target source files using `view_file` focusing on modified lines and surrounding context.

### Step 2: Security, Privacy & Vulnerability Audit
Scan for critical security and governance flaws using the following checklist:

- **Prompt & Data Injection (ASI01/ASI06)**: Inspect all LLM tool integration points for unparsed tool outputs, missing boundary delimiters/nonces, or direct concatenation of untrusted user input into system prompts.
- **Norwegian PII & Privacy Leakage (Stage-Gate Port 4)**: Verify zero unredacted national identity numbers (Fødselsnummer 11-sifre, D-nummer), phone numbers (`+47`), or personal contact details are stored in plain text or sent to external public APIs.
- **Injection & Input Validation**: Check SQL queries for parameter binding (DuckDB/SQLite), shell commands for unsanitized inputs, and web templates for XSS risks.
- **Secrets & Hardcoded Credentials**: Verify no API keys, private tokens, passwords, or connection strings are hardcoded in source code or configuration files.
- **Access Control & Least Privilege**: Ensure endpoints enforce authentication and authorization checks (e.g. Teams RLS, FastAPI route dependencies).
- **Statutory & Audit Governance (Stage-Gate Port 9)**: Verify that high-impact municipal operations or financial forecasts enforce cryptographic SHA-256 state sealing and require named Human-In-The-Loop (HITL) approval (`APPROVED`, `MODIFIED`, `REJECTED`).

### Step 3: Static Analysis & Script Execution
- If executable validation scripts exist in `scripts/` or `tools/`, execute static analysis tools (e.g., `python tools/evaluation_runner.py` or linter scripts) using `run_command`.
- Do NOT read full test harness source code into the context window unless debugging a script failure; execute scripts directly to keep token consumption minimal.

### Step 4: Quality & Architecture Review
- **Error Handling**: Verify robust exception catching (`try-except` blocks) without silent suppression (`except: pass`).
- **Type Safety & Schemas**: Ensure function signatures use explicit type annotations or Pydantic data models.
- **Maintainability & Documentation**: Verify core public APIs include docstrings and modular separation of concerns.
- **Edward Tufte UI Standards**: For dashboard, chart, or Excel exports, verify compliance with Data-Ink Ratio principles (no vertical gridlines in tables, muted palette, bright colors reserved strictly for active variances, direct labeling).

### Step 5: Output Synthesis & Grading
Structure the review output according to the standard review template:

1. **Executive Summary & Gate Decision**:
   - `PASSED`: Code meets all security, quality, and compliance requirements.
   - `NEEDS_REVISION`: Minor non-security flaws or style improvements required.
   - `BLOCKED_SECURITY_RISK`: Critical vulnerability, PII leak, or compliance violation identified.
2. **Security & Compliance Findings (Critical/High/Medium/Low)**:
   - Clear description, file path, line numbers, and concrete remediation code snippet.
3. **Code Quality & Architecture Suggestions**:
   - Constructive recommendations for performance, type safety, and maintainability.
