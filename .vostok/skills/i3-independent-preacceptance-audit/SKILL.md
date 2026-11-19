---
name: i3-independent-preacceptance-audit
description: >-
  Mandatory separate auditor flow for I3 work before asking for D-H. Contrasts
  frozen requirements/criteria against the delivered change. Use when I3
  trigger holds, or when feature-delivery requires the pre-acceptance audit.
  Canonical workflow: .vostok/workflows/i3-independent-preacceptance-audit.md.
---

# I3 independent pre-acceptance audit

Follow the canonical workflow
[i3-independent-preacceptance-audit.md](../../workflows/i3-independent-preacceptance-audit.md).
Do not re-author its stages here.

## Quick obligations

1. Confirm the I3 trigger (grade I3 on record + authorized execution slice +
   implementer VERIFY/D-K ready for acceptance).
2. Declare isolation mode; prefer a separate agent/session when the host allows.
3. Contrast requirements/criteria vs diff; do not equate green tests with
   semantic satisfaction.
4. Status `findings` → remediation → **re-audit**; do not ask for D-H with open
   findings unless the human names an explicit exception.
5. Never claim independence, human review, or `enforced` without the matching
   signal.

This skill’s presence does not prove discovery, load, or application (ADR-007).
