"""Operational G2 protection profiles for Spec 0004.

Cursor CLI is the only host with a measured fail-closed path so far. Codex remains
explicitly unsupported for --protection required. This module never claims desktop
coverage, MCP/Task write safety, or E6 without a matching active profile.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from repository_rule_contracts import relative_path, require

PROFILE_SCHEMA = "vostok.protection-profile.v1"
CURSOR_HOST = "cursor-cli"
CODEX_HOST = "codex-cli"
READ_TOOLS = frozenset({"Read", "Glob", "Grep", "SemanticSearch"})
WRITE_TOOLS = frozenset({"Write", "Edit", "Delete", "StrReplace"})
# Full required coverage for "all writes in root" needs Shell gated or denied.
REQUIRED_WRITE_SURFACE = frozenset({"Write", "Edit", "Shell"})


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_profile(profile):
    require(isinstance(profile, dict), "invalid protection profile")
    required = {"schema", "host", "host_version", "surface", "fail_closed", "covered_tools",
                "mcp_policy", "task_policy", "hooks_sha256", "root", "worktree_id",
                "map_digest", "task_digest", "binding_digest", "status", "limits"}
    require(set(profile) == required, "invalid protection profile fields")
    require(profile["schema"] == PROFILE_SCHEMA, "unsupported protection profile schema")
    require(profile["host"] in {CURSOR_HOST, CODEX_HOST}, "unsupported protection host")
    require(isinstance(profile["host_version"], str) and profile["host_version"], "missing host version")
    require(profile["surface"] in {"cli-print", "cli-exec", "desktop"}, "unsupported protection surface")
    require(profile["fail_closed"] is True, "protection profile must be fail-closed")
    require(isinstance(profile["covered_tools"], list) and profile["covered_tools"]
            and all(isinstance(t, str) and t for t in profile["covered_tools"]), "invalid covered_tools")
    require(profile["mcp_policy"] in {"deny_all", "unsupported"}, "invalid mcp_policy")
    require(profile["task_policy"] in {"deny_all", "unsupported"}, "invalid task_policy")
    require(isinstance(profile["hooks_sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", profile["hooks_sha256"]),
            "invalid hooks digest")
    require(isinstance(profile["root"], str) and Path(profile["root"]).is_absolute(), "profile root must be absolute")
    for key in ("worktree_id", "map_digest", "task_digest", "binding_digest"):
        require(isinstance(profile[key], str) and profile[key], f"missing {key}")
    require(profile["status"] in {"active", "inactive"}, "invalid profile status")
    require(isinstance(profile["limits"], list) and all(isinstance(x, str) and x for x in profile["limits"]),
            "invalid profile limits")
    blockers = []
    if profile["host"] == CODEX_HOST:
        blockers.append({"reason": "codex_protection_unsupported",
                         "detail": "measured Codex hook profile allows write after crash/empty"})
    if profile["status"] != "active":
        blockers.append({"reason": "protection_inactive"})
    if profile["surface"] == "desktop":
        blockers.append({"reason": "desktop_protection_unmeasured"})
    elif profile["host"] == CURSOR_HOST and profile["surface"] != "cli-print":
        blockers.append({"reason": "cursor_surface_unmeasured"})
    missing = sorted(REQUIRED_WRITE_SURFACE - set(profile["covered_tools"]))
    if missing:
        blockers.append({"reason": "required_write_surface_uncovered", "missing": missing})
    if profile["mcp_policy"] != "deny_all":
        blockers.append({"reason": "mcp_writes_not_denied"})
    if profile["task_policy"] != "deny_all":
        blockers.append({"reason": "task_writes_not_denied"})
    return blockers


def inspect_cursor_hooks(hooks):
    """Structural coverage check for a Cursor hooks.json document."""
    require(isinstance(hooks, dict) and hooks.get("version") == 1, "invalid Cursor hooks document")
    entries = hooks.get("hooks")
    require(isinstance(entries, dict), "hooks object required")
    pre = entries.get("preToolUse")
    require(isinstance(pre, list) and pre, "preToolUse hooks required")
    shell = entries.get("beforeShellExecution")
    mcp = entries.get("beforeMCPExecution")
    report = {"preToolUse": [], "beforeShellExecution": [], "beforeMCPExecution": [],
              "fail_closed": True, "limits": []}
    for item in pre:
        require(isinstance(item, dict) and isinstance(item.get("command"), str) and item["command"], "invalid preToolUse")
        report["preToolUse"].append({"matcher": item.get("matcher", "*"), "failClosed": item.get("failClosed") is True})
        if item.get("failClosed") is not True:
            report["fail_closed"] = False
    if not any(item.get("matcher", "*") == "*" for item in pre):
        report["fail_closed"] = False
        report["limits"].append("preToolUse_all_tools_uncovered")
    if isinstance(shell, list) and shell:
        for item in shell:
            require(isinstance(item, dict) and isinstance(item.get("command"), str) and item["command"], "invalid shell hook")
            report["beforeShellExecution"].append({"failClosed": item.get("failClosed") is True})
            if item.get("failClosed") is not True:
                report["fail_closed"] = False
        if not any(item.get("matcher", "*") == "*" for item in shell):
            report["fail_closed"] = False
            report["limits"].append("beforeShellExecution_all_tools_uncovered")
    else:
        report["limits"].append("beforeShellExecution_absent")
    if isinstance(mcp, list) and mcp:
        for item in mcp:
            require(isinstance(item, dict) and isinstance(item.get("command"), str) and item["command"], "invalid MCP hook")
            report["beforeMCPExecution"].append({"failClosed": item.get("failClosed") is True})
            if item.get("failClosed") is not True:
                report["fail_closed"] = False
        if not any(item.get("matcher", "*") == "*" for item in mcp):
            report["fail_closed"] = False
            report["limits"].append("beforeMCPExecution_all_tools_uncovered")
    else:
        report["limits"].append("beforeMCPExecution_absent")
    if not report["fail_closed"]:
        report["limits"].append("fail_open_hook_present")
    return report


def cursor_hooks_plan(gate_command: str) -> dict:
    """Minimal fail-closed Cursor hooks that cover Write/Edit/Shell/MCP entrypoints."""
    entry = {"command": gate_command, "matcher": "*", "timeout": 15, "failClosed": True}
    return {"version": 1, "hooks": {
        "preToolUse": [entry],
        "beforeShellExecution": [dict(entry)],
        "beforeMCPExecution": [dict(entry)],
    }}


def binding_allows_path(binding, relative):
    relative_path(relative)
    if not isinstance(binding, dict) or binding.get("status") == "blocked":
        return False, "binding_blocked_or_missing"
    task_paths = binding.get("task_paths")
    if not isinstance(task_paths, list):
        return False, "binding_missing_task_paths"
    if relative not in task_paths:
        return False, "path_outside_task_scope"
    return True, "path_in_bound_task"


def extract_tool_path(tool_input):
    if not isinstance(tool_input, dict):
        return None
    paths = [tool_input[key] for key in ("file_path", "path", "target_file", "relative_workspace_path")
             if key in tool_input and isinstance(tool_input[key], str)]
    if len(set(paths)) != 1:
        return None
    return paths[0]


def decide(profile, binding, event, *, hooks_sha256=None, binding_sha256=None):
    """Translate a host pre-tool event into allow/deny using the bound task."""
    blockers = validate_profile(profile)
    if blockers:
        return False, blockers[0]["reason"], {"blockers": blockers}
    if hooks_sha256 is None:
        return False, "hooks_digest_missing", {}
    valid_hooks = set(hooks_sha256) if isinstance(hooks_sha256, (set, frozenset, list, tuple)) else {hooks_sha256}
    if profile["hooks_sha256"] not in valid_hooks:
        return False, "hooks_digest_mismatch", {}
    if not isinstance(event, dict):
        return False, "invalid_event", {}
    name = event.get("hook_event_name") or event.get("event")
    tool = event.get("tool_name")
    if name in {"beforeShellExecution", "beforeMCPExecution"} or tool == "Shell":
        return False, "shell_or_mcp_denied_by_profile", {"tool": tool or name}
    if name not in {"preToolUse", "PreToolUse"} and tool not in WRITE_TOOLS | READ_TOOLS:
        return False, "unsupported_event", {"event": name, "tool": tool}
    if tool in READ_TOOLS:
        return True, "read_only", {"tool": tool}
    if tool not in WRITE_TOOLS:
        return False, "unsupported_or_uncovered_tool", {"tool": tool}
    if tool not in profile["covered_tools"]:
        return False, "tool_not_in_covered_surface", {"tool": tool}
    raw = extract_tool_path(event.get("tool_input"))
    if raw is None:
        return False, "missing_or_ambiguous_path", {}
    root = Path(profile["root"]).resolve()
    try:
        target = Path(raw)
        target = target if target.is_absolute() else (root / target)
        target = target.resolve()
        relative = target.relative_to(root).as_posix()
    except (OSError, ValueError):
        return False, "path_escapes_root", {}
    if any(part in {".git", ".cursor", ".codex", ".claude", ".agents"} for part in Path(relative).parts):
        return False, "protected_configuration", {"path": relative}
    if not isinstance(binding, dict):
        return False, "binding_blocked_or_missing", {}
    if not isinstance(binding.get("worktree_id"), str) or not binding["worktree_id"] or binding["worktree_id"] != profile["worktree_id"]:
        return False, "worktree_mismatch", {}
    if not isinstance(binding.get("map_digest"), str) or not binding["map_digest"] or binding["map_digest"] != profile["map_digest"]:
        return False, "stale_map_digest", {}
    if not isinstance(binding.get("task_digest"), str) or not binding["task_digest"] or binding["task_digest"] != profile["task_digest"]:
        return False, "stale_task_digest", {}
    valid_binding = {digest(binding)}
    if isinstance(binding_sha256, str) and binding_sha256:
        valid_binding.add(binding_sha256)
    elif isinstance(binding_sha256, (set, frozenset, list, tuple)):
        valid_binding.update(x for x in binding_sha256 if isinstance(x, str) and x)
    if profile["binding_digest"] not in valid_binding:
        return False, "stale_binding_digest", {}
    ok, reason = binding_allows_path(binding, relative)
    return ok, reason, {"path": relative, "tool": tool}


def protection_required_result(phase_result, profile=None, hooks=None, hooks_sha256=None, *, context=None):
    """Gate used by --protection required. No silent downgrade to unprotected success."""
    base = {"schema": "vostok.rule-command-result.v1", "phase_status": phase_result.get("status"),
            "phase_result": phase_result}
    if profile is None:
        return {**base, "status": "blocked_protection_unavailable",
                "limits": ["operational_G2_profile_missing", "no_silent_downgrade", "no_host_protection_activated"]}
    try:
        blockers = list(validate_profile(profile))
    except (ValueError, TypeError):
        blockers = [{"reason": "invalid_protection_profile"}]
        profile = {}
    if hooks is None:
        blockers.append({"reason": "operational_hooks_missing"})
    else:
        try:
            inspection = inspect_cursor_hooks(hooks)
        except (ValueError, TypeError):
            inspection = {"fail_closed": False, "limits": ["invalid_hooks_document"]}
        if not inspection["fail_closed"]:
            blockers.append({"reason": "hooks_not_fail_closed"})
        if "beforeShellExecution_absent" in inspection["limits"]:
            blockers.append({"reason": "shell_hook_absent"})
        if "beforeMCPExecution_absent" in inspection["limits"]:
            blockers.append({"reason": "mcp_hook_absent"})
        for reason in ("preToolUse_all_tools_uncovered", "invalid_hooks_document"):
            if reason in inspection["limits"]:
                blockers.append({"reason": reason})
        canonical = digest(hooks)
        if hooks_sha256 is None:
            hooks_sha256 = canonical
        if hooks_sha256 != profile.get("hooks_sha256") and canonical != profile.get("hooks_sha256"):
            blockers.append({"reason": "hooks_digest_mismatch"})
    if context is not None:
        for key in ("root", "worktree_id", "map_digest", "task_digest", "binding_digest"):
            expected = context.get(key)
            actual = profile.get(key)
            if key == "root" and isinstance(actual, str) and isinstance(expected, str):
                actual, expected = str(Path(actual).resolve()), str(Path(expected).resolve())
            if not expected or actual != expected:
                blockers.append({"reason": "protection_context_mismatch", "field": key})
        if not context.get("effective_hooks_sha256"):
            blockers.append({"reason": "workspace_hooks_missing_or_unreadable"})
        elif context["effective_hooks_sha256"] != digest(hooks):
            blockers.append({"reason": "workspace_hooks_mismatch"})
    if phase_result.get("status") == "blocked":
        blockers.append({"reason": "phase_blocked"})
    if blockers:
        return {**base, "status": "blocked_protection_unavailable", "blockers": blockers,
                "limits": ["no_silent_downgrade", "protection_profile_or_coverage_insufficient",
                           "codex_remains_unsupported_for_required"]}
    return {**base, "status": "protection_ready",
            "profile_digest": digest(profile),
            "limits": list(profile["limits"]) + [
                "host_protection_depends_on_active_hooks",
                "cli_surface_only" if profile["surface"].startswith("cli") else "surface_limited",
                "shell_and_mcp_denied_by_policy",
                "not_universal_enforcement",
            ]}
