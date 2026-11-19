---
id: spec-closure-claims-matrix
type: template
revision: 2026-11-09
purpose: claims/AC matrix for principal-spec closure
backed_by:
  - .vostok/workflows/spec-closure.md
  - docs/adr/ADR-008-verification-acceptance.md
---

# Claims / AC matrix — Spec {{000N}} closure

Copy to `specs/{{000N-slug}}/closure/claims-matrix.md`.

Threshold: …  
Date: …

| ID | Question | Surface | Outcome | Anchor | Limit |
| --- | --- | --- | --- | --- | --- |
| Claim A / AC-… | … | repo \| Claude TUI \| … | supports \| no \| partial \| n/a | path under `retained/` or reproducible quote | … |
| Claim B / AC-… | … | … | … | … | … |
| Claim C / AC-… | … | … | … | … | … |
| AC-… (conditional) | … | … | conditional·done \| not run \| n/a | … | does not block validated |

## Rules

1. `supports` ⇒ anchor present in `closure/retained/` **or** reproducible quote in this cell (command, exit, 1–3 lines).
2. Contrast ≠ pilot.
3. Deleted anchor ⇒ row in `deleted-inventory.md`; this cell no longer asserts currency via a phantom path.
4. Unknown ≠ success. Green test ≠ all claims.
