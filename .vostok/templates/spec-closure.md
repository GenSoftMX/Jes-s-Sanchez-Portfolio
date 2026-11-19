---
id: spec-closure
type: template
revision: 2026-11-09
purpose: durable closure record for a principal spec (000N) — index + owner act
backed_by:
  - docs/adr/ADR-003-trust-evidence-enforcement.md
  - docs/adr/ADR-008-verification-acceptance.md
  - docs/adr/ADR-011-observability-decision-tracing.md
  - .vostok/workflows/spec-closure.md
---

# Closure — Spec {{000N-slug}}

Copy to `specs/{{000N-slug}}/CLOSURE.md` when closing the increment.
Procedure: [spec-closure workflow](../workflows/spec-closure.md).
Sheets: [claims-matrix](spec-closure-claims-matrix.md),
[decision-log](spec-closure-decision-log.md),
[deleted-inventory](spec-closure-deleted-inventory.md).

| Field | Value |
| --- | --- |
| Date | YYYY-MM-DD |
| Spec | `specs/{{000N-slug}}/` |
| Outcome | `closed` \| `closed_with_limits` \| `rejected` |
| Applied threshold | e.g. Claims A∧B∧C (§…) |
| Baseline | commit `…` / tag `…` |
| Tuple | host · version · surface (if applicable) |
| Compat | path to current row in `docs/compatibility/` |

## Limits (what is not claimed)

- …

## Dossier pointers

After copying this file to `CLOSURE.md`, the sheets live under `closure/`.
Here destination paths are in code (they are not template imports); sibling
templates are linked for anyone editing the portable package.

- Decisions: `closure/decision-log.md` (template [spec-closure-decision-log.md](spec-closure-decision-log.md))
- Matrix: `closure/claims-matrix.md` (template [spec-closure-claims-matrix.md](spec-closure-claims-matrix.md))
- Deletions: `closure/deleted-inventory.md` (template [spec-closure-deleted-inventory.md](spec-closure-deleted-inventory.md))
- Anchors: `closure/retained/` (if applicable)

## Owner act (mandatory for closed / closed_with_limits / rejected)

Provenance: explicit declaration. It is **not** a cryptographic signature or
`authenticated` identity. The agent does **not** issue this block.

> "…verbatim owner text…"

| Field | Value |
| --- | --- |
| Declared by | owner |
| Date | YYYY-MM-DD |
| Scope | spec increment / with limits listed above |
