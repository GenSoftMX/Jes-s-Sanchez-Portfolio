---
id: context-selection
type: rule
revision: 2026-11-18
scope: guided context selection, architectural bootstrap diagnosis, and modular topology navigation (AC-13 / ADR-006 / Spec 0030 / Spec 0033)
authority: Instruction Authority (project)
backed_by:
  - docs/adr/ADR-006-context-engineering.md
  - docs/adr/ADR-003-trust-evidence-enforcement.md
  - docs/adr/ADR-007-agent-resources-layout.md
---

# Context Selection and Navigation (Guided)

## Mandatory

1. **First-request pre-flight, topology, and architectural diagnosis:** Before exploring or editing code in a session or recipient repository, check whether the Technical Sheet (`.vostok/project-sheet.md` or `project-sheet.md`) and Architecture Contract (`.vostok/architecture-contract.md`) exist. On first request or when architectural rules are missing/inconsistent, run a read-only scan of topology, pre-existing agentic rules, and architectural state (`defined`, `partially_defined`, `inconsistent`, or `unidentified`, detecting drift between documented and implemented units). When key architectural decisions are missing or drift exists, initiate a contextual bootstrap interaction with a **motivated recommendation** ([presentation-design](presentation-design.md)), letting the user: (a) preserve the current structure, (b) analyze alternatives (`tech-advisor`), (c) generate an architecture contract proposal (project file `.vostok/architecture-contract.md`, modeled on the producer template `architecture-contract.md` when available), or (d) postpone non-blocking decisions. Propose Vostok adoption with guaranteed backup before modifying files.
2. **Upward hierarchical navigation ("The Closest `AGENTS.md`"):** In modular repositories or monorepos, when working on any file under `path/to/module/`, search upward for the closest `AGENTS.md` to that file. Its local guidelines and prohibitions govern the technical implementation of that module as mandatory rules.
3. **Instruction authority hierarchy:** When discrepancies arise between sources, apply the following strict resolution order:
   1. Environment / Harness constraints (memory, network/shell permissions, sandboxes).
   2. Explicit intent of the current turn (echo in I1 or intent in I2).
   3. The closest `AGENTS.md` to the modified file and the respective module's rules.
   4. Global rules and workflows from the Lean Core (`.vostok/rules/` and root `AGENTS.md`).
   5. General conventions and templates.
4. **Declarative routing:** In monorepos, consult the context router (`context-router.md` from the project or Vostok documentation, if it exists) before running broad searches. Loading modules or files unrelated to the active use case is prohibited.
5. **Separate declared / observed / injected:** Without a signal from the host about the assembled prompt, **injected = unavailable** (do not invent Injection).
6. **Critical rules:** Identify active critical rules; **do not** discard them merely due to context budget. If they do not fit, declare the condition and stop or escalate.
7. **Name contradictions:** Identify currency (current vs. obsolete source) when it affects the task. Knowledge documents marked `Verified: YYYY-MM-DD` must be checked against the current code if they are older than the last material change to the module.
8. **Justify exclusions:** Justify relevant exclusions (noise, duplicate, out of scope, unaffected module).
9. **Context manifest:** Record the selection with the [context manifest](../templates/context-manifest.md) when the grade or task requires it. I0 does not carry the I2 manifest.

## Limit

This rule is not a deterministic selector, RAG, or invasive index. It does not prove that the model received exactly what was selected, and it does not replace code compilers or linters.
