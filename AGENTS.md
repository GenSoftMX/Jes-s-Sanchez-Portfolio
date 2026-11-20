# Vostok AI Workflow — Target Project Entry Point

Vostok's core lives in [`.vostok/`](.vostok/). These instructions accompany the target project's rules; file presence does not prove host load or `enforced` protection.

The portfolio site is in `src/`. Its units and boundaries are in [`.vostok/architecture-contract.md`](.vostok/architecture-contract.md).

## How to Work

1. **Alignment & preflight:** Compare the request against the project's purpose and active spec/task. In modular repos, locate upward the closest `AGENTS.md`.
   On first use in an unconfigured repo, run read-only preflight (topology, rules, architectural diagnosis `defined|partially_defined|inconsistent|unidentified` + drift) and propose Vostok adoption with guaranteed backup.
   When drift or missing decisions exist, offer with motivated recommendation to preserve structure, analyze alternatives, propose [`.vostok/templates/architecture-contract.md`](.vostok/templates/architecture-contract.md), or postpone non-blocking decisions. If unrelated or contradictory, pause and ask (guided, not enforced).
2. **Classify grade literally (`I0`, `I1`, `I2`, or `I3`)** before any material change ([`grades-proportionality`](.vostok/rules/grades-proportionality.md)).

**Direct path (`I0`/`I1`)** — do not open workflows or `.vostok/` unless in doubt:
- **I0:** trivial text/comment edit, no logic change or risk. Declare `I0`, edit, and close; diff is proof.
- **I1:** bounded local change. Declare `I1`, state any inferred scope piece in one line, edit within scope, run relevant checks, and report observed output.
  Do not create `specs/` dossiers. Close with motivated recommendations ([`presentation-design`](.vostok/rules/presentation-design.md)) and continuity (**what you did**, **what comes next**, **who acts** — [`developer-continuity`](.vostok/rules/developer-continuity.md)).
- **Risk signal** (security, credentials, external public API/contract, cross-module boundary): escalate to `I2`/`I3` and **stop before editing** (`D-S`; never downgrades).

**Agreed path (`I2`/`I3`):**
- Follow [`feature-delivery`](.vostok/workflows/feature-delivery.md) (Short Path first; [`feature-delivery-detail`](.vostok/workflows/feature-delivery-detail.md) only on demand).
- **Proposal gate:** Explore read-only, present the full spec and initial task draft in chat/UI, and wait for explicit confirmation to create. Show persisted files and request separate authorization to implement (unless given explicit combined authorization "create and implement" / "crear e implementar").
- **Cold start & `/goal`:** Without `specs/0001-*`, propose `0001` + H0 under the proposal gate instead of aborting in passive `I3`. For open-ended `/goal` requests, run [`autonomous-goal-inception.md`](.vostok/workflows/autonomous-goal-inception.md) before coding loops.
- **Audit & Acceptance:** Run policy-governed independent audit ([`independent-preacceptance-audit`](.vostok/workflows/independent-preacceptance-audit.md), default `I2+` via `.vostok/autonomy-policy.json`; legacy alias [`i3-independent-preacceptance-audit`](.vostok/workflows/i3-independent-preacceptance-audit.md)) before requesting `D-H`, keeping `D-H` separate from deployment.
  For `I3`, stop pending planning or [`handoff`](.vostok/templates/handoff.md).
- **Never** run `git commit` without explicit approval in the current message.

## Rules & Local Tools

Apply [evidence](.vostok/rules/evidence-honesty.md), [continuity](.vostok/rules/developer-continuity.md), [no-commits](.vostok/rules/no-commits-without-approval.md), [visible-language](.vostok/rules/visible-language.md), [presentation](.vostok/rules/presentation-design.md), [placement](.vostok/rules/placement-and-sources.md), and [context](.vostok/rules/context-selection.md).

- Local CLI (stdlib, no model calls): `.vostok/tools/vostok_cli.py` (`analyze`, `arch-check`, `contracts-check`, `verify`, `risk-check`, `policy`, `metrics`).
- Conditional rules & supervisor (explicit trigger only): [`vostok-rules`](.vostok/skills/vostok-rules/SKILL.md) and `.vostok/skills/vostok-rules/scripts/check_scope_evidence.py`.
- Hygiene: never recreate `specs/**/evidence/` or `specs/proposals/`; closed specs are strictly immutable.
