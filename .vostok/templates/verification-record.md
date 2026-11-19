---
id: verification-record
type: template
revision: 2026-11-09
purpose: per-check verification evidence for feature-delivery VERIFICATION (D-AC input)
backed_by:
  - docs/adr/ADR-008-verification-acceptance.md
  - docs/adr/ADR-003-trust-evidence-enforcement.md
---

# Verification record

**I0/I1:** do not use this file. Command + result in chat is enough.  
**I2 / experiment:** human-readable form per check (or sections `V0`, `V1`, …). Does not replace
[criterion-states.md](criterion-states.md) (D-AC states); feeds it.  
Unknown ≠ success. Green test ≠ satisfied criterion ≠ D-H.

If persisted (I2 / experiment only): goes **with the task** under the single contract [evidence-record.md](evidence-record.md) (`record.json`, schema `1.0.0`); this template and [verdict.md](verdict.md) are human-readable views, not parallel records. Forbidden `specs/**/evidence/`; audits only in `.vostok/audits/` (gitignored).

## Minimal form (I2 or when chat is not enough)

```text
Verification
- Work / intent (id + revision): …
- Related criterion (ID + statement): …
- Command run: …
- Relevant environment (cwd, runtime, version if applicable): …
- Actual result (summary): …
- Exit code: …
- Capture: quoted snippet | path under artifacts/ …
- Verified files or revision: …
- Check evaluation: passed | failed | not run | not applicable | unknown
- Sufficient evidence for the criterion?: yes | no | partial — …
- Suggested D-AC state: …
- Repair applied (if any): none | …
- Limitations / unknowns: …
```

## Capture proportionality

| Situation | What to persist |
| --- | --- |
| I1 daily path | Nothing on disk; chat |
| I2 check passes and summary suffices | Exit code + 1–3 lines in this record or in `record.json` |
| Check fails or repro is needed | File under task's `artifacts/` |
| Host transcript / JSONL | Only if an activation AC asks for it → local `raw/`; **not** proof of criterion |

## Standardized Verification Matrix (`vostok verify` / Spec 0034)

Distinguish explicitly between `executed`, `skipped`, `failed`, and `unavailable`. Never report `skipped` or `unavailable` as `executed`.

| Category | Status (`executed \| skipped \| failed \| unavailable`) | Scope / Command | Limitations / Notes |
| :--- | :--- | :--- | :--- |
| `unit` | … | … | … |
| `integration` | … | … | … |
| `contract` | … | `vostok contracts-check` | … |
| `e2e` | … | … | … |
| `static_lint_types` | … | … | … |
| `security_secrets` | … | … | … |
| `architecture` | … | `vostok arch-check` | … |
| `docs_sync` | … | `vostok docs-impact` | … |

- **M1 Telemetry (Rework):** `remediation_cycles: <int>`, `corrective_churn_ratio: <float | unavailable>`.

## Mandatory distinctions

| Plane | Question |
| --- | --- |
| Test execution | Was the command run? |
| Technical outcome | Exit code / assertions? |
| Sufficient evidence | Does the capture cover the criterion? |
| Criterion satisfaction | Sufficient authority for "satisfied"? |
| D-K coherence | Does the set support closure? (I2) |
| D-H | Did an authorized person accept? (human only) |

## Short rules

1. No command or review when the criterion requires it → do not mark verified.
2. Do not delete failed records to simulate a perfect sequence.
3. Bounded repair; each rerun is a new record or dated appendix.
4. Unverifiable criterion → declare it; do not inflate "satisfied".
5. Persist only what supports a claim.
6. Limit disclaimers: once per pack; do not re-state them on every check.
