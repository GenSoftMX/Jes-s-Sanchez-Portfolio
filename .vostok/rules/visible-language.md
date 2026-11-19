---
id: visible-language
type: rule
revision: 2026-11-06
scope: chat and human-facing messages
authority: Instruction Authority (project)
backed_by:
  - docs/adr/ADR-014-visible-product-language.md
---

# Plain Visible Language

## Mandatory

1. Speak to the human in plain prose. Internal catalog identifiers (D-*, grade codes as mandatory jargon) are not required in chat.
2. Show the decision or status needed according to the grade; do not ask for routine confirmation in I0 or in I1 when the echo invents nothing.
3. Distinguish in prose: recommended, declared, observed, verified, accepted, actually enforceable — **without** hierarchy or rhetorical promotion among them.
4. Do not use labels like `verified`, `enforced`, `accepted`, or "completed" in ways that claim guarantees the ADRs do not support.
5. In I2, request acceptance of the result in clear language; do not substitute it with an "accepted" narrative.
6. After a material turn (I1+), the close states in prose what was done and **what comes next** (who acts; blocker or decision if applicable). Detail: [developer-continuity](developer-continuity.md). I0 does not require that block.

## Limit

This rule does not redefine the catalog or the grades. It does not introduce UI or dashboard.
