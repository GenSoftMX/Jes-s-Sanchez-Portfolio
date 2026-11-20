---
id: independent-preacceptance-audit
type: workflow
revision: 2026-11-18
purpose: policy-governed independent pre-acceptance audit before D-H for I2 and I3 work (successor to Spec 0021)
backed_by:
  - docs/adr/ADR-003-trust-evidence-enforcement.md
  - docs/adr/ADR-004-autonomy-grades-risk.md
  - docs/adr/ADR-008-verification-acceptance.md
composes_into:
  - feature-delivery.md
---

# Workflow — Independent Pre-Acceptance Audit (`I2+`)

**Separate auditor flow** distinct from the implementer's delivery thread. Successor to [i3-independent-preacceptance-audit](i3-independent-preacceptance-audit.md) (Spec 0021 remains frozen and untouched). Does **not** replace `VERIFY`, `D-K`, or human `D-H`, and is guided rather than host-`enforced`.

---

## 1. Trigger (Policy-Governed `I2+`)

Run before requesting `D-H` when **all** hold:
1. Governing work is classified **`I2`** or **`I3`** (or escalated via `D-S` / `vostok risk-check`).
2. Project autonomy policy (`.vostok/autonomy-policy.json`, default `required_from_grade: "I2"`) requires independent audit for this grade and no configured low-risk exemption applies.
3. Implementer `VERIFY` (`vostok verify`) and `D-K` are complete.

`I0` and `I1` do not invoke this gate.

---

## 2. Isolation Modes

| Mode | When | Declaration |
| :--- | :--- | :--- |
| `separate_agent_or_session` | Host allows launching a separate subagent/session with frozen inputs | Preferred |
| `separate_role_same_conversation` | Isolation unavailable | Allowed with limit declared visibly |
| `isolation_unavailable` | Cannot meaningfully separate role | Contrast still required; do not claim independence |

Explicit notice required in every report: **AI subagent audit ≠ human acceptance (`D-H`) and ≠ independent human review.**

---

## 3. Five Evaluation Axes & Independent Contrast

The auditor must inspect delivered files, `git diff`, contracts, and verification outputs directly — **never** relying solely on the implementer's summary:

1. **Functional correctness:** observable criteria (`AC-*` / `CA-*`) vs. delivered implementation.
2. **Architecture & boundaries:** adherence to `.vostok/architecture-contract.md`, `<module>/AGENTS.md`, and `vostok arch-check`.
3. **Security & safety:** path safety, secrets (`vostok risk-check`), input validation, and permission boundaries.
4. **Tests & verification:** genuine assertions (no trivial mocks), `executed` vs. `skipped` / `unavailable` honesty (`vostok verify`).
5. **Residual risks & limits:** documented unknowns and scope compliance.

---

## 4. Structured Verdicts & Blocking Policy

| Verdict | Meaning | Effect on `D-H` |
| :--- | :--- | :--- |
| **`approved`** | All criteria met; zero open findings | Proceed to `present-information` trigger **D** → ask `D-H` |
| **`approved_with_limits`** | Criteria met with minor/informational limits explicitly declared | Proceed to **D** → ask `D-H` with limits visible |
| **`rejected`** | Open `high`/`medium` findings or unmet criteria | **Block `D-H`** → scoped remediation → re-audit |
| **`insufficient_evidence`** | Missing or unverified evidence for material criteria | **Block `D-H`** → collect evidence → re-audit |

---

## 5. Required M3 Telemetry Block

Every audit report must record:
- `audit_duration_s` (wall-clock seconds)
- `isolation_mode`
- `verdict` (`approved | approved_with_limits | rejected | insufficient_evidence`)
- `findings_count_by_axis` (functional, architecture, security, tests, risks)
- `remediation_triggered` (`true | false`)
