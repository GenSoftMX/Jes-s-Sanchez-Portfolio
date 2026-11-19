---
id: no-commits-without-approval
type: rule
revision: 2026-11-09
scope: git commits created by the agent
authority: Instruction Authority (project)
backed_by:
  - AGENTS.md
---

# No Commits Without Direct Approval

## Mandatory

1. **Do not** create git commits (`git commit`, amend that creates a commit, or equivalents) without **direct and explicit approval** from the owner or authorized human in the current message (or an unambiguous record in the same turn).
2. Generic authorizations ("work autonomously", "deliver the proposal", "you may generate commits when the environment allows", `/goal` objectives without requesting a commit) **do not** count as commit approval.
3. Preparing changes, leaving them in the working tree or staging, and proposing a commit message is allowed. Executing the commit is not allowed without an explicit yes.
4. Push, merge to `main`/`master`, and destructive operations still require a separate explicit request; this rule does not authorize them.

## Limit

This rule does not configure git, does not replace host hooks, and does not authorize bypassing `--no-verify` or force-pushing.
