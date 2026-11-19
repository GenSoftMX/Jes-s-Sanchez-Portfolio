---
name: present-information
description: >-
  Present current scope, options, architecture, diagrams, or a review package
  in chat. Use when the user asks to see these, or feature-delivery reaches
  presentation trigger A–E. Trigger E presents I2 spec/task drafts before
  creation and waits for explicit create confirmation. Do not use for plain Q&A, audits, or
  exploration without those triggers. Never for I0; no decision brief in I1;
  I2 before build and acceptance review.
---

# Skill: present-information (canonical)

Portable presentation procedure. **Showing does not decide or accept.**

**Do not activate** for direct questions, audits, or general exploration without
triggers A–E or an explicit request to present scope/options/package.

1. Read and apply [presentation-design](../../rules/presentation-design.md).
2. Follow the step-by-step flow in [present-information](../../workflows/present-information.md).
3. If an options/architecture brief is needed: [decision-brief](../../templates/decision-brief.md) **with the task** — never `specs/proposals/`.
4. Shape according to content (table, checkboxes, diagram, questions, prose). Fix the source, do not dress up the output.
5. In trigger E, present in chat/UI the full draft of the spec and initial task before writing related files. Wait for explicit confirmation to create; after creating, show and cross-check the files and request authorization separately to implement. A request for adjustments means updating and re-presenting. A native artifact is only valid if it does not create the spec/task in the workspace.
6. Diagram: host view if available, faithful to the source; otherwise, Mermaid in chat. Do not publish to external services unless explicitly requested.
7. I0: do not use this skill. I1: no brief; closeout = criteria + check. I2 pre–D-H: "ready for review", not "completed".

Native projections only point here; they do not rewrite the procedure.
