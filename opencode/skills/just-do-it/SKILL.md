---
name: just-do-it
description: Execute a clear, detailed technical specification (TS) with minimal reasoning. No questions, no planning chatter, just implement using all available tools. Use when user gives a ready TS and wants autonomous execution.
license: MIT
compatibility: opencode
---

# Just Do It

You receive a clear, detailed technical specification (TS).

## Rules (strict)

- Do NOT ask any clarifying questions.
- Do NOT output long reasoning, plans, or explanations unless explicitly required by the TS.
- Minimize internal reasoning tokens. Act.
- Use every available tool (bash, file edit, search, etc.) as needed.
- Work step-by-step until the TS is fully completed.
- Prefer the smallest correct change that satisfies the requirements.
- If something is ambiguous — make the most reasonable assumption based on the codebase and existing patterns and proceed.
- At the end give a very short status: what was done + key files changed.

## Mandatory execution constraints

- First implement the entire task **on paper only** — without making any real changes to production / project code.
- You are allowed to work fully in combat mode on the real infrastructure.
- You may create any temporary files, directories, scripts, or sandboxes you need (`tmp`, `/tmp`, project-local temp dirs, etc.).
- Use any tools necessary (bash, tests, benchmarks, profilers, linters, etc.).
- Perform all required tests and measurements.
- The computer is fully at your disposal.
- Only after the solution is ready, working, and tested — present the final working code that implements the task in the real system.
- Always provide a brief summary of what you are going to do or what you have already done.
- **Do not apply any real changes to the project until the user explicitly gives approval.**

## Workflow

1. Quickly scan relevant files/tools if needed.
2. Design and implement the full solution in temporary/isolated space.
3. Run all necessary tests, checks, and measurements.
4. Iterate and fix until the solution is solid.
5. Present the final working, tested code + short status.
6. Wait for explicit user approval before applying any real changes.
