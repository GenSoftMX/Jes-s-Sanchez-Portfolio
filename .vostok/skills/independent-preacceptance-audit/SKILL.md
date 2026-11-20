---
name: independent-preacceptance-audit
description: >-
  Policy-governed separate auditor for I2+ work before D-H (5 axes, 4 structured
  verdicts, M3 telemetry). Canonical: .vostok/workflows/independent-preacceptance-audit.md.
---

# Independent Pre-Acceptance Audit (`I2+`)

Follow the canonical workflow [independent-preacceptance-audit.md](../../workflows/independent-preacceptance-audit.md).

## Mandatory Obligations

1. Confirm trigger (`I2` or `I3` per `.vostok/autonomy-policy.json`, default `required_from_grade: "I2"`).
2. Declare isolation mode (`separate_agent_or_session` preferred).
3. Inspect delivered files, diffs, contracts, and test outputs directly; never trust the implementer's summary alone.
4. Evaluate all 5 axes (functional, architecture, security, tests, residual risks) and emit one of the 4 structured verdicts (`approved`, `approved_with_limits`, `rejected`, `insufficient_evidence`) plus the `M3` telemetry block (`audit_duration_s`, `findings_count_by_axis`).
5. Block `D-H` on `rejected` or `insufficient_evidence` until remediation + re-audit (or explicit human exception). Never claim human review or host `enforced`.
