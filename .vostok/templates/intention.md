---
id: intention
type: template
revision: 2026-11-06
purpose: I2 persisted intent under specs/
backed_by:
  - docs/adr/ADR-005-intent-representation.md
  - docs/adr/ADR-007-agent-resources-layout.md
  - docs/adr/ADR-014-visible-product-language.md
---

# Persisted intent (I2)

Use **before** the first material change in I2 work. Lives as a **task** under its parent spec: `specs/<000N-slug>/tasks/0001-<slug>/intent.md` (sequential order `000N-<slug>`; never as a standalone spec at the root of `specs/`). Not a product Spec, nor I3 plan/tasks, nor outcome approval.

If there is material ambiguity (a boundary or criterion must be invented): **stop** and ask. The answer updates the text; that is **not** outcome acceptance.

Preserve the revisions that governed changes. An authorized requirement change opens a **new revision**; do not silently rewrite the revision that already governed a slice.

## Revision preservation

1. The revision governing the current work is declared in front matter (`revision: rN`) and in the body.
2. Before opening `rN+1`, **preserve** the text of `rN` without editing it afterward (e.g. copy to `revisions/rN.md` or `intent-rN.md` in the same work directory).
3. The already-implemented slice remains bound to the revision that governed it. Subsequent work cites the new revision.
4. Do not "fix" the past to match the diff.

The `status` field is the **overall work state** (Product Definition / ADR-008). It is not a criterion D-AC state or the D-H outcome.

Allowed values (exactly these five; do not invent others):

| Work state | When |
| --- | --- |
| incomplete | Missing scope, evidence, or compliance (D-K) does not support closure |
| blocked | Stopped without a usable governing revision, or missing an unblocking answer |
| divergent | Unauthorized out-of-scope diff/behavior |
| pending acceptance | Outcome prepared for D-H; "ready for review" ≠ completed |
| completed | D-H accepted and no pending criterion is counted as met |

```text
---
id: 0001-<slug>
title: <short title>
revision: rN
grade: I2
status: incomplete | blocked | divergent | pending acceptance | completed
created: YYYY-MM-DD
updated: YYYY-MM-DD
supersedes_revision: rN-1 | null
---

# Intent — <title>

Governing revision: **rN**.
Preserved revisions: `revisions/r1.md`, … (if any)
Work state: … (one of the five; distinct from D-AC and D-H)

## Goal
…

## Includes
- …

## Excludes
- …

## Criteria (identifiable)
| ID | Observable condition |
| --- | --- |
| C1 | … |
```

Notes:

- Each criterion names an **observable** condition. If it names nothing observable, it does not govern: rewrite it or ask.
- Reusable rules are not copied here to turn them into criteria.
- Diff, evidence, and handoff **cite** this revision; they do not replace it.
- There is **no** `approved` / `implemented` state for intent. Acceptance of the **outcome** is D-H (a separate record). `completed` as a work state requires D-H; it is not inferred from a task's `done`.
- Do not use `in_progress`, `rejected`, or other names outside the work state table.
- Plain language in chat; this template is the durable record.
