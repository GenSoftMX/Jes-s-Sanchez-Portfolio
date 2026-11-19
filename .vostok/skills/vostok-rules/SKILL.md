---
name: vostok-rules
description: >-
  Discover and classify a repository's existing agent rules, validate a cited
  rule map, and derive task applicability. Use for repository-rule integration
  or explaining which obligations apply to a task. Evaluate authorized checks
  with source freshness. Feature-delivery invokes this via §4b/§5b; Cursor G2
  CLI protection is binding-backed, Codex required remains unsupported.
---

# Repository rules integration

Use the host's model to interpret sources; do not add a model client or runtime.
The implementation is `tools/repository_rules.py` in the Vostok source
repository (canonical). After managed install, the same bytes are also present
under `.vostok/skills/vostok-rules/scripts/` (mapped via `SOURCE_PATHS`). Prefer
`tools/` when both exist in the source repo; in a receiver, use the installed
`scripts/` path. Same rule for `repository_rule_contracts.py`,
`repository_rule_cache.py`, and sibling modules. Resolve whichever path exists
before invoking it.

For `integrate --root <repo>`:

1. Run `scan --root <repo>`. Exit 1 with `needs_interpretation` is expected,
   not successful integration. A blocked scan or exit 2 stops the process.
   Native surfaces without a reader (`CLAUDE.md`, `.mdc`, …) are inventoried as
   warnings and do not by themselves make `complete` false. Broken/absolute
   references and other structural errors still block. An unborn `HEAD` (Git
   init without commits) yields `baseline_head: null` and the
   `unborn_or_absent_head` limit instead of failing discovery. Never execute the
   receiver's code, install dependencies, repair its rules, or change its native
   configuration as part of discovery. Scan resolves versioned discovery
   profiles (`base.v1` plus stack profiles from filename signals only), publishes
   `discovery` and the effective `boundary`, and does not claim semantic coverage
   from that composition.
2. Keep derived files in the Git administrative directory's `vostok-rules/`
   subdirectory, or a fresh operator-selected directory outside the receiver.
   `--output` preserves existing files. Cache files are not credentials.
3. Run `draft --root <repo>` (with `--carry-from <prior-map>` when reusing a
   compatible reviewed map) and interpret every unresolved source unit. Unit
   identity (`content-context.v2` under `markdown-and-text-config.v2`) binds
   path, unit text, and ordered unit context while keeping current line numbers
   in locators: blank-line shifts preserve unique units, any semantic/heading/
   order change in a file invalidates that file's units, ambiguous duplicate
   units never carry treatments, and incompatible reader versions require a
   fresh review. Use the exact map fields in the contract definitions; retain
   every unit ID and a reason for its treatment. Split multiple obligations
   into separate cited rules. A heading, example or background paragraph is not
   automatically an obligation; an ADR or guide can contain obligations even
   outside a rules directory. Unresolved meaning stays `unresolved`; do not
   fill uncertainty with a guess.
4. Classify resource, domains, modality, scope/conditions/stage, authority and
   evaluation separately. Copy a literal source quote, preserving source unit
   links. Do not promote Proposed decisions to Accepted. Combine compatible
   project and Vostok obligations; record incompatible mandatory obligations
   as conflicts. Local specificity does not erase a general obligation.
5. Commands found in sources are candidates. Define argv, cwd, inputs,
   timeout, relevant environment key names and generated outputs without
   running them. Guided, human and independent reviews are distinct evaluation
   modes. Never invent a human or independent review. Host-config values are
   withheld from inventory output; their hash is available. If understanding a
   relevant obligation requires withheld data, leave it unresolved and explain
   the missing safe reader instead of copying credentials into the map.
6. Mark the source review `reviewed_guided` only after actually reviewing it,
   then run `validate --root <repo> --map <file>`. Mechanical coverage checks
   do not prove semantic exhaustiveness. Report source review provenance and
   the pending independent corpus review separately.
7. If the user supplied a concrete task, encode its identity/revision, exact
   intended paths, change types, operations and known facts. Run `bind` and
   retain all applicable, inapplicable and unknown rules with reasons. Use
   `explain` for a declared task path. Unknown relevant conditions and conflicts
   block; the caller cannot select a convenient subset of extracted rules.
   When the task edits obligation sources (or sets
   `modifies_repository_rules=true`), pass `--prior-map` with the previous
   agreement map. Without `agreement_change_authorized=true`, weakening or
   removing a previously active mandatory/prohibited obligation blocks; do not
   let a rewritten map self-justify the same diff.

Use `incorporate --root <repo>` only to preview adding this skill and its
scripts. It preserves existing identical files without claiming ownership;
different contents block the whole plan. Apply only an authorized concrete
preview using `--apply --plan-digest <digest>`. This adds catalog tools, never
hooks or native configuration, and is not successful rule integration.

Before a material task change, use `preflight`; after authorized changes, use
`verify`. For daily task phases with an already reviewed map, `task --root
<repo> --task <file> --phase preflight|verify` (optionally `--map <file>`,
`--cache <dir>`, `--prior-map <file>`, `--authorize-check <digest>`,
`--guided-reviews <file>`, `--details`) scans current sources, selects or
carries a single compatible validated map from the administrative cache, derives
a fresh binding for the current task, and delegates to the unchanged
`preflight`/`verify` evaluation. Missing, incompatible, ambiguous, or
partially carried maps block and explain the next step; the cache never selects
by timestamp, never remembers check authorizations or task reviews, and never
creates I1 dossiers. Required checks need the exact candidate digest authorized
by the task's scope; pass it with `--authorize-check`. Discovering a command
alone does not authorize execution.
Guided reviews are notes tied to the map/task digests, distinct from technical
PASS. Human/independent obligations stay pending external review; never invent
those acts. Verification executes argv with its cwd/environment/input binding,
observes exit/timeout, rechecks sources, and invokes the unchanged scope
supervisor. One check has one cwd; combine directories with separate authorized
checks, never shell `cd` chains. Declared `outputs` are recorded and may be
passed as extra allow-paths for attribution only; Git-ignored generated files
still yield UNKNOWN (`declared_ignored_outputs_unknown` or undeclared leak).
Do not remove that blocker by excluding all ignored files. There is no API for
caller-supplied exits.

For `--protection required`, supply `--protection-profile` and `--hooks` from a
Cursor G2 plan (`protection-plan`). Without a valid fail-closed Cursor profile
that covers Write/Edit/Shell and denies MCP/Task, the command returns
`blocked_protection_unavailable` (no silent downgrade). Codex remains
unsupported for required protection. The operational gate is
`cursor_g2_gate.py`: it allows reads, denies Shell/MCP, and allows Write/Edit
only for exact bound task paths. Previewing a plan does not install hooks.

## Software delivery priority and remediation cycle

`vostok-rules` is an optional governance and protection analysis tool. In
ordinary product development tasks, bugfixes, or post-audit remediation cycles
where `--protection required` has not been requested:
- The presence of units pending review, a missing rule map, or a cache mismatch
  **must NEVER stop the execution of unit or integration tests (`npm test`,
  `pytest`, etc.), type checks (`typecheck`), or the delivery of the code
  solution to the operator**.
- The agent must prioritize observable technical verification of the software.
  In case of rule incompatibility in ordinary product tasks, it must record an
  informational warning (`[INFO] rule governance skipped or untriggered`) and
  proceed with the project's technical verification suite.
Do not claim desktop E6, universal enforcement, or integration complete. The
older Cursor/Codex probe permits are experimental measurements, not this gate.
