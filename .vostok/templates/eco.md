---
id: eco
type: template
revision: 2026-11-06
purpose: I1 echo before material edits
backed_by:
  - docs/adr/ADR-004-autonomy-grades-risk.md
  - docs/adr/ADR-005-intent-representation.md
  - docs/adr/ADR-014-visible-product-language.md
---

# Scope echo (I1)

In I1 work, when the visible request already includes goal, boundaries (`includes` / `excludes`), and observable criteria without requiring material interpretation, **the request is the scope record** and is not restated.

If any piece is missing but can be derived directly without choosing between material alternatives, state it in one line **before** editing. Ephemeral: do not open an I2 dossier or a durable file under `specs/` in I1.

If defining a boundary or criterion requires guessing, inventing a requirement, or choosing between material alternatives: **stop** and ask; do not edit.

```text
Inferred scope (only items not written in the request):
- …
```

Notes:

- Plain language (without requiring grade codes or D-* identifiers in chat).
- Do not ask for routine sign-off when scope is already complete. It is not approval or a Spec. It is not D-H.
- A criterion that does not yet name anything observable does not govern: rewrite it or ask.
