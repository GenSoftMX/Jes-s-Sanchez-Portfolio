---
id: feature-delivery-detail
type: workflow
revision: 2026-11-13
purpose: on-demand stage detail (§1–§7) for feature-delivery; not always-on
backed_by:
  - docs/adr/ADR-001-product-identity.md
  - docs/adr/ADR-002-integration-model.md
  - docs/adr/ADR-004-autonomy-grades-risk.md
  - docs/adr/ADR-005-intent-representation.md
  - docs/adr/ADR-006-context-engineering.md
  - docs/adr/ADR-008-verification-acceptance.md
  - docs/adr/ADR-009-handoff-recovery.md
composes_into:
  - feature-delivery.md
---

# Workflow — feature-delivery detail (on demand)

**Not** an always-on entry point. Open only from
[feature-delivery.md](feature-delivery.md) when a specific § is needed
(stop, I2, or doubt). I0/I1: do not open this file.

## 1. INTENT

- **Inputs:** user request + observable risk signals.
- **Outputs:** grade `I0` / `I1` / `I2` (or `I3` stop) + scope (`goal`, `includes`, `excludes`, `criteria`). Artifact: `I0`/`I1` in chat; `I2` in `intent.md` (+ `criteria.md` if applicable).

### Advancement conditions
- Grade classified; `I1` with complete echo without inventing (or human confirmation of what was inferred); for I2, spec/task draft presented and creation confirmed before writing the dossier; then intent under `specs/<000N…>/tasks/<task-id>/` with `rN` and observable criteria.
- **Stop:** material ambiguity (ask, do not edit); until creation is confirmed, no writing of spec/task/scaffolding/code; after creating, ask for separate authorization before implementing. `D-S` escalation to `I2` due to risk signal (record signal, recalculate grade, and ask for confirmation before editing files; do not skip `intent.md` to edit directly); minimum `I3` (pending planning / handoff; except structured Cold Start proposal under its I2 gate); out of scope or normative change (owner).

---

## 2. CONTEXT

**Trigger (if not applicable → omit stage and manifest):**
- Mixed/contradictory sources affecting the change, E8/AC-13 case, `I2` with conflicting docs/rules, or mandatory rule exceeding budget. (Clear `I1` in one area → **omit**).
- **Outputs:** relevant selection + [context-manifest](../templates/context-manifest.md) if applicable; views declared / observed / injected (`injected = unavailable` without host signal).
- **Stop:** unresolved conflict of mandatory rules → declare and escalate.
- **Dependencies:** [context-selection-step](context-selection-step.md), [context-selection](../rules/context-selection.md). Do not use `legacy/` as a base.

---

## 3. PLAN

- **Proportionality:** in `I1` the plan lives in the echo (steps ↔ criteria; no `plan.md`). In `I2`: light plan in the task.
- **Presentation (`I2`, trigger A):** if it defines architecture or admits multiple reasonable options → write [decision-brief](../templates/decision-brief.md) with the task and run [present-information](present-information.md) **before** EXEC (material choices = open questions; no trigger → omit).
- **Advancement:** every criterion has a planned check or "not verifiable yet"; nothing violates exclusions; brief presented without placeholders if trigger A occurred.
- **Stop:** requires `I3` / out of scope, or pending material decision blocking EXEC.

---

## 4. EXECUTION

- **Preconditions:** INTENT/PLAN/CONTEXT advanced (or legitimately omitted); if §4b applies, `preflight`/`bind` not blocked.
- **Advancement:** changes within includes/excludes; file list for VERIFY; observable diff (narration ≠ execution). Bounded repair returns to VERIFICATION.
- **Stop:** material deviation (divergence in `I2` or declare in `I1`); `preflight`/`bind` blocked by recipient rules.

---

## 4b. Recipient rules (Spec 0004) — before material change

**Trigger (if not applicable → omit):**
- The task explicitly aims to audit or modify recipient rules (`modifies_repository_rules = true`); or
- The request expressly asks for integration or `--protection required`.

**Omit:**
- In ordinary code deliveries and remediations (features, bugfixes) without mandatory protection.
- In remediation / rework cycles after an audit or acceptance rejection.
- If there is no valid map and the task is not governance: **do not** run a cold mass scan; report an informational warning and continue with code delivery.

### Procedure (skill [vostok-rules](../skills/vostok-rules/SKILL.md))
1. If there is no active map: `scan` → guided interpretation → `validate` (or
   reuse fresh map from admin cache). Cache under
   `.git/vostok-rules/` or operator; **not** among recipient sources.
2. Encode the task (`id`/`revision`/paths/change_types/operations/facts).
3. `bind` (and `explain` if needed). Unknown conditions, conflicts,
   relevant unresolved items, or weakening without `--prior-map` → **block**.
4. `preflight` before the first material edit. Candidate checks require
   `--authorize-check` with exact digest; discovering ≠ authorizing.
5. If mode is `--protection required`: require Cursor G2 profile + fail-closed
   hooks (`protection-plan` / `cursor_g2_gate`). Without a valid profile →
   `blocked_protection_unavailable` (Codex required = unsupported). **Do not**
   degrade to unprotected execution.

### Proportionality
- **I1:** states and blockers **in chat**; no packs.
- **I2:** persist summary/binding/verdict with the task if the dossier
  needs it; cache does not replace D-H or acceptance.
- Agent narration **does not** replace CLI or gate exit.

### Limits
- Guided map ≠ semantic exhaustiveness. G2 CLI ≠ desktop. Shell/MCP denied
  by profile do not prove universal Task coverage.

---

## 5. VERIFICATION

### Mandatory
- Real proof (command with output, or file review) when the criterion is checkable.
- Unknown ≠ success. Green ≠ all criteria satisfied.
- I1: per-criterion evaluation **in chat**. No template file.
- I2: D-AC ([criterion-states](../templates/criterion-states.md)); a single pack
  persisted with the task if needed (`record.json` as source; optional
  readable views — no parallel states).

### Scope & Verification Supervisor (Spec 0003 — if ScopeContract exists)

When an applicable **ScopeContract** exists (I1 echo with materialized
includes/excludes, or persisted contract in I2), in VERIFY:

1. Identify the governing revision (`governing_revision` if I2; in I1 the echo).
2. Invoke `python3 tools/check_scope_evidence.py` (or the copy installed under
   `.vostok/skills/vostok-rules/scripts/`) with `--root`, contract or
   `--allowed`/`--excluded`, `--diff-from` mode, and evidence binding when
   the criterion requires a check. The criterion declares `check` and `verified_inputs` in
   the contract; use `--execute-check` so the supervisor runs it as
   argv in `--root` (no shell), captures the exit, and binds the before/after digest.
   Do not pass `--check-exit-code` or `--check-executed`: an invoker's claim
   does not prove execution. `--criterion-evidence` may only reference the
   criterion's exact inputs; if there are multiple mandatory criteria, run
   each one and do not present the set as ready if any is missing or remains UNKNOWN.
3. Observe the **exit code** (0 / 1 / 2) — model-independent fact.
4. Read the `SupervisionVerdict` (JSON): `outcome_class`, `gate_hint`,
   `scope.violations`, `evidence[].sufficiency`, `limits`.
5. Interpret without glossing over:
   - exit 0 + gate `CONTINUE`/`READY_FOR_REVIEW` → proceed with honest facts.
   - `policy_fail` / violations / `absent`|`obsolete` evidence → **do not**
     present VERIFY as satisfactory.
   - `unknown_incomplete` / `UNKNOWN` → do not claim compliance.
   - `invocation_error` / `internal_error` → stop; fix invocation.
6. Procedural transition compatible with `gate_hint` (`REPAIR` only in
   `allowed_paths`; **prohibited** from auto-editing `excluded_paths`; max 2
   repairs; no automatic `git reset --hard`).
7. Report in I1 (chat) or I2 (with the task) the result + verdict limits.
8. Proportional traceability: I0/I1 without `record.json`/packs; I2 optional
   `supervision.json` with the task.

**Limit:** the supervisor is **checkable**, not `enforced`. A `gate_hint` does
not guarantee agent obedience (ADR-013). Do not invent D-H or semantic
satisfaction from exit 0. Spec 0003 extension; not a second constitution.

### Stop
- Narration only → do not claim verified.
- Supervisor exit ≠ 0 policy / incomplete UNKNOWN → no clean CONTINUE.

### Do not require (I0/I1)
- `record.json`, VERDICT, evidence-pack, transcripts, or recreating `evidence/`.
- Invoking the supervisor **without** an applicable ScopeContract (trivial I0 / no
  declared scope).

---

## 5b. Recipient rules — VERIFY (Spec 0004)

**Trigger:** §4b was used in this delivery, or the diff activates obligations of the
map. Otherwise → **omit**.

1. After authorized changes: `verify` with the same map/task (and `--prior-map`
   if rule sources were touched).
2. Authorize only checks with exact digest. Ignored outputs → UNKNOWN
   (strategy E09); do not exclude global ignores just to turn green.
3. Re-read source freshness; stale binding/worktree invalidates.
4. If `--protection required`: repeat the profile gate; absence or differing
   hook digest → explicit block.
5. Report: **I1** in chat (applicable / blockers / status); **I2** with the
   task. Never invent human/independent review or D-H.

Compose with §5 (supervisor 0003): both may apply; neither is silenced
so the other turns green.

---

## 6. ACCEPTANCE

**I1 — collapsed:** after VERIFY, [present-information](present-information.md)
trigger **C**: criteria + proof in minimal form (checklist or table).
No D-K/D-H block. That **is** the I1 close.

**I2 — full:**
- Honest D-K; if it holds → [present-information](present-information.md)
  trigger **D** ("ready for review" package) **before** requesting D-H.
- D-H only by authorized human (agent **never** simulates).
- States: `incomplete` / `blocked` / `with divergences` / `pending acceptance` / `completed`.
- `completed` requires authentic D-H; `pending acceptance` only if D-K holds.
- Showing the package **is not** acceptance.
- **Do not** require [i3-independent-preacceptance-audit](i3-independent-preacceptance-audit.md) in I2.

**I3 — acceptance after authorized slice:**
- Same D-K / D-H separation as I2, **plus** the mandatory gate
  [i3-independent-preacceptance-audit](i3-independent-preacceptance-audit.md)
  after D-K and **before** present-information D / requesting D-H.
- Operational trigger: see that workflow (I3 grade on record + authorized slice +
  VERIFY/D-K ready). Do not invent the gate to bypass the initial I3 stop.

### Remediation and rework cycle (post-audit / not accepted)
When review or audit determines that the implementation is not ready to accept (`incomplete` or `with divergences` states with findings):
1. **Bounded re-entry:** The task enters a remediation cycle. Scope is strictly limited to the findings list.
2. **Procedural immunity:** The full flow is not restarted and the repository rules preflight (§4b) is not triggered; code remediation is never halted by rule caches or uninterpreted units.
3. **Correction flow:**
   - Fix the findings in code (`EXECUTION`).
   - Run the project's test suite (`pnpm/npm test`, `pytest`, `typecheck`, etc.) (`VERIFICATION`).
   - Update the state of observable criteria (e.g., `criteria.md`).
   - If the I3 gate applied: **re-audit** with [i3-independent-preacceptance-audit](i3-independent-preacceptance-audit.md).
   - Only then present the diff and technical evidence to the human operator for the acceptance decision (D-H).

### Stop
- Agent "accepts" → invalid.

---

## 7. HANDOFF

**Trigger (if not applicable → omit):**
- Session cut with incomplete work; or
- Blocker / pending human decision; or
- Experiment requiring a 2nd session (e.g., E-FD-03-type continuity).

I1 that closes in the same session → **omit**.

### If executed
- [handoff.md](../templates/handoff.md): echo/intent, status, facts, pending items, proof, risks, next safe action.
- If Spec 0004 applied: cite map/binding digests, preflight/verify status,
  G2 profile (`protection_ready` / `blocked_protection_unavailable`), and limits;
  do not claim enforced or desktop.
- Do not claim verified/accepted without backing.

---
