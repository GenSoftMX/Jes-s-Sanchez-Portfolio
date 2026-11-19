---
id: evidence-honesty
type: rule
revision: 2026-11-06
scope: all claims about evidence, load, enforcement, and completion
authority: Instruction Authority (project)
backed_by:
  - docs/adr/ADR-003-trust-evidence-enforcement.md
  - docs/adr/ADR-007-agent-resources-layout.md
  - docs/adr/ADR-008-verification-acceptance.md
---

# Evidence and Claims Honesty

## Mandatory

1. Separate **implemented** / **pending** / **verified**. Verified requires evidence; the agent's narrative alone is not enough.
2. Available ≠ discovered ≠ loaded ≠ applied. Do not step up a level without specific evidence for that level.
3. Do not claim that the host **loaded** Vostok, that a control is **enforced**, or that a criterion is **satisfied**, without the backing required by the applicable ADRs.
4. Unknown ≠ success. Absence of evidence ≠ criterion met. A link or a green gate alone is not enough for "satisfied."
5. Do not invent experiment results (E1/E6/E8), human acceptances, or authenticated provenance.
6. "Ready for review" ≠ finished. In I2, without human acceptance the dossier remains pending acceptance.

## Limit

This rule does not install hooks, does not run E1/E6, and does not authenticate identities. `authenticated` is out of scope for the MVP.
