---
id: evidence-pack
type: template
revision: 2026-11-09
purpose: layout and retention for persisted verification with a task (no specs/**/evidence/)
backed_by:
  - docs/adr/ADR-003-trust-evidence-enforcement.md
  - docs/adr/ADR-007-agent-resources-layout.md
  - docs/adr/ADR-008-verification-acceptance.md
---

# Evidence pack (convention)

Operational rule: [`AGENTS.md`](../../AGENTS.md) + [placement-and-sources](../rules/placement-and-sources.md).  
There is **no** `specs/**/evidence/` tree (retired). Persistence, if applicable, lives with the **task**.

Three layers. Do not mix roles in the same index file.

| Layer | When | Content |
| --- | --- | --- |
| **A — Operational** | Daily I0/I1 | Chat only (echo + command). **No** pack on disk |
| **B — Persisted** | I2 or experiment that must leave a trace | One `record.json` (+ views) **under the task** |
| **C — Host signal** | Only if an AC requires it | Transcript / JSONL / TUI → `raw/` (local / gitignored) |

## Machine-readable contract

For new persisted packs (I2), [evidence-record.md](evidence-record.md) (`record.json`, schema `1.0.0`) governs; `verification-record` and `verdict` are human-readable views. I0/I1 require no mandatory JSON. Audits exclusively in `.vostok/audits/` (gitignored).

## Layout (if persisted)

```text
specs/<000N-slug>/tasks/<task-id>/
  intent.md | criteria.md | …     # task agreement
  verification/                   # optional; free name as long as it is under the task
    <record-id>/
      record.json                 # if using contract 1.0.0
      report.md                   # optional
      artifacts/
      raw/                        # gitignored; only if the AC requires it
```

A standalone `verification-record.md` in the task without a subfolder is also valid if it suffices for the criteria. Recreating `specs/<000N…>/evidence/` is **forbidden**.

## Retention

| Include | Avoid |
| --- | --- |
| Record / captures supporting a claim | Full harness transcript |
| A session diff tied to a criterion | Git hygiene without a claim |
| Limits once | Repeated disclaimers |

**Persist only what supports a claim.**

## Proportionality

| Grade | Typical minimum |
| --- | --- |
| I0 | One line |
| I1 | Echo + verification-record (ephemeral unless the owner asks to persist) |
| I2 | Intent/criteria in the task + record if proof must be kept; human D-H separate |

## What this template does not decide

It does not change ADR-003/008, does not invent `enforced`, does not authenticate D-H, and does not mandate a pack on every routine run.
