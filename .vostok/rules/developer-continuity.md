---
id: developer-continuity
type: rule
revision: 2026-11-16
scope: chat and human-facing closes after material agent turns
authority: Instruction Authority (project)
backed_by:
  - docs/adr/ADR-014-visible-product-language.md
  - docs/adr/ADR-009-handoff-recovery.md
  - docs/adr/ADR-008-verification-acceptance.md
---

# Visible Developer Continuity

The developer should never be left wondering **what comes next**. After a material
turn, the chat closes with continuity in plain language
([visible-language](visible-language.md)). Guided — not `enforced` by the host.

## Mandatory

1. **Continuity close** at the end of every material response (where there was an edit,
   verification, stop, gate, or blocker). Include, in brief prose:
   - **Done** — what happened in this turn (one sentence).
   - **Next** — concrete action that follows.
   - **Who acts** — developer, agent, or both.
   - **If applicable** — decision with options, or blocker (what is missing: API key,
     login, permission, acceptance, etc.).
2. **Do not invent** the next step: it must come from the scope, dossier, or
   request. If a material decision is missing → formulate a structured question
   with options (including "later" / "do not change" when helpful) and always
   accompany it with a **motivated recommendation** based on the project's technical
   suitability ([presentation-design](presentation-design.md)). Once the user confirms
   the choice, persist the decision and its rationale as observable evidence
   (in `decision-log` for I2/I3, or in the trace/echo for I1).
3. **Do not substitute gates:** requesting D-H, authorization to create/implement, or
   human help remains an explicit question; the continuity close names it, it does not
   treat it as done.
4. **Proportionality:**
   - **I0:** a one-line trace is enough; do not require the Done/Next block
     unless something remains pending for the human.
   - **I1:** after editing/verifying, close with Done + Next (+ Who). If a decision
     was agreed upon in the turn, leave a brief record of the agreement and its reason.
   - **I2 / I3 (slice):** same, and name the pending gate (creation,
     implementation, D-H, I3 audit, remediation) when applicable, recording
     accepted decisions in the dossier's `decision-log`.
5. **Handoff** ([handoff.md](../templates/handoff.md)) remains the artifact
   between sessions; this close is the **in-chat** feedback for each turn.

## Examples (form, not a rigid template)

| Situation | Typical close |
| --- | --- |
| I1 done, no commit requested | Done: … Next: should I commit or continue with X? Who: you decide. |
| Technical consultation / decision | Done: analyzed alternatives A and B. Next: should we adopt Option A? (Recommended: A because it minimizes debt). Who: you decide. (Evidence will be recorded upon agreement). |
| Missing secret / API key | Done: prepared the config. Next: paste the API key in … (or authorize another path). Who: you. Blocker: cannot authenticate without the key. |
| I2 ready for D-H | Done: VERIFY/D-K ready. Next: do you accept the result? Who: you (D-H). |
| Remediation | Done: fixed findings N. Next: re-verify / re-audit / re-present. Who: agent, then you if D-H applies. |
| I0 typo | `I0` — fixed "…" in `path`. (no ceremony) |

## Limit

Does not introduce UI, dashboard, or runtime. Does not redefine D-H or handoff. Does not claim
that the host enforces the close. Compatible with [presentation-design](presentation-design.md)
(presenting ≠ deciding ≠ accepting).
