# 🤖 Instruction Guide for Antigravity AI Agent

## Project Context
You are working on AI_KOM, an AI-driven financial advisory system for Kristiansand kommune (Helse og Mestring).

## Code Standards & Conventions:
1. **Pydantic v2 Models**: All tool arguments must strictly validate against models in app/schemas.py.
2. **Parameterized SQL Queries**: Never execute raw string SQL queries. Always pass parameters via tuple/dict to prevent SQL injection.
3. **Role-Based Access Control (RBAC)**: Ensure all SQL tools enforce WHERE ansvar = '...' for enhetsleder role.
4. **Immutable Audit Logging**: Log every user query, tool invocation, and budget reallocation to stg_audit_log.
5. **Loop Engineering**: Maintain recursion limits (max_iterations = 5) and handle exception loops gracefully.
