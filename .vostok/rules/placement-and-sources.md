---
id: placement-and-sources
type: rule
revision: 2026-11-16
scope: placement of Vostok resources and choice of implementation sources
authority: Instruction Authority (project)
backed_by:
  - docs/adr/ADR-007-agent-resources-layout.md
  - docs/adr/ADR-012-distribution-installation.md
  - docs/adr/ADR-017-vostok-directory-layout.md
---

# Placement and Sources

## Mandatory

1. Canonical source of portable policy / way of working: `AGENTS.md` + `.vostok/`. Specs in `specs/000N-…/` are product and I2 intent; `specs/CONVENTIONS.md` is a tree map, **not** a second operational constitution. Native projections are not a second constitution.
2. Root of `specs/`: only principal specs `000N-<slug>/` plus `README.md` / `CONVENTIONS.md`. **Do not** create `specs/proposals/`, `specs/**/evidence/`, or orphan folders (`tasks/`, `fixtures/`, …) at the root.
3. I2 work = **task** under the parent: `specs/<000N…>/tasks/<task-id>/` (intent/plan/criteria), where `<task-id>` adopts the sequential convention `0001-<slug>`, `0002-<slug>`, etc. (local to each spec). A task is not a new numbered spec.
4. Routine persisted verification, if needed, lives **with the task** (or ephemeral in I0/I1). Do not reopen a central `evidence/` tree under the spec (retired; see `specs/EVIDENCE-TREE-DECISION.md`). Record of **spec closure**: `CLOSURE.md` + `closure/` ([spec-closure](../workflows/spec-closure.md)); do not use `docs/audits/` or `.vostok/audits/` as the home for the owner act.
5. Do not silently overwrite existing files or customizations. Pre-existing identical file → preserve; do not claim ownership by mere coincidence.
6. Do not treat `legacy/` as the implementation base for the new product without explicit recorded justification.
7. When two texts of the same policy have different content: name the canonical (portable) source and fix the projection; do not maintain contradictions.
8. Creating the layout does not enforce behavior on the model or the host.
9. **Strict immutability of closed specs:** A spec in a terminal state (`closed`, `closed_with_limits`, or `rejected`) and its entire tree under `specs/<000N-slug>/` (including `spec.md`, `plan.md`, `tasks.md`, `tasks/`, `fixtures/`, `closure/`, and `experiments/`) is a frozen, **read-only** historical record. Modifying, reopening, adding tasks to, or altering assertions/tests of a closed spec is strictly prohibited. Any evolution, clarification of terms, errata, or new verification must be recorded in a new spec or in a task of the active spec, without retroactively mutating the closed dossier.
10. **Modularity and local contracts:** In monorepo or multi-module repositories, the presence of `AGENTS.md` files or guideline folders in subdirectories (`path/to/module/AGENTS.md`) is canonical and legitimate. These files act as local technical boundary contracts subordinate to the root Lean Core, governing what the module may import, its architectural prohibitions, and the commands used to verify it in isolation.
11. **One-Way Spec Isolation (specs are ephemeral):** Development dossiers under `specs/` **may** reference project documentation, ADRs, rules, code, and tools. Conversely, living project documentation (`README.md`, `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, `.vostok/**`, `docs/**`, `tools/**`, `CHANGELOG.md`) and permanent test suites (`tests/`) **must not** link to or depend on `specs/**` (neither in Markdown links nor in YAML frontmatter `backed_by` entries). Specs are temporary development-phase artifacts that may be archived or removed before release without breaking documentation, layout checks, or tests.

## Limit

This rule is not an installer, does not claim "installable product," and does not establish automatic ownership by manifest.
