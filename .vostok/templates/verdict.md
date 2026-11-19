---
id: verdict
type: template
revision: 2026-11-09
purpose: slim index of claims→evidence for experimental evidence packs (E-FD-*, Spec AC)
backed_by:
  - docs/adr/ADR-003-trust-evidence-enforcement.md
  - docs/adr/ADR-008-verification-acceptance.md
---

# Verdict (claims index)

**Forbidden in I0/I1.** Only experimental run or I2 that needs a claim→proof
index **with the task** (`specs/<000N…>/tasks/<task-id>/…`). Do **not** recreate `specs/**/evidence/`.  
Does **not** replace [verification-record.md](verification-record.md). **Not** D-H or owner acceptance.

If persisted with `record.json`, this template is a human-readable view of the same pack under [evidence-record.md](evidence-record.md) (schema `1.0.0`) — never a second record or substitute for D-H. Historical formats are preserved without retrospective conversion; audits only in `.vostok/audits/`.

```text
Verdict
- Run / date / surface (host): …
- Governing work (echo or intent): …
```

| Claim | AC / criterion | Outcome | Evidence |
| --- | --- | --- | --- |
| … | … | supports \| does not support \| blocked \| not claimed | path or check id (e.g. V1, captures/…) |

```text
Limits (once)
- What is not claimed (e.g. AC-03, enforced, D-H, native S2): …
- raw/ (if any): host annex; not proof of product criterion on its own
```

## Short rules

1. Each row must point to real evidence (record, capture, or review), not just narrative.
2. "Not claimed" / "blocked" are valid outcomes; do not pad them as success.
3. Do not duplicate the body of each verification-record here.
