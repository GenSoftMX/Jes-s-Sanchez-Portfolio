---
id: present-information
type: workflow
revision: 2026-11-16
purpose: present scope, options, diagrams, or review package in chat without deciding
backed_by:
  - docs/adr/ADR-008-verification-acceptance.md
  - docs/adr/ADR-014-visible-product-language.md
  - docs/adr/ADR-004-autonomy-grades-risk.md
composes_into:
  - feature-delivery.md
---

# Workflow — present-information

Cross-cutting **presentation design** capability. Does not replace
[feature-delivery](feature-delivery.md): it is invoked on triggers from that
pipeline or on demand. Rule: [presentation-design](../rules/presentation-design.md).

**Default:** omit if there is no trigger. I0 never enters.

---

## Triggers

| Id | When | Typical source |
| --- | --- | --- |
| **A** | I2 after INTENT/PLAN if there is architecture or reasonable options | `decision-brief` / intent |
| **B** | Human asks to see proposal, options, spec/scope, or diagram, subject to I0–I2 proportionality | Active artifact |
| **E** | I2 before creating spec/task (includes Cold start) | Draft in chat/UI; no dossier yet |
| **C** | I1 close after VERIFY | Echo + test result (chat only) |
| **D** | I2 / I3 when D-K holds and D-H is pending | Brief executive dossier (changes, `vostok verify` matrix, independent audit verdict if `I2+` policy requires, residual risks, and explicit separation of `D-H` vs. deployment) |

---

## Steps

1. **Classify the trigger** (A/B/C/D/E). If none applies → omit.
2. **Is `decision-brief` needed?** Only in **A** (or B if options are requested and it does not exist yet). Write it with [decision-brief.md](../templates/decision-brief.md) **alongside the task**, once dossier creation is authorized. In E do not create the brief/dossier: draft the ephemeral proposal in chat/UI. If not needed → step 4.
3. **Complete the brief** before showing. No placeholders. If a material decision is missing and you cannot ask yet → stop (same as open question).
4. **Choose the form** according to the table in [presentation-design](../rules/presentation-design.md). If a table should appear and does not, fix the **source** (homogeneous labels, short phrases); do not invent another view.
5. **Show in chat** the view (Markdown / Mermaid / host native view). Diagram: nodes and arrows **exact** to the source; warn that the chat drawing is ephemeral. Without native view: readable Mermaid or, if the human wants to keep it, local HTML (not hosted).
6. **Separate decisions.** Material choices = open questions / stop. In **D**, ask for explicit acceptance of the result; do not say "accepted" or "completed."
7. **If the source changes** afterward → present again before continuing (A) or before D-H (D).
8. **Gate E — pre-creation:** present spec and initial task visibly and sufficiently complete (goal, scope, exclusions, milestones, observable criteria, and pending decisions) without writing them to the workspace. Ask specifically whether creating those files is authorized. If changes are requested, revise and present again; if not confirmed, stop without related writes. After confirmation, create only the shown artifacts, present them again, and verify fidelity. By default, request separate authorization for implementation; approving creation does not start EXEC. **Fast-track:** if the human explicitly gives combined authorization ("create and implement"), the agent verifies fidelity and proceeds directly to EXEC without an intermediate pause.

---

## Stops when

- Content of the brief or a criterion would have to be invented to "fill" the view.
- In E, there is no explicit creation confirmation or the human requests changes; the draft remains in conversation only.
- After creating, separate implementation authorization is missing (unless prior explicit combined authorization).
- A material choice in **A** remains unanswered and blocks EXEC.
- In **D**, the human has not accepted: the work remains `pending acceptance`, not `completed`.

---

## Out of scope for this workflow

- Deterministic Legacy-style `present` CLI (optional F2 phase).
- Recording D-H, authorizing deviations, or changing the grade.
- `specs/proposals/`, `evidence/` tree, own UI.
