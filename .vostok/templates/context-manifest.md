---
id: context-manifest
type: template
revision: 2026-11-07
purpose: declared context selection record (AC-13)
backed_by:
  - docs/adr/ADR-006-context-engineering.md
  - docs/adr/ADR-003-trust-evidence-enforcement.md
---

# Context manifest (guided)

Complete for the case/task. Do not invent reads or injection.

```text
Context
- Work / request: …
- Grade: I0 | I1 | I2
- Candidate sources (available): …
- Selected (declared): …
- Observed (host reads/tools, if any): …
- Injected (assembled prompt): unavailable | (only if exposed by the host)
- Applicable critical rules: …
- Contradictions / currency: …
- Justified exclusions: …
- Budget threshold: none written | …
- Stop / escalation (if a mandatory one does not fit): …
```

Notes:

- Declared ≠ observed ≠ injected.
- Quality ≠ number of files read.
- This manifest is not D-H or proof of host load.
