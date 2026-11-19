---
id: handoff
type: template
revision: 2026-11-09
purpose: minimal continuity artifact between sessions (D-Ho)
backed_by:
  - docs/adr/ADR-009-handoff-recovery.md
  - docs/adr/ADR-003-trust-evidence-enforcement.md
  - docs/adr/ADR-014-visible-product-language.md
---

# Minimal handoff

Continuity artifact. It is **not** chat history, host memory, promoted knowledge, or proof of enforcement.

Fill in only the fields required by the grade. Do not invent evidence, provenance, or acceptance.  
Prefer **pointers** to echo / `VERDICT.md` / verification-record; do not recount every check.

```text
Handoff
- Grade: I0 | I1 | I2 | (exit to planning / handoff if applicable)
- Work state: completed | pending acceptance | incomplete | blocked | divergent
- Work identity (I2): … / n/a in I0–I1
- Governing revision (I2): … / n/a in I0–I1
- Scope source or trace (in I1 include the verbatim text or faithful summary of the request plus declared inferences; trace in I0 if applicable): …
- Done: … (one sentence; details in cited evidence)
- Pending (remaining work): …
- Recommended next action: …
- Evidence: available (cite VERDICT and/or verification-record and/or captures/) | unknown | missing
- Receiver rules (Spec 0004, if applied): map/binding digests … | preflight/verify status … | protection … (protection_ready / blocked_protection_unavailable / not requested) | limits …
- Risk or stop (if applicable): …
- Deviations / exceptions (if any; authorized or not): …
```

When resuming:

1. Do not assume verified, satisfied, or accepted without dossier backing.
2. An unknown effect remains unknown; do not blindly retry operations with uncertain side effects.
3. In I2, check that the cited revision is still the governing one.
