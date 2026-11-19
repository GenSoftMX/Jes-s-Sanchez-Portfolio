---
id: context-selection-step
type: workflow
revision: 2026-11-07
purpose: minimal guided context selection step before material work / E8
backed_by:
  - docs/adr/ADR-006-context-engineering.md
  - .vostok/rules/context-selection.md
---

# Workflow — context-selection-step

Insert **after** setting grade/scope and **before** a material diff that depends on mixed sources, or when preparing E8.

1. List relevant candidate sources (no RAG).
2. Evaluate currency, authority, and contradictions (guided judgment).
3. Select the useful minimum; record exclusions.
4. Verify that no applicable mandatory rule was left out without declaration.
5. Fill out [context-manifest.md](../templates/context-manifest.md).
6. Mark **injected = unavailable** if the host does not expose the prompt.

Does not replace the harness. Does not claim Injection.
