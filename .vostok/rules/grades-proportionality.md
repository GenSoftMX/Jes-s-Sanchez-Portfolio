---
id: grades-proportionality
type: rule
revision: 2026-11-15
scope: all work under this repository
authority: Instruction Authority (project)
backed_by:
  - docs/adr/ADR-004-autonomy-grades-risk.md
  - docs/adr/ADR-005-intent-representation.md
---

# Proportional Formality

## Mandatory

Before choosing the grade, compare the request against the project's explicit
purpose and the active spec/task, if one exists. Use declared project sources;
do not infer its purpose from the repository name alone. If the relationship is
uncertain, seems unrelated, or sources contradict each other, stop before material
changes and ask whether to expand the scope, use another project, or cancel. If
there is no reliable source for the purpose, ask for context. An intentional
extension follows the applicable I2 flow; confirming it does not by itself authorize
creating the dossier or implementing. This check is guided, not a guarantee of
host enforcement.

1. Classify the work and always write the literal tag (`I0`, `I1`, `I2`, or `I3`) before a material change. I3 is named; the MVP **does not** execute its dossier (plan/tasks).
2. **I0:** one line (`I0`, one-sentence request, no recorded risk signal) and direct edit of the target file; the edit diff suffices as file proof unless the request requires running a command. No persisted echo, no I2 dossier, no ceremonial acceptance.
3. **I1:** the scope (goal, includes, excludes, and observable criteria) exists **before** the first material change. If the visible request already includes all four pieces and requires no material interpretation, the request is the scope record and is not repeated. If a piece is missing that can be derived directly without choosing between material alternatives, declare it in one line before editing. If a limit or criterion would have to be invented: stop and ask.
4. **I2:** intent persisted under `specs/`, with identity and review. Acceptance of the result is an explicit human act; the agent neither issues nor simulates it.
5. The grade **goes up** with recorded risk signals (security, credentials, contract or public API consumed by external clients, module boundary crossing); it **does not go down** through silence, declination, or an agent's phrase.
   - **Module boundary crossing rule:** A change strictly confined to internal files of a single module/feature without altering public entry points or shared contracts stays in **I1**. If the change alters contracts consumed by other modules, touches core modules (`core/`), crosses multiple modules of the monorepo, or modifies dependency configuration (`build.gradle`, `package.json`, etc.), it obligatorily escalates to **I2** (`D-S`).
   - When a risk signal elevates a seemingly local request to `I2`, **stop before editing any file and ask for confirmation of the grade and the `intent.md` dossier** (never skip `intent.md` to directly edit the requested files).
6. If the recalculated minimum is I3: exit to pending planning or handoff. Do not simulate I3 or continue in I1. The MVP **does not** execute the I3 dossier silently. If a human later authorizes an execution slice and the result reaches acceptance: mandatory gate [i3-independent-preacceptance-audit](../workflows/i3-independent-preacceptance-audit.md) before requesting D-H. That gate **does not** apply to I0/I1/I2.
7. **Cold start:** in a new repository without active specs (`specs/` empty or without `0001-*`), a foundational or MVP requirement is not aborted into a passive I3 stop. First prepare and present in chat/UI the proposal for spec `0001`, milestones, initial task, and H0 without writing files. Wait for explicit confirmation to create spec/task and show the persisted files afterward. Do not create scaffolding or business logic before that confirmation; creation authorization does not authorize implementation either. Present and request subsequent authorization for scaffolding or execution.

## Limit

This rule does not choose a harness, does not open `specs/` in I0, and does not turn the presence of files into enforcement.
