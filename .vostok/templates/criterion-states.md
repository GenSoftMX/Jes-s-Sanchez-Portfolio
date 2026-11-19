---
id: criterion-states
type: template
revision: 2026-11-06
purpose: per-criterion D-AC states and separate human acceptance (D-H)
backed_by:
  - docs/adr/ADR-008-verification-acceptance.md
  - docs/adr/ADR-003-trust-evidence-enforcement.md
  - docs/adr/ADR-014-visible-product-language.md
---

# Criterion and acceptance states (I2)

Recorded alongside the task's intent (`specs/<000N-slug>/tasks/<task-id>/criteria.md`). Cites the **governing revision** (`rN`) of [`intent.md`](intention.md). Does not rewrite the intent.

## How the 3 levels connect when closing an I2 task

To avoid confusion when closing an `I2` task, always distinguish these three levels in order:

```text
Level 1: State of each criterion (C1, C2…)
   (Did this revision's check run? → moves to "validated per available checks")
        ↓
Level 2: Coherence report (D-K)
   (Does the dossier hold together and is no pending criterion presented as met? → "supports closure")
        ↓
Level 3: Work state + Human acceptance (D-H)
   - Before the human responds: work state = "pending acceptance" ("ready for review")
   - Only after the human explicitly accepts (D-H): work state = "completed"
```

## Five states (one per criterion)

Use **exactly** one of these per criterion. Do not invent a sixth.

| State | Means | Does not mean |
| --- | --- | --- |
| no evidence | No link to an artifact from this revision | Failure of the work by itself |
| linked | Link exists; not yet cross-checked | Compliance / "ready" |
| validated per available checks | This revision's check passed; evidence is not just agent narration | **satisfied** |
| pending semantic evaluation | The link or check does not exhaust the meaning, or authoritative judgment is missing | Silently met |
| satisfied or rejected | Decision with sufficient authority (two outcomes of the same state) | That a green gate is always enough |

Short rules:

1. A link or a green test does **not** promote to "satisfied" on its own.
2. "Validated" is **not** written or presented as "satisfied" in the MVP (except in the narrow case where the criterion text **is** exactly that already-validated check).
3. "Rejected" is not "satisfied". Without an authorized exception, it is non-compliance.
4. Unknown ≠ success. Absence of evidence ≠ criterion met.

```text
# Criteria — <identity> (revision rN)

| ID | State | Evidence (path or quote) | Notes |
| --- | --- | --- | --- |
| C1 | no evidence \| linked \| validated per available checks \| pending semantic evaluation \| satisfied \| rejected | … | … |
```

## Coherence report (D-K; does not accept)

Optional, when the grade asks for it. Three planes of **D-K**. It is **not** human acceptance. It does **not** issue "accepted" as its own decision.

```text
Coherence (D-K)
- Structural: holds \| does not hold — …
- Compliance: supports closure \| does not support — …
  (a criterion in no evidence / linked / pending semantic evaluation does not count as met;
   validated ≠ satisfied)
- Acceptance mirror: absent \| pending \| accepted \| accepted with visible exception \| rejected
  (only reflects D-H; it is not a second decision)
```

## Outcome acceptance (D-H; distinct human act)

Only an **authorized person**. The agent does not issue, infer, or simulate it.

- Bound to the reviewed **work**, **revision**, and **outcome**.
- Separate from each criterion's state, the D-K report, and the **overall work state**.
- Without D-H: the work does **not** become `completed`. If the outcome is prepared for the person → work state `pending acceptance`. If D-K does not support closure (e.g. criteria still in no evidence / linked / pending semantic evaluation) → `incomplete` (or another appropriate work state), not "pending acceptance" by default.
- May, in the **same** act, judge pending semantic items and authorize visible deviations/exceptions. That does **not** rewrite the revision that governed implementation or silently turn a pending or rejected item into "satisfied".

```text
Outcome acceptance
- State: pending \| accepted \| accepted with visible exception \| rejected
- Who (person): … / (empty if pending)
- When: … / (empty if pending)
- Reviewed work / revision / outcome: …
- Judgments or exceptions in this act (if applicable): …
- Record: guided (no authenticated identity in the MVP)
```

If the "Who" field is filled in by the agent without an explicit human message, the record does **not** count as acceptance.
