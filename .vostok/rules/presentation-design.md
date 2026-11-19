---
id: presentation-design
type: rule
revision: 2026-11-16
scope: chat and human-facing presentation of scope, options, diagrams, and results
authority: Instruction Authority (project)
backed_by:
  - docs/adr/ADR-008-verification-acceptance.md
  - docs/adr/ADR-014-visible-product-language.md
  - docs/adr/ADR-004-autonomy-grades-risk.md
---

# Information Presentation Design

The human should not have to open the dossier to know what is going to be built, what was decided, or what remains to be accepted. When the grade and trigger call for it, a readable view is shown in chat. The dossier (echo, intent, brief, states) remains the source.

## Mandatory

1. **Showing ≠ deciding ≠ accepting.** Presenting does not record approval, does not authorize deviations, and does not complete D-H. Viewing the presentation does not close the work.
2. **Source first.** The view comes from the echo (I1), from the intent / `decision-brief` / states / D-K (I2), or from the on-demand request. If the source changes, present it again. Do not add content that is not written in the source (except structural labels: section headings, "recommended").
3. **Consultation with motivated recommendation:** When consulting or asking the human about design choices, technical forks, or trade-offs, the consultation **must not be passive or neutral without criteria**: it must always be accompanied by a **motivated recommendation** based on project suitability analysis (lower technical debt, lower risk, alignment with ADRs, operational simplicity). Visible format: `(Recommended: Option X because ...)`. The human always retains decision-making sovereignty.
4. **Persisting the decision as evidence:** When the human responds and approves an option (or chooses another alternative), the rationale for why it was adopted and the discarded alternatives **must be recorded as observable evidence**:
   - **I2 / I3:** record in the dossier's `decision-log` (the task's [`decision-brief.md`](../templates/decision-brief.md) or `closure/decision-log.md`).
   - **I1:** record the decision and reason in the echo / verification trace in chat.
   - **I0:** omitted (no material decisions or ceremony).
5. **Form follows content** (choose the smallest sufficient form):

   | Content | Form |
   | --- | --- |
   | Options with homogeneous labels (what it is / pros / cons) | Comparison table + **Motivated recommendation** |
   | Acceptance criteria or VERIFY | Checklist or criterion → result table |
   | Components and relationships | Diagram + "who connects to whom" list |
   | Human choices | Questions with options + recommended option (include "do not change" / "later" if applicable) |
   | Explanations / assumptions | Short prose |
   | Coherence report (I2) | Three planes in plain prose |
   | Acceptance request (`I2+` / Trigger D) | Brief executive dossier (changes, verification matrix, independent audit verdict & residual risks) + explicit `D-H` question (separated from deployment) |
   | Material turn close | Continuity: done / what's next / who acts ([developer-continuity](developer-continuity.md)) |

6. **Proportionality.**
   - **I0:** do not present; only the one-line trace.
   - **I1:** the echo already declares scope; at close, criteria + proof in minimal form. If a consultation was agreed upon, include the adopted decision in chat. No `decision-brief` or presentation dossier.
   - **I2:** full spec/task proposal visible before creating the dossier (trigger E); brief + presentation with motivated recommendation before building if there is architecture or reasonable options; record of agreed decisions in the dossier; before D-H, result + coherence view.
7. **Plain language** ([visible-language](visible-language.md)): no D-* jargon by default; do not inflate guarantees (`enforced`, "completed" merely for having shown).
8. **Medium.** Prefer the host's native view if it renders diagrams. Otherwise: Markdown / Mermaid in chat. A **local** HTML page only if the diagram needs to be preserved; do not publish to external services unless the human asks for it.
9. **Diagram fidelity.** Same nodes, arrows, and labels as the source. Warn that the chat drawing is ephemeral.
10. **Do not present a brief with unfilled template placeholders**: complete it or ask; do not improvise the view.

## Limit

This rule does not introduce UI, dashboard, or runtime. It does not redefine D-K or D-H. It does not require a deterministic CLI (optional future phase). Procedure: [present-information](../workflows/present-information.md).
