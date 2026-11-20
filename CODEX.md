# Native Projection — OpenAI Codex / ChatGPT

This file is an **adapter projection**, not the canonical source of Vostok policy.

- Portable canonical: [`AGENTS.md`](AGENTS.md) → [`.vostok/`](.vostok/)
- Compatibility: [`docs/compatibility/codex.md`](.vostok/docs/compatibility/codex.md)

## Mandatory Directives for Codex

1. **Mandatory reading & bootstrap:** Read [`AGENTS.md`](AGENTS.md) first to align with project purpose, run read-only architectural preflight when unconfigured, and classify the literal grade (`I0`, `I1`, `I2`, `I3`).
2. **I2 pre-proposal gate:** Explore read-only and present the complete spec, milestone plan, and initial task in chat before writing files, scaffolding, or code. Wait for explicit confirmation to create, show persisted files, and request separate authorization to implement (unless given explicit "create and implement" / "crear e implementar").
3. **Structured Interactive Decision Contract (Level B Quick-Key):** At any decision gate (Trigger E proposal gate, implementation authorization, design forks, or D-H acceptance), you **must never ask open-ended narrative questions in prose**. You must always emit a discrete **Quick-Key Decision Block** with numbered options (`[1]`, `[2]`, `[3]`) where option `[1]` is `(Recommended: ...)`, allowing the human to decide by simply replying with a number.
4. **Placement of Specs:** Specifications and tasks must live exclusively under `.vostok/specs/<000N-*>/tasks/`. Dedicated `specs/` folders at the repository root are strictly prohibited. Every closed/rejected spec is immutable.
5. **Proportional Verification:** In bootstrap/contractual tasks (such as H0) where code implementation is explicitly excluded, verify contract completeness and design criteria. Do not block completion on missing code directories (`documented_unit_missing` in `arch-check`) that are explicitly scheduled for scaffolding in subsequent tasks (H1+).
6. **Policy-governed `I2+` audit & `D-H`:** Before requesting `D-H` on `I2+`, run [`.vostok/workflows/independent-preacceptance-audit.md`](.vostok/workflows/independent-preacceptance-audit.md) per `.vostok/autonomy-policy.json`; keep `D-H` separate from deployment.
7. **No commits without approval:** Never run `git commit` without explicit approval in the current message.
