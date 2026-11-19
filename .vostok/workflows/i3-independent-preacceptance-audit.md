---
id: i3-independent-preacceptance-audit
type: workflow
revision: 2026-11-15
purpose: mandatory separate auditor flow before D-H for I3 work that reaches acceptance
backed_by:
  - docs/adr/ADR-003-trust-evidence-enforcement.md
  - docs/adr/ADR-004-autonomy-grades-risk.md
  - docs/adr/ADR-008-verification-acceptance.md
composes_into:
  - feature-delivery.md
---

# Workflow — I3 independent pre-acceptance audit

**Separate auditor flow.** Distinct from the implementer’s feature-delivery
thread. Does **not** replace VERIFY, D-K, or D-H. Does **not** authorize silent
I3 execution. Guided procedure — not host `enforced`.

**Default:** omit unless the [Trigger](#trigger) holds. I0 / I1 / I2 **never**
take this mandatory gate.

Skill: [i3-independent-preacceptance-audit](../skills/i3-independent-preacceptance-audit/SKILL.md).
Contrast technique may reuse [technical-review](../skills/technical-review/SKILL.md)
**under the auditor role**, not as a substitute for this gate.

---

## Trigger

Run only when **all** hold:

1. Governing work is classified **I3** (or escalated to I3) on the record.
2. A human authorized a later **execution slice** that produced an implementable
   result under a named revision (I3 still stopped for plan first).
3. Implementer VERIFY and D-K are done and would otherwise lead to asking for D-H.

If the trigger fails: do not ask for D-H under an I3 label; do not invent an
audit to unblock execution.

---

## Isolation modes

| Mode | When | What to declare |
| --- | --- | --- |
| `separate_agent_or_session` | Host allows another agent/session with frozen inputs | Prefer this |
| `separate_role_same_conversation` | Isolation unavailable | Allowed with the limit **visible** |
| `isolation_unavailable` | Cannot separate role meaningfully | Report; still run contrast; do **not** claim independence |

Never invent “independent review,” human review, or `enforced`. Presence of
this file ≠ discovered ≠ loaded ≠ applied (ADR-007).

---

## Inputs (frozen for the audit)

- Governing intent / requirements / criteria (named revision).
- Diff or change set under review.
- Implementer VERIFY result and D-K report (as data, not as verdict to rubber-stamp).

---

## Steps

1. **Confirm trigger** and declare isolation mode before judging.
2. **Assume auditor role** (prefer separate agent/session). Do not continue as
   the implementer narrating self-approval.
3. **Contrast** each observable criterion / requirement against the delivered
   change. Green tests alone do not satisfy a semantic criterion.
4. **Emit one of:**
   - `clean` — no open findings that block acceptance.
   - `findings` — actionable list (location, condition, impact, evidence).
   - `isolation_unavailable` — contrast still required; independence not claimed.
5. **If `findings`:** enter remediation scoped to the list
   ([feature-delivery](feature-delivery.md) remediation cycle). After fixes,
   **re-run this workflow** before present-information D / D-H.
6. **If `clean` (or human names an explicit exception):** proceed to
   [present-information](present-information.md) trigger **D**, then ask for
   **D-H**. Do **not** ask for D-H while findings remain open unless the human
   explicitly authorizes a named exception.

---

## Outputs

Report in chat (persist with the task only if I2-style dossier already exists
for the execution slice):

- Isolation mode declared.
- Criteria / requirements checked vs result.
- Status: `clean` | `findings` | `isolation_unavailable`.
- Findings list or “none open.”
- Explicit statement: this audit ≠ D-H.

---

## Remediation link

Open findings → fix → VERIFY → update criterion states → **re-audit (this
workflow)** → only then present-information D / ask D-H.

Skipping re-audit after remediation is a procedure violation.

---

## Out of scope

- Mandatory use on I0 / I1 / I2.
- Replacing D-K or D-H.
- SaaS auditor, daemon, or claim of verified independence without host signal.
- Executing I3 without the initial stop / plan / human authorization of slices.
