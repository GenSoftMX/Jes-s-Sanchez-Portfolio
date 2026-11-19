---
id: spec-closure
type: workflow
revision: 2026-11-09
purpose: standard closure of a principal spec (000N) — constancy, anchors, sweep
backed_by:
  - docs/adr/ADR-003-trust-evidence-enforcement.md
  - docs/adr/ADR-008-verification-acceptance.md
  - docs/adr/ADR-011-observability-decision-tracing.md
  - docs/adr/ADR-007-agent-resources-layout.md
templates:
  - ../templates/spec-closure.md
  - ../templates/spec-closure-claims-matrix.md
  - ../templates/spec-closure-decision-log.md
  - ../templates/spec-closure-deleted-inventory.md
---

# Workflow — principal spec closure (standard)

**Rare event.** Closes the **increment** of a `000N-…` spec with a portable
record. **Not** the short path of [feature-delivery](feature-delivery.md).
**Not** D-H of an I2 task. **Does not** recreate `specs/**/evidence/`.

Placement rule: [placement-and-sources](../rules/placement-and-sources.md)
and [`AGENTS.md`](../../AGENTS.md).

---

## When

Owner asks to close the increment, **or** the spec's technical threshold is
sustained (e.g., 0002 Claims A∧B∧C) and the owner accepts (or accepts with limits / rejects).

## Three layers

| Layer | What | Git |
| --- | --- | --- |
| **D** Decision | Owner act, limits, baseline, tuple, log | Always |
| **A** Anchor | Minimal proof per cited claim | Selective (`closure/retained/`) |
| **R** Residue | raw/, transcripts, duplicate packs, smokes | Delete after promoting |

## Mandatory layout on closure

```text
specs/<000N-slug>/
  CLOSURE.md
  closure/
    decision-log.md
    claims-matrix.md
    deleted-inventory.md
    retained/                 # only if a separate file is needed
```

Templates: [spec-closure.md](../templates/spec-closure.md) and siblings
`spec-closure-*.md`.

## Procedure

1. **Freeze** — do not delete yet; gather acts and candidate anchors.
2. **Draft D** — `CLOSURE.md` + `decision-log.md` + `claims-matrix.md`.
3. **Promote A** — copy to `closure/retained/` only what a "holds" row requires.
4. **Verify** — every "holds" has a present anchor or reproducible citation;
   limits written; baseline cited; one sentence in compat if applicable.
   Optional in the source repository, if available: `python3 tools/check_spec_closure.py specs/<000N-slug>`.
5. **Owner act** — authorized human declares in `CLOSURE.md` (verbatim).
   The agent **never** invents this block.
6. **Sweep R** — delete according to `deleted-inventory.md` (fill out the inventory
   **before** or in the same commit as the deletion).
7. **Mark** — frontmatter of `spec.md`: `closed` | `closed_with_limits` |
   `rejected`. Index (`AGENTS.md` / `README`) points to `CLOSURE.md`.
8. **Tag (optional)** — `vostok-000N-closed-<date>` cited from `CLOSURE.md`.

## Frontmatter states (`spec.md`)

| status | Meaning |
| --- | --- |
| `approved` | Text approved; implementation may continue |
| `validated` | Technical threshold sustained; owner act pending or not yet issued |
| `closed` | Owner accepted; dossier present; residue swept |
| `closed_with_limits` | Same, with limits in `CLOSURE.md` |
| `rejected` | Owner rejected; dossier equally mandatory |

`closed` / `closed_with_limits` / `rejected` **require** the layout above.

## Short rules

1. Promote **before** deleting. Without a deletion inventory → do not sweep.
2. Deleted path ≠ current proof.
3. Contrast ≠ pilot in the matrix.
4. Acceptance of the increment ≠ D-H of `tasks/<id>/`.
5. Provenance of the owner act = `guided` (ADR-003); not `authenticated`.
6. Do not put this workflow into daily I0/I1.
7. **Absolute immutability after closure:** Once marked as `closed`, `closed_with_limits`, or `rejected`, the entire `specs/<000N-slug>/` subtree is frozen in read-only mode. No new tasks may be added, nor `spec.md`, `plan.md`, `tasks.md` modified, nor assertions or code in `experiments/` or `fixtures/` altered. Historical experiments are frozen verification anchors, not live continuous-regression suites.
8. **Non-retrospection (Supersession Principle):** If a later spec alters or refines concepts from an earlier one, or if an erratum is discovered in a closed spec, **never** retroactively edit the closed dossier: the evolution is documented in the new successor spec or in the active task.

## Out of scope

Runtime, `enforced` hooks, journal, authenticated identity, `evidence/` tree,
acceptance only under `docs/audits/` or `.vostok/audits/`.
