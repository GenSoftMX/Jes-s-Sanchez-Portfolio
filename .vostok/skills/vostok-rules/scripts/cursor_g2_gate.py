#!/usr/bin/env python3
"""Cursor hook adapter for operational G2 (binding-backed, not operator permit).

Reads a protection profile and a frozen binding snapshot from the admin cache.
Denies Shell/MCP writes. Allows Read. Allows Write/Edit only for exact task paths
when the binding is not blocked and digests match. Fail closed on any error.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from repository_rule_protection import decide, digest, file_digest, inspect_cursor_hooks


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_hooks_digests(profile, profile_path: Path):
    if not isinstance(profile, dict) or not isinstance(profile.get("root"), str):
        return None
    root = Path(profile["root"])
    if not root.is_absolute():
        return None
    workspace_hooks = root.resolve() / ".cursor/hooks.json"
    if not workspace_hooks.is_file():
        return None
    admin_hooks = profile_path.parent / "hooks.json"
    if admin_hooks.is_file() and file_digest(workspace_hooks) != file_digest(admin_hooks):
        return set()
    hooks_doc = load_json(workspace_hooks)
    inspection = inspect_cursor_hooks(hooks_doc)
    if (not inspection["fail_closed"]
            or "beforeShellExecution_absent" in inspection["limits"]
            or "beforeMCPExecution_absent" in inspection["limits"]):
        return set()
    return {file_digest(workspace_hooks), digest(hooks_doc)}


def normalize(event):
    if not isinstance(event, dict):
        return None
    name = event.get("hook_event_name")
    if name in {"beforeShellExecution", "beforeMCPExecution"}:
        return {"hook_event_name": name, "tool_name": "Shell" if name == "beforeShellExecution" else "MCP",
                "tool_input": event.get("command") and {"command": event.get("command")} or event.get("tool_input") or {}}
    if name != "preToolUse":
        return None
    tool = event.get("tool_name")
    data = event.get("tool_input")
    if not isinstance(tool, str) or not isinstance(data, dict):
        return None
    return {"hook_event_name": "preToolUse", "tool_name": tool, "tool_input": data}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        if len(argv) != 3:
            return 2
        profile_path, binding_path, log_path = map(Path, argv)
        event = json.load(sys.stdin)
        profile = load_json(profile_path)
        binding = load_json(binding_path)
        hooks_sha = resolve_hooks_digests(profile, profile_path)
        binding_sha = file_digest(binding_path) if binding_path.is_file() else None
        normalized = normalize(event)
        allowed, reason, detail = decide(
            profile, binding, normalized or event,
            hooks_sha256=hooks_sha, binding_sha256=binding_sha,
        )
        record = {"tool": event.get("tool_name") if isinstance(event, dict) else None,
                  "event": event.get("hook_event_name") if isinstance(event, dict) else None,
                  "allowed": allowed, "reason": reason, "detail": detail}
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(json.dumps({
            "permission": "allow" if allowed else "deny",
            "user_message": "Vostok G2: " + reason,
            "agent_message": "Operational protection gate; do not retry a denied action.",
        }))
        return 0
    except Exception:
        # failClosed hooks treat non-zero as block; keep stderr free of secrets.
        print(json.dumps({"permission": "deny", "user_message": "Vostok G2: gate_error"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
