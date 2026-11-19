---
id: evidence-record
type: template
revision: 1.0.0
updated: 2026-11-09
purpose: uniform serialized evidence for tasks and local audits
backed_by:
  - docs/adr/ADR-003-trust-evidence-enforcement.md
  - docs/adr/ADR-004-autonomy-grades-risk.md
  - docs/adr/ADR-005-intent-representation.md
  - docs/adr/ADR-007-agent-resources-layout.md
  - docs/adr/ADR-008-verification-acceptance.md
  - docs/adr/ADR-011-observability-decision-tracing.md
  - docs/adr/ADR-013-records-hooks-tool-safety.md
  - docs/adr/ADR-015-agreement-change.md
---

# Uniform evidence record — 1.0.0

Canonical representation and processing convention for new **optional** packs
persisted with a task. Placement rule: [`AGENTS.md`](../../AGENTS.md) and
[placement-and-sources](../rules/placement-and-sources.md). Does not reopen ADRs
or specs 0001/0002. The `specs/**/evidence/` tree and `specs/proposals/` are
**retired**; do not point there or recreate them.

A pack has **one `record.json`**, using the schema
[`evidence-record/1.0.0.schema.json`](evidence-record/1.0.0.schema.json).
`kind=task|audit` changes data and retention; the same validator and traversal
are used. `report.md`, verification-record, and verdict are human-readable views,
not parallel records or sources with independent states.

## Proportionality

- I0 keeps exclusively its single line; no dossier, criteria, D-K, or D-H.
  Ingestion may normalize it in memory to the `ephemeral` profile, never turn
  this convention into a requirement to save JSON for a typo.
- I1 keeps echo and minimal verification, ephemeral **in chat**. Do not create
  `record.json` on the daily path. If an I1 evidence needs processing, it is
  normalized in memory or temporary space; ingestion identity is not spec
  identity. Durable fixtures are examples, not a daily requirement. Closes
  without ceremonial acceptance.
- I2 keeps intent and revisions in `specs/`; every new persisted evidence pack
  uses this contract. The JSON cites the revision and the originals: it does not
  replace intent, ADR-011 trace, or human acceptance.
- I3 is not executed; exits to pending planning/handoff.

## Single shape and naming

```text
specs/<000N-slug>/tasks/<task-id>/verification/<record-id>/
  record.json
  report.md                       # optional
  artifacts/<name>.<ext>          # only material supporting criteria

.vostok/audits/<record-id>/
  record.json
  report.md                       # mandatory audit view
  artifacts/<name>.<ext>
```

In the Vostok source repository, `specs/CONVENTIONS.md` is a tree map, not an
operational rule. Forbidden: `specs/**/evidence/`.
`record_id = <id>__<YYYYMMDDTHHMMSSZ>__a<NN>`; lowercase ASCII IDs with hyphens,
attempt starting at 01. Folder = ID. `created_at` UTC with `Z`; ID seconds
match creation. New attempt = new pack; do not overwrite failures.
Does not vary by success, block, host, or grade. `fixture=true` identifies examples.

| Field | Verifiable relationship |
| --- | --- |
| `subject.agreement` | Preserved source agreement, trace/echo/spec type, identity and revision when they exist. `spec` here includes I2 intent; does not turn a task into a normative 000N spec. |
| `criteria` | Exact inventory and text of the agreement; check type, locator, changes, verifications, evaluation, and authority. |
| `changes` | Logical path, operation, before/after content, and affected criteria; audit describes inspected changes. Zero changes requires a reason. |
| `verifications` | Method, descriptive argv, environment, timestamps, timeout, result, exit/absence, final inputs, inline output or capture, provenance/trust/limits. |
| `artifacts` | IDs, paths relative to the pack, role, media type, SHA-256, and provenance. No downloaded URLs or external paths. |
| `additional_evidence` | Summary of per-criterion decisions and present/missing/blocked/unknown requirements. |
| `state`, `assessment`, `acceptance` | Execution, technical outcome, D-AC, coherence, and human act remain separate. |
| `audit`, `storage`, `limits` | Coverage/findings if audit, retention, and limits of the set. |

Content SHA: canonical UTF-8 JSON of `{path: sha256_final}` with sorted keys
and `,`/`:` separators without spaces; deletion = `null`.
`subject.content_revision = sha256:<digest>`. With zero changes it identifies `{}`,
**not** an entire codebase. Include relevant dependencies as inputs and declare
environmental conditions; this profile does not compute full impact.

The agreement may be preserved JSON with `kind`, `id`, `revision`, `criteria`
(id/text/type), goal, and includes/excludes; locator /criteria/N (same prefix
emitted by the validator). Native Markdown intent is also supported: scalar
`id`/`revision` in front matter and rows `| C1 | exact text |` or `| AC-01 | text |`
under `## Criteria…` (or `## Criterios…`); locator `line:N`. Without explicit
revision, use `sha256:<original bytes>`; do not invent rN. General YAML or
arbitrary Markdown is not parsed: unsupported formats are rejected and require an
explicit snapshot, preserving the original and the governing revision. A JSON
extraction alone only proves coherence against that snapshot, not fidelity to
another omitted document.

## Additional evidence: deciding per criterion

Each `criteria[].evidence_decision` declares `decision`, `triggers`, `reason`,
and `requirement_ids`. The summary is derived: `undetermined` if any criterion
cannot be decided; otherwise `required` if any requires it; otherwise `exempt`.
The validator checks that summary and reciprocal links.

| Decision | Condition and record |
| --- | --- |
| `exempt` | Minimal contrast covers the criterion; explain why in reason, without triggers/requirements. Does not exempt from verifying. The summary also requires `exemption_reason`. |
| `required` | There is an observable trigger and ≥1 requirement associated with the criterion, method/capture/expected decision, and actual state. |
| `undetermined` | Information is missing to decide; explicit reason and question/blocker. Never read as an exemption. |

Triggers: artifact required by criterion; behavior exceeding minimal contrast;
host/UI claim; failure/contradiction; semantic gap; missing dependency; content
change invalidating the contrast; unknown. UI captures are not required for a
text change, nor a transcript for a local check. A blocked requirement remains
required. A diagnostic with exit zero does not turn an unexecuted check into
an executed one. `present` needs artifacts as output of checks bound to the
criterion; its semantic sufficiency remains a judgment, not a hash.

## States and acceptance

D-AC serializes the five ADR-008 states as `no_evidence`, `linked`,
`validated`, `semantic_pending`, `decided` (outcome satisfied/rejected).
`exact_check` only supports satisfaction when the text is exactly the available
check of that revision; a proxy does not gain that authority. Human judgment may
use inspected artifacts without inventing a passing command. The validator
checks declared coherence, not meaning.

Work states: `incomplete`, `blocked`, `divergent`, `pending_acceptance`,
`completed`. `blocked` has reason, criteria, and step to unblock. A blocked pack
can be **consistent**; it does not constitute successful work.
`verification=passed` does not by itself accept or satisfy criteria.

I2 requires D-H for `completed`, bound to the reviewed work/revision/content;
human actor and artifact of the act, `guided` trust, not authenticated. A test
is not a human act. Explicit exceptions preserve the rejected/pending status;
they do not relabel it satisfied. I1 may close with applicable minimal
verification without requiring formal satisfied on all criteria or D-H.
Declarations, host signals, and ADR-011 trace keep their surfaces separate.

## Audits: local, temporary, and uniform

Single destination: `.vostok/audits/`, **non-portable** local state from ADR-007.
Does not replace the durable I2 dossier. No audit report, note, finding, capture,
listing, or index is published to Git or docs. `docs/audits/` remains ignored to
prevent reintroduction. Do not restore what was removed.

`audit` extension: target record and spec, revision and content, scope,
per-criterion coverage (checked/not_reviewed/blocked), findings with ID,
criteria, severity, status, evidence, consequence and recommendation, conclusion.
Not reviewing a criterion does not mean "no findings". Auditing does not accept
the task. The target source must be inside the pack along with its artifacts; it
is validated recursively by the same function, without executing its commands.

The report is an exact view of `record.json`, generated via
`--print-audit-report`; the validator rejects discrepancies. Fixed sections:
Object and revision; Scope and method; Coverage per criterion; Findings; Status
and blockers; Limits and retention. There is no other findings format.

TTL **7 days from created_at UTC**, explicit `expires_at`. Check expiration when
opening/closing review. **Manual** cleanup of the exact pack after checking
identity and expiration; no automatic cleanup. To continue later, create a new
attempt with a new date, reason, and reference to the previous one in limits; do
not rewrite the original date or silently extend its TTL. An expired pack may
still be intact: the validator publishes `expired`, it does not present it as
current. Its absence after cleanup ceases to be verifiable. Do not capture
secrets or internal prompts. If a task needs durable evidence, produce its own
check; do not copy the temporary verdict.

## Reusable processing

In the Vostok source repository, with Python ≥3.9 and the dependency pinned in `tools/requirements-evidence.txt`:

```sh
python3 -m venv /private/tmp/vostok-record-env
/private/tmp/vostok-record-env/bin/pip install -r tools/requirements-evidence.txt
/private/tmp/vostok-record-env/bin/python tools/validate_evidence.py <paquete>/record.json
```

Accepts multiple packs and `--repo-root <repo>` for the local audit root.
Same `validate_package(path, repo_root)` API for task/audit, without fixture
filter. Does not execute argv, open network, install hooks, or trust text as
proof. Checks version/schema, symlink-free local IDs/paths, integrity,
agreement, criteria, bounded content revision, final inputs, evidence decisions,
basic coherence, and audit report/TTL. Change path is logical: it does not read
or certify the production checkout.

Exit 0 means **consistent contract**, including blocked; exit 1 invalid pack;
exit 2 invocation/missing dependency. Output publishes real state, acceptance,
fixture, and expiration. It is not a compliance or approval gate.
Valid schema ≠ observed execution ≠ independence ≠ sufficiency ≠ D-H.

## Transition

Historical Markdown/JSONL/captures remain unchanged. New packs use 1.0.0; no
retrospective records are fabricated. Draft 0.1.0 is historical; the validator
rejects it as a non-current version. Human-readable templates point to this
contract, preserving specialized ADR-008 fields. Reuse only if revision,
object, content, and conditions remain verifiable (ADR-015); do not inherit
compliance or blindly rerun the entire suite.
