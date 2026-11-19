---
id: feature-delivery
type: workflow
revision: 2026-11-16
purpose: canonical operational procedure INTENT→…→HANDOFF for software feature delivery (proportional)
backed_by:
  - docs/adr/ADR-001-product-identity.md
  - docs/adr/ADR-002-integration-model.md
  - docs/adr/ADR-004-autonomy-grades-risk.md
  - docs/adr/ADR-005-intent-representation.md
  - docs/adr/ADR-006-context-engineering.md
  - docs/adr/ADR-008-verification-acceptance.md
  - docs/adr/ADR-009-handoff-recovery.md
composes:
  - catalog-minimum.md
  - context-selection-step.md
  - present-information.md
  - feature-delivery-detail.md
  - i3-independent-preacceptance-audit.md
---

# Workflow — feature-delivery (canonical)

**Single procedural source** of the operational pipeline. Native projections
only point here; they **do not** rewrite stages. It is not a runtime or orchestrator.

**Default:** skip a stage if there is no trigger. The best flow is the one that
is not executed. Logical order (reference, **not** a chat checklist):

```text
INTENT → CONTEXT → PLAN → EXECUTION → VERIFICATION → ACCEPTANCE → HANDOFF
```

Apply [grades-proportionality](../rules/grades-proportionality.md). Rules:
[evidence-honesty](../rules/evidence-honesty.md),
[visible-language](../rules/visible-language.md),
[presentation-design](../rules/presentation-design.md),
[placement-and-sources](../rules/placement-and-sources.md),
[context-selection](../rules/context-selection.md).

Composition: [catalog-minimum](catalog-minimum.md),
[context-selection-step](context-selection-step.md),
[present-information](present-information.md)
(presentation triggers A–E; omit if not applicable).

Recipient rules (Spec 0004): skill
[vostok-rules](../skills/vostok-rules/SKILL.md); detail §4b / §5b. Not a
second constitution: omit if there is no trigger.

---

## Short Path (MANDATORY first)

**Minimal reading:** in I0/I1 do not open this file if `AGENTS.md` suffices. If you open it
(I2, stop, or doubt), stop after this short path + "Stage × grade" + "Evidence"
unless you need a specific §. **Prohibited** from reading [feature-delivery-detail.md](feature-delivery-detail.md) (§§1–7) "just in case."

In I0/I1 **do not** narrate §1–§7 or materialize evidence templates. The detail is
**on demand** (stop, I2, or doubt about a stage).

### Quick decision map (3 questions before acting)

**Before classifying:** compare the request against the project's declared
purpose and the active spec/task, when one exists. If it fits, continue without
additional ceremony. If it looks like a valid extension but falls outside active
work, declare it as new scope and route it through I2 when appropriate. If it seems
unrelated, contradicts the purpose, or lacks reliable context, stop before editing:
explain which source you consulted and ask whether to expand this project, whether
it belongs to another project, or whether to cancel. Do not switch workspaces
automatically. If sources are missing or contradict each other, ask; do not infer
the purpose from the repository name. Answering to expand scope does not bypass I2
gates. This is a guide for the agent, not a host-enforced block.

1. **What is the grade of the task?**
   - **I0** (typo/doc/minor comment with no logic change or risk) → declare `I0` + edit the requested file directly (the edit diff suffices; no extra commands unless tests are requested); no continuity ceremony unless something is pending for the human ([developer-continuity](../rules/developer-continuity.md)).
   - **I1** (clear local change, direct path in `AGENTS.md`) → declare `I1`; if the request includes goal, limits, and criterion, do not repeat it; declare in 1 line only what is inferred → edit → verify in chat → brief close with **done / what's next / who acts** ([developer-continuity](../rules/developer-continuity.md)).
   - **I2** (small feature, public/local contract, or requires persisting agreement) → apply the pre-creation gate below; if `D-S` escalated a direct request, also confirm the grade. Create only the shown dossier after confirmation; present and verify what was persisted; ask for separate authorization to implement (unless explicit combined fast-track) → edit → verify → review package → **explicit human acceptance**.
   - **I3** (cross-cutting architecture/security) → **stop** (pending planning or handoff). Do not execute the I3 dossier silently. If there is later an **authorized execution slice** and the work reaches VERIFY/D-K ready to accept: mandatory gate [i3-independent-preacceptance-audit](i3-independent-preacceptance-audit.md) **before** present-information D / requesting D-H. Does not apply to I0/I1/I2.
   - **I2 before creating dossier (includes Cold start):** explore in read-only mode; draft and show in chat/UI the full spec and initial task; wait for explicit confirmation to create only what was approved; show and verify the persisted files. Change requests update the draft and require re-presenting it. By default, creation confirmation **does not** authorize implementation or additional scaffolding: ask for separate explicit authorization before EXEC. **Fast-track:** if the human explicitly gives combined authorization ("create and implement"), persist the dossier and proceed directly to EXEC without an intermediate pause.
   - **Cold start & architectural bootstrap:** if the repository has no specs (`specs/` empty or without `0001-*`), do not block in passive `I3`. Run read-only architectural diagnosis (`defined`, `partially_defined`, `inconsistent`, `unidentified`) and surface documented-vs-implemented drift; when architectural decisions are missing or inconsistent, invite the user with a motivated recommendation to preserve the current structure, analyze alternatives, generate an architecture contract (project file `.vostok/architecture-contract.md`), or postpone non-blocking decisions. Propose in chat spec `0001`, milestone plan, initial task, and H0 (contracts/architecture) following the I2 gate above. Do not create spec/task or scaffolding before confirmation; do not execute business logic before subsequent authorization.
2. **Is there material ambiguity or grade escalation (`D-S`)?**
   - If writing the echo or intent requires inventing a limit or criterion, or if a risk signal (public contract consumed by external clients, security, credentials, module boundary crossing) elevates a seemingly local request to `I2` → **stop and ask** before touching files.
3. **When to activate extensions (and when to omit them)?**
   - **Context selection (§2):** only if there are conflicting sources or a tight budget; in clear I1 → **omit**.
   - **Options presentation (`decision-brief` + `present-information` A):** only in **I2** before editing when there are multiple reasonable architectures/options.
   - **Spec/task pre-creation (`present-information` E):** in **I2** (includes Cold start) before writing the dossier; draft in chat/UI, creation confirmation, and separate (or explicit combined) implementation authorization.
   - **Recipient rules (§4b / §5b, `tools/repository_rules.py` or scripts installed under `.vostok/skills/vostok-rules/`):** only if the task aims to audit/modify repository rules or expressly requests `--protection required`. Omit in ordinary development tasks and remediation cycles.
   - **Scope supervisor (§5, `tools/check_scope_evidence.py` or installed copy):** only in VERIFY when an applicable `ScopeContract` exists.

### Remediation / rework cycle (post-audit or not accepted)
When a task or spec receives audit findings (human or technical) and its state is `incomplete` or `with divergences`:
1. Scope is strictly bounded to the received findings.
2. **Governance immunity:** global rule scans and preflights (§4b) are skipped; code remediation is never halted by rule caches or uninterpreted units.
3. The cycle is direct: fix code → run project tests (`test`, `typecheck`) → check observable criteria.
4. **If the I3 gate applied:** re-run [i3-independent-preacceptance-audit](i3-independent-preacceptance-audit.md) before present-information D / requesting D-H. Otherwise: re-present the acceptance package to the operator.

### I0
One-line trace → minimal change → check if any → done.
No echo, manifest, formal plan, D-H, handoff, or evidence files.
If the operation is **regulated** by recipient rules or requests
`--protection required` → apply the Spec 0004 control (§4b) before writing;
if there is no viable map/profile, **stop** (do not degrade silently).

### I1 (direct path)
1. **Scope** ([eco.md](../templates/eco.md)): if the request already includes goal,
   includes, excludes, and observable criteria without inventing anything, the request
   is the record; do not repeat it. Declare in one line before editing only what
   is inferred. If a limit/criterion would have to be invented: **stop** and ask.
2. **CONTEXT** only with trigger (§2). Otherwise: **omit** (no manifest).
3. **PLAN** = implicit in the scope source or one paragraph; no separate dossier.
4. **EXECUTION** within scope. If §4b applies: `preflight`/`bind` **before**
   the first material change; result in chat only.
5. **VERIFICATION**: a real command or review; result **in chat**.
   If there was a map/binding: include §5b (`verify`) in the same chat.
   **Prohibited in I1:** `record.json`, [verdict](../templates/verdict.md),
   [evidence-pack](../templates/evidence-pack.md), `evidence/` tree, rule packs
   as durable evidence.
6. **Close**: criteria + proof to the user **and** continuity (done / what's next / who acts; blocker or decision if applicable; record agreed decisions and their rationale in chat). No D-K/D-H. See [developer-continuity](../rules/developer-continuity.md) and [presentation-design](../rules/presentation-design.md).
7. **HANDOFF** only if the session ends or work remains pending (§7). Otherwise: **omit**.

### I2
Before creating the task: visible proposal in chat/UI and explicit creation confirmation. After confirmation, persist approved spec and task, present and verify them; then request separate authorization to implement (unless fast-track with explicit combined authorization "create and implement"). Then: intent + criteria as a **task** under the spec → CONTEXT if applicable → plan in the
task (when touching HTTP APIs, events, or public schemas, apply **contract-first**: define and validate OpenAPI/schema contracts via `vostok contracts-check`, check architecture boundaries via `vostok arch-check --stage plan`, and propose contract updates via `vostok arch-evolve --stage plan` before writing implementation code) → if there is architecture or reasonable options: [decision-brief](../templates/decision-brief.md) (with analysis, motivated recommendation, and record of agreements as evidence)
+ [present-information](present-information.md) **before** EXEC → EXEC (with
§4b if applicable; run `vostok arch-check --diff --stage execution`, `vostok arch-evolve --stage execution` for intentional boundary evolution, and `vostok risk-check` on changed files to detect dynamic `D-S` signals) → VERIFY (`vostok verify --stage verify` including full-graph cycles and expiring exceptions, D-AC, `vostok docs-impact`, and §5b) → D-K → policy-governed independent audit ([independent-preacceptance-audit](independent-preacceptance-audit.md) when required for `I2+` by `.vostok/autonomy-policy.json`); present review package
([present-information](present-information.md) trigger D) → **human-only D-H** (strictly separated from deployment authorization)
(with continuity close: what's next = accept/reject) → handoff if pending
or session cut. See [developer-continuity](../rules/developer-continuity.md). Persistence: criteria + result **with the
task** (rule binding/verdict if used; `.git/vostok-rules/` cache is not
D-H). `record.json` / verdict **only** if offline auditing/processing is needed
with the task — one artifact, not three records with independent states.

### I3
Stop → pending planning or [handoff](../templates/handoff.md). Exception: on Cold Start, activate the structured Spec 0001 startup protocol instead of a passive stop.

When, after plan and **human authorization of an execution slice**, the result
is in VERIFY + D-K ready to accept: run
[i3-independent-preacceptance-audit](i3-independent-preacceptance-audit.md)
(separate auditor) → if `clean` (or explicit human exception) → present-information D
→ **human-only D-H**. Open findings → remediation → re-audit; do not request D-H
with open findings without a named exception. This gate **does not** apply to I0/I1/I2.

---

## Stage × grade

| Stage | I0 | I1 | I2 | I3 (after authorized slice) |
| --- | --- | --- | --- | --- |
| INTENT | 1-line trace | Scope in request (+ inferred in 1 line) | Task `tasks/<id>/` + review | Stop / plan / handoff first |
| CONTEXT | Omit | Only with **trigger** (§2) | Yes if mixed sources / conflict; manifest if applicable | Per authorized slice |
| PLAN | Omit / implicit | Collapsed in the echo | Light in the task | Pending planning until authorization |
| EXECUTION | Yes (minimal) | Yes | Yes | Only after human authorization of the slice |
| VERIFICATION | Check if changed | Yes (real proof; **chat only**) | Yes + D-AC; optional `record.json` with task | Yes + slice D-AC |
| ACCEPTANCE | N/A | Brief close (present-information C) | D-K; present-information D; human D-H; states | D-K → **mandatory I3 audit** → D → D-H |
| HANDOFF | Omit | Only cut / pending | If pending, blocker, or 2nd session | Usual on initial stop |

**Never omit:** grade classification; stop on material ambiguity;
bounded EXEC; VERIFY with real proof when claiming done; human D-H in I2
for `completed`; in I3 with acceptance trigger, the independent audit
before requesting D-H.

---

## Evidence

- No `specs/**/evidence/` tree ([placement-and-sources](../rules/placement-and-sources.md)).
- I0/I1: ephemeral **only** (chat). I2: with the task if persisted.
- [evidence-record](../templates/evidence-record.md) / [verdict](../templates/verdict.md) =
  **persisted I2 / experiment only**; not daily path.
- `tools/validate_evidence.py`, if available in the source repository, only if `record.json` exists. Consistent ≠ met ≠ accepted.
- S0 layout / projection anti-drift: `tools/check_portable_layout.py`, if available in the source repository (optional; does not assert semantics).

---

## Detail contract (on demand — not an I1 checklist)

Sections §1–§7 live in
[feature-delivery-detail.md](feature-delivery-detail.md). **Do not** open them or
execute them as ceremony in I1. Use only on a stop, I2, or doubt about a
specific stage. **Prohibited** from reading the detail "just in case."

**Harness:** model, tools, prompt. **Vostok:** procedure and honesty.  
**Human:** ambiguities; D-H in I2; out-of-scope risks.

---

## Native activation (reference)

| State | Meaning |
| --- | --- |
| S0 | Files present (canonical + skill) |
| S1 | Skill discovered |
| S2 | Natively invoked (`/feature-delivery`) — manual Read ≠ S2 |
| S3 | After S2, procedure effects |

Detail: Spec 0002 §6.3. This file existing ≠ S1–S3.

---

## Out of scope for this workflow

- Own runtime, orchestrator, RAG.
- Duplicated procedural body in native projections.
- `enforced` without E6; executing I3 without stop/plan/slice authorization; reopening Spec 0001 / ADR Accepted.
- Skipping the pre-D-H I3 audit when the Spec 0021 trigger is met.
- Recreating `specs/**/evidence/` or `specs/proposals/`.
- **Principal spec closure** → [spec-closure.md](spec-closure.md) (not I1 short path).
