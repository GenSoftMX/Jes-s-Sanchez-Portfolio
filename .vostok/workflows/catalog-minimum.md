---
id: catalog-minimum
type: workflow
revision: 2026-11-06
purpose: minimal portable walk of the decision catalog
backed_by:
  - docs/adr/ADR-001-product-identity.md
  - docs/adr/ADR-004-autonomy-grades-risk.md
  - docs/adr/ADR-007-agent-resources-layout.md
---

# Workflow — catalog-minimum

> **Which file should I follow to execute a task?**  
> To drive any code request (`I0` / `I1` / `I2`), follow **[`feature-delivery.md`](feature-delivery.md)** directly (starting with its *Short Path*).  
> This document (`catalog-minimum.md`) is the **conceptual decision map** that `feature-delivery.md` operationalizes; it is not a second parallel flow or a runtime.

Follow only the steps required by the grade. Omit ceremony that the grade does not ask for.

## 1. Grade and stop

- Propose the grade (I0 / I1 / I2).
- Record risk signals if they exist; recalculate the minimum.
- **S4:** if the risk signal raises the minimum to **I3** (or requests an I3 plan/tasks): **stop**; do not continue in I1; do not simulate an I3 dossier. Exit: **pending planning** or [handoff](../templates/handoff.md).
- After an **authorized** execution slice and result ready to accept: gate
  [i3-independent-preacceptance-audit](i3-independent-preacceptance-audit.md)
  before D-H (I3 only; not I0/I1/I2).
- Rule: [grades-proportionality.md](../rules/grades-proportionality.md).

## 2. Scope

- **I0:** trace line; no echo or Spec.
- **I1:** the full request is the scope record prior to the first material change; declare before editing only what is inferred ([eco.md](../templates/eco.md)).
- **I2:** intent persisted under `specs/` with [intention.md](../templates/intention.md); criterion and acceptance states with [criterion-states.md](../templates/criterion-states.md).
- On material ambiguity: stop and ask.

## 3. Applicable constraints

- Identify active rules with applicable scope.
- Do not discard mandatory rules due to context budget.
- On contradiction between mandatory rules: declare conflict and stop or escalate.
- Rules: [`.vostok/rules/`](../rules/).
- If the recipient contributes its own agentic rules (Spec 0004): follow
  [feature-delivery](feature-delivery.md) §4b/§5b and the
  [vostok-rules](../skills/vostok-rules/SKILL.md) skill; do not improvise a
  manual manifest or degrade `--protection required`.

## 3b. Context selection (if applicable)

- If there are mixed sources / E8 preparation / material work depending on currency: [context-selection-step.md](context-selection-step.md).
- Rule: [context-selection.md](../rules/context-selection.md); form: [context-manifest.md](../templates/context-manifest.md).
- Injected = `unavailable` without a host signal. No deterministic selector/RAG.

## 4. Execution in the harness

- The host runs tools and permissions.
- This workflow does not replace the harness or claim loading of these resources.

## 5. Verification and close

- Check result against the grade's scope/criteria.
- Do not call a mere link satisfied; unknown ≠ success.
- **I2 — work state (≠ D-AC):**
  - If D-K does **not** support closure (missing evidence, criterion in no-evidence / linked / pending-evaluation, etc.) → **`incomplete`** (or another appropriate state: blocked / with divergences). **Do not** use `pending acceptance` by default.
  - If D-K supports it and the result is prepared for the human → request D-H; without it the work state is **`pending acceptance`** ("ready for review" ≠ `completed`).
  - Only after D-H that accepts (and with no pending criteria counted as met) → **`completed`**.
- Rules: [evidence-honesty.md](../rules/evidence-honesty.md), [visible-language.md](../rules/visible-language.md); form: [criterion-states.md](../templates/criterion-states.md).

## 6. Continuity (if applicable)

- If the session ends or work must continue later: [handoff.md](../templates/handoff.md).
- Do not rely on the transcript as the sole governance backing.

## Operational vertical (Spec 0002)

To drive a development request through INTENT→…→HANDOFF, use the canonical
contract [feature-delivery.md](feature-delivery.md) (native activation
`/feature-delivery`). This minimal catalog **does not** duplicate that procedure.

Presenting scope/options/result in chat (when triggered):
[present-information.md](present-information.md); rule
[presentation-design](../rules/presentation-design.md). Showing ≠ D-H.

## Principal spec closure (rare event)

Upon accepting the increment of a `000N-…`: [spec-closure.md](spec-closure.md).
This is not routine I0/I1. It does not replace a task's D-H.

## Out of scope for this workflow (MVP)

- Deterministic selector / RAG / index; E6/E8 execution (separate evidence); enforcement hooks.
