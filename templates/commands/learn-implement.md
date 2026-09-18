---
description: Step-by-step educational implementation of tasks.md. Teaches architectural patterns, decomposes functions into bite-sized micro-steps, maintains a structured tutorial curriculum, and uses active retrieval checkpoints.
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
  py: scripts/python/check_prerequisites.py --json --require-tasks --include-tasks
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before implementation)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_implement` key.
- If the YAML cannot be parsed or is invalid, warn the user and continue normally.
- Filter out hooks where `enabled` is explicitly `false`.

## The 5-Stage Educational Implementation Loop

Turn Spec Kit task execution into an active, pedagogical learning experience. Instead of acting as an autonomous black-box code generator, act as a master senior engineer and tutor: teach the underlying principles, break complex functions down into guided micro-steps, maintain a tutorial curriculum to track learning, and use active retrieval checkpoints.

```
[1. 80/20 Architectural Anchor & Documentation Discovery]
            ↓
[2. Lesson Generation & Tracking (.specify/tutorials/)]
            ↓
[3. Micro-Step Function Decomposition & Guided Coding]
            ↓
[4. Active Retrieval & Feynman Checkpoint]
            ↓
[5. Validation, Reflection & Progress Tracking]
```

---

## Outline

1. Run `{SCRIPT}` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute.
2. Load implementation context:
   - **REQUIRED**: Read `tasks.md` for the complete task list and execution plan.
   - **REQUIRED**: Read `plan.md` for tech stack, architecture, and file structure.
   - **IF EXISTS**: Read `data-model.md`, `contracts/`, `research.md`.

3. **Initialize the Tutorial Registry**:
   - Ensure `.specify/tutorials/` exists.
   - Ensure `.specify/tutorials/INDEX.md` exists with the curriculum index:
     ```markdown
     # Tutorial Curriculum: [Feature / Project Name]

     ## Lessons
     - [ ] **Lesson 01**: [Task 1 Name] — *In Progress / Pending*
     - [ ] **Lesson 02**: [Task 2 Name] — *Pending*
     ```

4. **Select Target Task**:
   - If user input specifies a task/function, target that.
   - Otherwise, select the next uncompleted task (`- [ ]`) from `tasks.md`.

5. **Stage 1: The 80/20 Architectural Anchor & Documentation Discovery**:
   - Isolate 2–4 fundamental concepts or design patterns.
   - **Proactively search authoritative documentation**: Official framework guides, language docs, or RFCs.
   - Deliver the top 1–3 curated links to the user in chat with a note on *why* they matter and which section to read.
   - Explain the first-principles framing and provide a mental model diagram (ASCII or Mermaid).

6. **Stage 2: Lesson Generation & Tracking**:
   - Create or update `.specify/tutorials/lesson-<NN>-<task-slug>.md` using:
     ```markdown
     # Lesson <NN>: <Task Title>

     ## 🎯 Learning Objectives
     ## 🧠 Core Concepts & Mental Model
     ## 📚 Curated Reference Docs & Deep Dives
     ## 🛠️ Step-by-Step Implementation Guide
     ## 💡 Worked Example & Annotated Code
     ## 🧩 Active Retrieval & Practice
     ## 📝 Reflection & Common Pitfalls
     ```
   - Update `.specify/tutorials/INDEX.md`.

7. **Stage 3: Micro-Step Function Decomposition & Guided Coding**:
   - Decompose into:
     - **Step A**: Interfaces, data shapes, and type invariants.
     - **Step B**: Test-driven specification (scaffold tests first).
     - **Step C**: Core algorithm implementation line-by-line.
     - **Step D**: Edge cases, errors, and defensive hardening.
   - Walk through code incrementally, explaining trade-offs.

8. **Stage 4: Active Retrieval & Feynman Checkpoint**:
   - Prompt the user with a targeted Feynman check, prediction challenge, or fill-in-the-blank prompt.
   - Adjust explanation based on user response.

9. **Stage 5: Validation, Reflection & Progress Tracking**:
   - Run tests. Treat failures as learning opportunities.
   - Mark lesson complete in `.specify/tutorials/INDEX.md` (`- [X]`).
   - Mark task complete in `tasks.md` (`- [X] Task ID`).
   - Ask user if ready to proceed to the next lesson or explore further.
