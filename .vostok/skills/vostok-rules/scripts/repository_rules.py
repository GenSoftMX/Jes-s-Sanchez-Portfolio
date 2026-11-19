#!/usr/bin/env python3
"""Repository rule inventory and contracts (Spec 0004, work in progress).

An inventory is not an interpretation, a validation verdict or a credential.
Scan never executes target code and reports needs_interpretation even for a
complete scan. Map validation/binding do not activate host protection.
"""
from __future__ import annotations

import argparse
from collections import Counter, deque
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

SCHEMA = "vostok.source-inventory.v1"
READER = "markdown-and-text-config.v2"
UNIT_IDENTITY = "content-context.v2"
DISCOVERY_FAMILY = "agents-markdown-jintent.v1"
READER_CONTRACT_VERSION = "2.0.0"


def reader_contract_digest():
    """Canonical digest of reader contract version and schema definitions.

    Ties reader compatibility to semantic schema, reader protocol, unit identity,
    and formal contracts rather than raw file bytes of this script, preventing
    cosmetic or maintenance edits from invalidating cached rule maps.
    """
    contracts_file = Path(__file__).with_name("repository_rule_contracts.py")
    contracts_bytes = contracts_file.read_bytes() if contracts_file.exists() else b""
    canonical_sig = f"{SCHEMA}:{READER}:{UNIT_IDENTITY}:{DISCOVERY_FAMILY}:{READER_CONTRACT_VERSION}".encode("utf-8")
    return sha(canonical_sig + sha(contracts_bytes).encode("utf-8"))
MAX_FILE_BYTES = 512 * 1024
MAX_FILES = 400
MAX_TOTAL_BYTES = 8 * 1024 * 1024
MAX_TREE_ENTRIES = 100000
# Versioned discovery profiles. Scan resolves base.v1 plus stack profiles from
# filename signals only (no target code execution). Composition is ordered union.
DISCOVERY_PROFILES = {
    "base.v1": {
        "excluded_dirs": frozenset({".git", "build", "dist", "coverage"}),
        "text_suffixes": frozenset({".md", ".mdx", ".yaml", ".yml", ".json", ".toml", ".sh"}),
        "config_names": frozenset({".gitignore"}),
        "signals": frozenset(),
    },
    "node.v1": {
        "excluded_dirs": frozenset({"node_modules", ".next", ".astro"}),
        "text_suffixes": frozenset({".mjs"}),
        "config_names": frozenset({"package.json", "package-lock.json", ".eslintrc.json", "tsconfig.json"}),
        "signals": frozenset({"package.json", "package-lock.json"}),
    },
    "python.v1": {
        "excluded_dirs": frozenset({".venv", "venv", "__pycache__"}),
        "text_suffixes": frozenset({".py"}),
        "config_names": frozenset({"pyproject.toml", "ruff.toml"}),
        "signals": frozenset({"pyproject.toml", "ruff.toml", "requirements.txt"}),
    },
    "dart.v1": {
        "excluded_dirs": frozenset({".dart_tool"}),
        "text_suffixes": frozenset(),
        "config_names": frozenset({"analysis_options.yaml", "pubspec.yaml", "pubspec.lock", ".pubignore"}),
        "signals": frozenset({"pubspec.yaml"}),
    },
}
SIGNAL_TO_PROFILE = {
    marker: profile_id
    for profile_id, profile in DISCOVERY_PROFILES.items()
    for marker in profile["signals"]
}
# Union of every registered profile (compat for importers; scan uses the resolved set).
EXCLUDED_DIRS = frozenset().union(*(p["excluded_dirs"] for p in DISCOVERY_PROFILES.values()))
TEXT_SUFFIXES = frozenset().union(*(p["text_suffixes"] for p in DISCOVERY_PROFILES.values()))
CONFIG_NAMES = frozenset().union(*(p["config_names"] for p in DISCOVERY_PROFILES.values()))
LINK = re.compile(r"\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)|`([^`\n]+)`")
# Recognized invocation syntax, not an exemption for arbitrary absolute paths.
# Other slash candidates (including /etc/passwd) retain the path checks below.
SLASH_COMMANDS = frozenset({"/feature-delivery", "/present-information", "/skills", "/goal"})
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
NATIVE_NAMES = frozenset({"CLAUDE.md", "GEMINI.md", ".cursorrules", ".windsurfrules", "copilot-instructions.md"})
EPHEMERAL_VOSTOK_DIRS = frozenset({"tmp", "audits", "backups"})
SAFE_HOST_POLICY_KEYS = frozenset({
    "approval_policy", "sandbox_mode", "trust_level", "network_access", "fail_closed",
})
SAFE_HOST_POLICY_VALUES = frozenset({
    "untrusted", "trusted", "never", "on-request", "on-failure", "unless-trusted",
    "read-only", "workspace-write", "danger-full-access", "true", "false", "enabled", "disabled",
})


def summarize_host_config(path, text):
    """Extract redacted structural keys for host_configuration without exposing secret values or paths."""
    if not text:
        return ""
    if str(path).endswith(".json"):
        try:
            data = json.loads(text)
        except ValueError:
            return "json:unparsed"
        if not isinstance(data, dict):
            return "json:non_object"
        keys = []
        for k, v in sorted(data.items()):
            safe_k = k if re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", str(k)) else "<redacted>"
            if isinstance(v, dict):
                sub = [sk if re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", str(sk)) else "<redacted>" for sk in sorted(v)]
                keys.append(f"{safe_k}:{{{','.join(sub)}}}")
            else:
                keys.append(f"{safe_k}=<redacted>")
        return "\n".join(keys)
    out = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            out.append("# <comment_redacted>")
            continue
        if line.startswith("[") and line.endswith("]"):
            redacted_header = re.sub(r'"[^"]*"|\'[^\']*\'', '"<redacted>"', line)
            out.append(redacted_header)
            continue
        m = re.match(r"^([A-Za-z0-9_.-]+)\s*=\s*(.+)$", line)
        if m:
            key, raw_val = m.group(1), m.group(2).strip()
            unquoted = raw_val.strip("\"'")
            if key in SAFE_HOST_POLICY_KEYS and unquoted in SAFE_HOST_POLICY_VALUES:
                out.append(f"{key}={unquoted}")
            else:
                out.append(f"{key}=<redacted>")
        else:
            out.append("<redacted_line>")
    return "\n".join(out)


def compose_profiles(profile_ids):
    """Ordered union of versioned discovery profiles."""
    excluded, suffixes, configs = set(), set(), set()
    for profile_id in profile_ids:
        profile = DISCOVERY_PROFILES[profile_id]
        excluded |= profile["excluded_dirs"]
        suffixes |= profile["text_suffixes"]
        configs |= profile["config_names"]
    return frozenset(excluded), frozenset(suffixes), frozenset(configs)


def discover_signals(root):
    """Filename-only signal pass. Does not read file bodies or execute the target."""
    root = Path(root)
    base_excluded = EXCLUDED_DIRS
    signals, entries = [], 0

    def walk(directory):
        nonlocal entries
        try:
            children = sorted(directory.iterdir())
        except OSError:
            return
        for child in children:
            entries += 1
            if entries > MAX_TREE_ENTRIES:
                return
            if child.name in base_excluded:
                continue
            if child.is_symlink():
                continue
            rel = child.relative_to(root).as_posix()
            if child.is_dir():
                walk(child)
            elif child.is_file() and child.name in SIGNAL_TO_PROFILE:
                signals.append({
                    "path": rel,
                    "marker": child.name,
                    "profile": SIGNAL_TO_PROFILE[child.name],
                })

    walk(root)
    return sorted(signals, key=lambda item: (item["path"], item["profile"]))


def resolve_discovery(root):
    """Resolve base.v1 + stack profiles from observed signals."""
    signals = discover_signals(root)
    stack = sorted({item["profile"] for item in signals})
    profiles = ["base.v1", *stack]
    excluded, suffixes, configs = compose_profiles(profiles)
    return {
        "family": DISCOVERY_FAMILY,
        "composition": "union",
        "signals": signals,
        "profiles": profiles,
        "excluded_dirs": excluded,
        "text_suffixes": suffixes,
        "config_names": configs,
    }


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def read_source(root, name):
    """Open each component without following symlinks, with bounded reads."""
    parts = Path(name).parts
    if not parts or Path(name).is_absolute() or any(p in {".", ".."} for p in parts):
        raise ValueError("invalid source path")
    directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            os.close(directory)
            directory = child
        descriptor = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        try:
            metadata = os.fstat(descriptor)
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > MAX_FILE_BYTES:
                raise ValueError("source is not a bounded regular file")
            with os.fdopen(descriptor, "rb", closefd=False) as handle:
                content = handle.read(MAX_FILE_BYTES + 1)
            if len(content) > MAX_FILE_BYTES:
                raise ValueError("source size limit")
            return content
        finally:
            os.close(descriptor)
    finally:
        os.close(directory)


def git(root, *args):
    # Built-in read-only plumbing, with external filesystem watchers disabled.
    # No checkout, filters, hooks, imports or commands from the receiver.
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_PAGER="cat", GIT_CONFIG_NOSYSTEM="1")
    proc = subprocess.run(["git", "--no-optional-locks", "-c", "core.fsmonitor=false",
                           "-c", "core.untrackedCache=false", "-C", str(root), *args],
                          capture_output=True, timeout=20, env=env)
    if proc.returncode:
        raise ValueError("Git discovery failed")
    return proc.stdout.decode("utf-8", errors="strict").strip()


def _git_proc(root, *args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_PAGER="cat", GIT_CONFIG_NOSYSTEM="1")
    return subprocess.run(["git", "--no-optional-locks", "-c", "core.fsmonitor=false",
                           "-c", "core.untrackedCache=false", "-C", str(root), *args],
                          capture_output=True, timeout=20, env=env)


def resolve_baseline_head(root):
    """Return HEAD sha, or None only when the current branch has no commits yet.

    Unborn = symbolic HEAD ref exists but `show-ref` does not (no commit). Other
    Git failures raise ValueError so scan does not disguise corruption as empty
    history.
    """
    sym = _git_proc(root, "symbolic-ref", "-q", "HEAD")
    if sym.returncode == 0:
        ref = sym.stdout.decode("utf-8", errors="strict").strip()
        if not ref:
            raise ValueError("Git discovery failed")
        exists = _git_proc(root, "show-ref", "--verify", "--quiet", ref)
        if exists.returncode != 0:
            return None
    proc = _git_proc(root, "rev-parse", "-q", "--verify", "HEAD^{commit}")
    if proc.returncode == 0:
        return proc.stdout.decode("utf-8", errors="strict").strip()
    raise ValueError("Git discovery failed")


def source_kind(path, config_names=None):
    names = CONFIG_NAMES if config_names is None else config_names
    parts = path.parts
    if any(parts[i] == ".vostok" and i + 1 < len(parts) and parts[i + 1] in EPHEMERAL_VOSTOK_DIRS for i in range(len(parts))):
        return None
    if path.name == "AGENTS.md":
        return "agent_entry"
    if path.name in NATIVE_NAMES or path.suffix == ".mdc" or ".github/instructions" in path.as_posix():
        return "unsupported_native_candidate"
    if ".vostok" in parts or ".agents" in parts or (".codex" in parts and "skills" in parts):
        return "markdown_resource" if path.suffix in {".md", ".mdx"} else "implementation_resource"
    if path.name in names or ".github/workflows" in path.as_posix():
        return "configuration"
    if path.as_posix() in {".codex/config.toml", ".cursor/hooks.json", ".cursor/cli.json", ".cursor/mcp.json", ".claude/settings.json", ".claude/settings.local.json"}:
        return "host_configuration"
    if any(part in {"adr", "adrs"} for part in parts) and path.suffix == ".md":
        return "decision_candidate"
    return None


def units(path, text):
    """Partition nonblank source lines, without interpreting normative meaning."""
    result, start, lines = [], None, text.splitlines()
    for number in range(1, len(lines) + 2):
        line = lines[number - 1] if number <= len(lines) else ""
        if line.strip() and start is None:
            start = number
        if start is not None and (not line.strip() or (number > start and re.match(r"\s*(?:[-*] |\d+\. |#{1,6} )", line))):
            end = number - 1
            value = "\n".join(lines[start - 1:end])
            result.append({"start": start, "end": end, "sha256": sha(value.encode()), "text": value})
            start = number if line.strip() else None
    # Preserve blank-line moves, not semantic moves: changing a heading, text,
    # or unit order invalidates this whole source's interpretation conservatively.
    context = sha(canonical([unit["sha256"] for unit in result]))
    counts = Counter(unit["sha256"] for unit in result)
    occurrences = Counter()
    for unit in result:
        content = unit["sha256"]
        occurrences[content] += 1
        ambiguous = counts[content] > 1
        identity = [UNIT_IDENTITY, path, context, content]
        if ambiguous:
            identity.append(occurrences[content])
        unit.update(id=sha(canonical(identity)), identity_version=UNIT_IDENTITY,
                    context_sha256=context, ambiguous_duplicate=ambiguous)
    return result


def markdown_references(text):
    """Keep fenced examples visible without promoting their paths to imports.

    Source units still include the full example for guided interpretation.
    Only reference traversal is classified here; this is not a rule extractor.
    """
    fence = None
    for line in text.splitlines():
        marker = FENCE.match(line)
        if marker:
            run, suffix = marker.groups()
            if fence is None:
                fence = run
                continue
            if run[0] == fence[0] and len(run) >= len(fence) and not suffix.strip():
                fence = None
                continue
        for match in LINK.finditer(line):
            yield match, fence is not None


def scan(root):
    root = Path(root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("root must be a directory")
    top = Path(git(root, "rev-parse", "--show-toplevel")).resolve()
    if top != root:
        raise ValueError("root must be the Git worktree root")
    admin = Path(git(root, "rev-parse", "--absolute-git-dir")).resolve()
    worktree = sha(canonical([str(root), str(admin)]))
    discovery = resolve_discovery(root)
    excluded_dirs = discovery["excluded_dirs"]
    text_suffixes = discovery["text_suffixes"]
    config_names = discovery["config_names"]
    submodules = set()
    for record in git(root, "ls-files", "--stage", "-z").split("\0"):
        if record.startswith("160000 "):
            submodules.add(record.split("\t", 1)[1])
    errors, warnings, exclusions, candidates, aliases = [], [], [], {}, []
    entries = 0
    directory_stamps = {}

    def walk(directory):
        nonlocal entries
        try:
            directory_stamps[directory] = directory.stat().st_mtime_ns
            children = sorted(directory.iterdir())
        except OSError:
            errors.append({"path": directory.relative_to(root).as_posix(), "reason": "unreadable_directory"})
            return
        for child in children:
            entries += 1
            rel = child.relative_to(root)
            if entries > MAX_TREE_ENTRIES:
                if not any(e["reason"] == "tree_limit" for e in errors):
                    errors.append({"path": ".", "reason": "tree_limit"})
                return
            if rel.as_posix() in submodules or child.name in excluded_dirs:
                exclusions.append({"path": rel.as_posix(), "reason": "submodule" if rel.as_posix() in submodules else "dependency_or_generated_boundary"})
                continue
            if not child.is_symlink() and len(rel.parts) >= 2 and rel.parts[-2] == ".vostok" and child.name in EPHEMERAL_VOSTOK_DIRS:
                continue
            kind = source_kind(rel, config_names)
            if child.is_symlink():
                try:
                    target = child.resolve(strict=True)
                    target_rel = target.relative_to(root)
                    if child.is_dir() and any(part.startswith(".vostok") or part.startswith(".agents") for part in target_rel.parts):
                        aliases.append({"path": rel.as_posix(), "target": target_rel.as_posix()})
                    elif kind:
                        if target.is_file():
                            aliases.append({"path": rel.as_posix(), "target": target_rel.as_posix()})
                            candidates[target_rel.as_posix()] = source_kind(target_rel, config_names) or kind
                        else:
                            errors.append({"path": rel.as_posix(), "reason": "unsupported_symlink"})
                    else:
                        exclusions.append({"path": rel.as_posix(), "reason": "symlink_not_followed"})
                except (OSError, ValueError, RuntimeError):
                    if kind or child.name in {".vostok", ".agents", ".codex", ".cursor", ".claude"}:
                        errors.append({"path": rel.as_posix(), "reason": "symlink_escape_cycle_or_missing"})
                    else:
                        exclusions.append({"path": rel.as_posix(), "reason": "symlink_not_followed"})
                continue
            if child.is_dir():
                walk(child)
            elif kind:
                candidates[rel.as_posix()] = kind

    walk(root)
    if "AGENTS.md" not in candidates:
        errors.append({"path": "AGENTS.md", "reason": "entry_missing"})
    pending = deque(sorted(candidates))
    sources, references, seen, total = [], [], set(), 0
    while pending:
        name = pending.popleft()
        if name in seen:
            continue
        seen.add(name)
        kind = candidates.get(name, "referenced_resource")
        if len(sources) >= MAX_FILES:
            errors.append({"path": name, "reason": "source_count_limit"})
            break
        path = root / name
        try:
            target = path.resolve(strict=True)
            target.relative_to(root)
            if not target.is_file():
                raise ValueError("not a regular file")
            if path.stat().st_size > MAX_FILE_BYTES:
                errors.append({"path": name, "reason": "source_size_limit"})
                continue
            content = read_source(root, name)
            total += len(content)
            if total > MAX_TOTAL_BYTES:
                errors.append({"path": name, "reason": "total_size_limit"})
                break
            text = content.decode("utf-8")
        except (OSError, ValueError, RuntimeError):
            errors.append({"path": name, "reason": "unreadable_missing_or_escaping_source"})
            continue
        if kind == "unsupported_native_candidate":
            # Inventariar sin tumbar complete: descubrir ≠ interpretar (opción B).
            warnings.append({"path": name, "reason": "native_reader_not_supported"})
        # Host configuration can contain credentials. Keep hashes and line
        # spans, never values, in the inventory. Interpretation remains pending.
        source_units = units(name, text)
        if kind == "implementation_resource":
            source_units = []
        if kind == "host_configuration":
            source_units = [{**unit, "text": None, "withheld": "host_configuration_values",
                             "redacted_structure": summarize_host_config(name, unit["text"])} for unit in source_units]
        sources.append({"path": name, "kind": kind, "sha256": sha(content), "bytes": len(content),
                        "units": source_units})
        if path.suffix not in {".md", ".mdx"} and path.name != "AGENTS.md":
            continue
        for match, example in markdown_references(text):
            value = match.group(1) or match.group(2)
            if any(char in value for char in "\n\r\x00") or " " in value:
                continue
            if example:
                references.append({"source": name, "target": value, "status": "example_not_loaded"})
                continue
            if match.group(2) and value in SLASH_COMMANDS:
                references.append({"source": name, "target": value, "status": "command_not_loaded"})
                continue
            url = urlsplit(value)
            if url.scheme or url.netloc:
                if match.group(1):
                    references.append({"source": name, "target": value, "status": "remote_not_loaded"})
                continue
            raw = unquote(url.path)
            if not raw or raw.startswith("#"):
                continue
            # Inline code is a path candidate, not a command or a glob expansion.
            if match.group(2) and ("/" not in raw and "." not in raw or any(c in raw for c in "*?<>|={}")):
                continue
            candidate = path.parent / raw
            if Path(raw).is_absolute():
                references.append({"source": name, "target": raw, "status": "absolute_not_loaded"})
                errors.append({"path": name, "reason": "absolute_reference"})
                continue
            try:
                relative = candidate.resolve().relative_to(root).as_posix()
            except (OSError, ValueError, RuntimeError):
                references.append({"source": name, "target": raw, "status": "escaping_reference"})
                errors.append({"path": name, "reason": "escaping_reference"})
                continue
            if any(part in excluded_dirs for part in Path(relative).parts):
                references.append({"source": name, "target": relative, "status": "excluded_boundary"})
                continue
            if candidate.is_dir():
                references.append({"source": name, "target": relative, "status": "directory_inventory"})
                continue
            supported = candidate.suffix in text_suffixes or candidate.name in config_names
            normative = source_kind(Path(relative), config_names) is not None
            if not candidate.is_file():
                if match.group(1) and (supported or normative):
                    errors.append({"path": relative, "reason": "broken_local_reference"})
                references.append({"source": name, "target": relative, "status": "missing_candidate"})
            elif supported:
                references.append({"source": name, "target": relative, "status": "loaded"})
                if relative not in seen:
                    candidates.setdefault(relative, source_kind(Path(relative), config_names) or "referenced_resource")
                    pending.append(relative)
            else:
                references.append({"source": name, "target": relative, "status": "context_not_interpreted"})
    # Detect mutations during scan; no promise to lock external processes.
    for source in sources:
        try:
            if sha(read_source(root, source["path"])) != source["sha256"]:
                errors.append({"path": source["path"], "reason": "source_changed_during_scan"})
        except (OSError, ValueError):
            errors.append({"path": source["path"], "reason": "source_disappeared_during_scan"})
    for directory, stamp in directory_stamps.items():
        try:
            if directory.stat().st_mtime_ns != stamp:
                errors.append({"path": directory.relative_to(root).as_posix(), "reason": "directory_changed_during_scan"})
        except OSError:
            errors.append({"path": directory.relative_to(root).as_posix(), "reason": "directory_disappeared_during_scan"})
    head = resolve_baseline_head(root)
    limits = ["structural_inventory_only", "no_semantic_completeness_claim",
              "native_candidates_inventoried_without_reader", "no_target_code_executed",
              "no_protection_activated", "external_concurrent_changes_not_locked",
              "discovery_profiles_signal_union"]
    if head is None:
        limits.append("unborn_or_absent_head")
    result = {"schema": SCHEMA, "reader": READER, "unit_identity": UNIT_IDENTITY,
              "reader_sha256": reader_contract_digest(),
              "root": str(root), "worktree_id": worktree,
              "baseline_head": head, "profile": DISCOVERY_FAMILY,
              "discovery": {
                  "family": discovery["family"],
                  "composition": discovery["composition"],
                  "signals": discovery["signals"],
                  "profiles": discovery["profiles"],
              },
              "boundary": {
                  "excluded_directory_names": sorted(excluded_dirs),
                  "text_suffixes": sorted(text_suffixes),
                  "config_names": sorted(config_names),
                  "max_files": MAX_FILES,
                  "max_file_bytes": MAX_FILE_BYTES,
                  "max_total_bytes": MAX_TOTAL_BYTES,
                  "max_tree_entries": MAX_TREE_ENTRIES,
              },
              "sources": sorted(sources, key=lambda s: s["path"]), "aliases": sorted(aliases, key=lambda a:a["path"]),
              "references": sorted(references, key=lambda r:(r["source"],r["target"],r["status"])),
              "exclusions": sorted(exclusions, key=lambda e:e["path"]),
              "warnings": sorted(warnings, key=lambda w: (w["path"], w["reason"])),
              "errors": errors,
              "complete": not errors, "status": "needs_interpretation" if not errors else "blocked",
              "limits": limits}
    result["inventory_digest"] = sha(canonical(result))
    return result


def required_protection(args, phase_result, inventory=None, mapping=None, task=None, binding=None):
    """Validate actual workspace hooks and task identity before executable checks.

    This contrasts local artifacts; it does not observe a running host session.
    No profile or hook argument is an authorization to run target code.
    """
    from repository_rule_protection import digest, protection_required_result
    profile = load_json(args.protection_profile) if args.protection_profile else None
    hooks = load_json(args.hooks) if args.hooks else None
    root = args.root.resolve(strict=True)
    context = {"root": str(root), "worktree_id": (inventory or {}).get("worktree_id"),
               "map_digest": digest(mapping) if mapping is not None else None,
               "task_digest": digest(task) if task is not None else None,
               "binding_digest": digest(binding) if binding is not None else None,
               "effective_hooks_sha256": None}
    try:
        actual_hooks = json.loads(read_source(root, ".cursor/hooks.json"))
        context["effective_hooks_sha256"] = digest(actual_hooks)
    except (OSError, ValueError):
        pass
    return protection_required_result(phase_result, profile=profile, hooks=hooks, context=context)


def emit_result(args, result, exit_code):
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        destination = args.output.resolve()
        admin_cache = Path(git(args.root.resolve(), "rev-parse", "--absolute-git-dir")).resolve() / "vostok-rules"
        if destination.is_relative_to(args.root.resolve()) and not destination.is_relative_to(admin_cache):
            raise ValueError("inventory output must be outside the receiver root")
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(output)
    else:
        print(output, end="")
    return exit_code


def main(argv=None):
    from repository_rule_contracts import bind, draft, validate_map
    from repository_rule_protection import (CODEX_HOST, CURSOR_HOST, cursor_hooks_plan, digest as protection_digest,
                                            validate_profile)
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name,help_text in (("scan","Read sources; never activates protection"),
                           ("draft","Prepare unresolved source treatments for the harness"),
                           ("validate","Check map coverage, citations and current inventory"),
                           ("bind","Derive every rule's applicability for a task"),
                           ("explain","Explain applicability and source citations"),
                           ("preflight","Evaluate obligations before material changes"),
                           ("verify","Run authorized checks and evaluate current rules"),
                           ("task","Reuse a validated map and compose task binding with preflight/verify"),
                           ("incorporate","Preview adding the skill/tools without overwriting"),
                           ("protection-plan","Preview a Cursor G2 hooks+profile plan (Codex unsupported)")):
        command = commands.add_parser(name,help=help_text)
        command.add_argument("--root", type=Path, required=True)
        command.add_argument("--output", type=Path)
        command.add_argument("--protection",choices=["not_requested","required"],default="not_requested")
        command.add_argument("--protection-profile",type=Path,help="Active G2 profile for --protection required")
        command.add_argument("--hooks",type=Path,help="Cursor hooks.json to validate with the profile")
        if name=="draft":
            command.add_argument("--carry-from",type=Path,help="Prior rule map to carry unchanged unit treatments and rules from")
        if name in {"validate","bind","explain","preflight","verify","task"}:command.add_argument("--map",dest="mapping",type=Path,required=name!="task")
        if name in {"bind","explain","preflight","verify","task"}:command.add_argument("--task",type=Path,required=True)
        if name in {"bind","explain","preflight","verify","task"}:
            command.add_argument("--prior-map",type=Path,help="Prior agreement map when the task modifies repository rules")
        if name in {"preflight","verify","task"}:
            command.add_argument("--authorize-check",action="append",default=[])
            command.add_argument("--guided-reviews",type=Path)
        if name == "task":
            command.add_argument("--phase", choices=["preflight", "verify"], required=True)
            command.add_argument("--cache", type=Path, help="Map cache; default <git-dir>/vostok-rules/task-cache")
            command.add_argument("--details", action="store_true", help="Include the complete unchanged phase verdict")
        if name=="explain":command.add_argument("--path",required=True)
        if name=="incorporate":
            command.add_argument("--apply",action="store_true")
            command.add_argument("--plan-digest")
        if name=="protection-plan":
            command.add_argument("--host",choices=[CURSOR_HOST,CODEX_HOST],default=CURSOR_HOST)
            command.add_argument("--host-version",required=True)
            command.add_argument("--map-digest",required=True)
            command.add_argument("--task-digest",required=True)
            command.add_argument("--binding-digest",required=True)
            command.add_argument("--gate-command",required=True,help="Absolute or repo-relative gate command for hooks")
    args = parser.parse_args(argv)
    try:
        inventory = mapping = task = binding = protection_guard = None
        task_entry = args.command == "task"
        selected_mapping = cache_metadata = None
        if task_entry:
            from repository_rule_cache import cache_directory, select_mapping, task_result
            inventory = scan(args.root)
            admin = Path(git(args.root.resolve(), "rev-parse", "--absolute-git-dir"))
            directory = cache_directory(args.root.resolve(), admin, args.cache)
            selected_mapping, cache_metadata = select_mapping(inventory, directory, args.mapping, load_json)
            if selected_mapping is None:
                result = {"status": "blocked", "blockers": cache_metadata["blockers"]}
                return emit_result(args, task_result(result, args.phase, cache_metadata, details=args.details), 1)
            args.command = args.phase
        # Incorporation must work even before the receiver has an entrypoint.
        if args.command=="incorporate":
            from repository_rules_install import apply, payload, plan
            root=args.root.resolve(strict=True)
            if Path(git(root,"rev-parse","--show-toplevel")).resolve()!=root:
                raise ValueError("root must be the Git worktree root")
            files=payload(Path(__file__).resolve().parents[1])
            result=plan(root,files,read_source)
            if args.apply and args.protection!="required":
                if not args.plan_digest:raise ValueError("apply requires a concrete preview plan digest")
                result=apply(root,files,args.plan_digest,read_source)
            exit_code=1 if result["status"]=="blocked" else 0
        elif args.command=="protection-plan":
            root=args.root.resolve(strict=True)
            inventory=scan(root)
            hooks=cursor_hooks_plan(args.gate_command)
            profile={"schema":"vostok.protection-profile.v1","host":args.host,"host_version":args.host_version,
                     "surface":"cli-print" if args.host==CURSOR_HOST else "cli-exec","fail_closed":True,
                     "covered_tools":["Write","Edit","Shell"],"mcp_policy":"deny_all","task_policy":"deny_all",
                     "hooks_sha256":protection_digest(hooks),"root":str(root),
                     "worktree_id":inventory["worktree_id"],"map_digest":args.map_digest,
                     "task_digest":args.task_digest,"binding_digest":args.binding_digest,"status":"active",
                     "limits":["cli_not_desktop","shell_denied_at_gate","mcp_denied_at_gate",
                               "binding_backed_not_operator_permit"]}
            blockers=validate_profile(profile)
            result={"status":"unsupported_host" if args.host==CODEX_HOST else ("blocked" if blockers else "preview"),
                    "hooks":hooks,"profile":profile,"blockers":blockers,
                    "limits":["preview_only","does_not_install_hooks","codex_unsupported_for_required"]}
            exit_code=1 if result["status"]!="preview" else 0
        else:
            inventory = scan(args.root)
            result,exit_code = inventory,1
        if args.command == "draft":
            prior_mapping = load_json(args.carry_from) if getattr(args, "carry_from", None) else None
            result = draft(inventory, prior_mapping=prior_mapping)
        elif args.command in {"validate","bind","explain","preflight","verify"}:
            mapping = selected_mapping if task_entry else load_json(args.mapping)
            blockers = validate_map(inventory,mapping)
            if args.command=="validate":
                result={"status":"blocked" if blockers else "map_ready_for_binding", "blockers":blockers,
                        "inventory_digest":inventory["inventory_digest"],
                        "limits":["structural_map_validation", "semantic_interpretation_guided", "independent_review_pending", "no_host_protection"]}
                exit_code=1 if blockers else 0
            else:
                task=load_json(args.task)
                prior_mapping=load_json(args.prior_map) if getattr(args,"prior_map",None) else None
                result=bind(inventory,mapping,task,sha(canonical(mapping)),sha(canonical(task)),prior_mapping=prior_mapping)
                binding = result
                exit_code=1 if result["blockers"] else 0
                if args.command in {"preflight","verify"}:
                    if args.protection == "required":
                        protection_guard = required_protection(args, result, inventory, mapping, task, binding)
                    if protection_guard is None or protection_guard["status"] == "protection_ready":
                        from repository_rule_evaluator import evaluate
                        result=evaluate(args.root.resolve(),inventory,mapping,task,args.command,args.authorize_check,
                                        load_json(args.guided_reviews) if args.guided_reviews else {},read_source,
                                        Path(__file__).with_name("check_scope_evidence.py"),scan,prior_mapping=prior_mapping)
                        exit_code=1 if result["status"]=="blocked" else 0
                if args.command=="explain":
                    if args.path not in task["paths"]:
                        raise ValueError("explain path must belong to the declared task scope")
                    from repository_rule_contracts import applicability
                    selected={**task,"paths":[args.path]}
                    unit_sources={unit["id"]:{"path":source["path"],"source_sha256":source["sha256"],"start":unit["start"],"end":unit["end"]} for source in inventory["sources"] for unit in source["units"]}
                    result={"status":result["status"],"path":args.path,"blockers":result["blockers"],
                            "rules":[{"id":rule["id"],"applicability":applicability(rule,selected),"modality":rule["modality"],
                                      "quote":rule["quote"],"sources":[unit_sources[uid] for uid in rule["source_units"]],
                                      "evaluation":rule["evaluation"]} for rule in mapping["rules"]],
                            "limits":result["limits"]}
        if args.protection=="required":
            result = (protection_guard if protection_guard is not None and protection_guard["status"] != "protection_ready"
                      else required_protection(args, result, inventory, mapping, task, binding))
            exit_code=0 if result["status"]=="protection_ready" and result.get("phase_status") not in {None,"blocked"} else 1
        if task_entry:
            result = task_result(result, args.phase, cache_metadata, details=args.details)
        return emit_result(args, result, exit_code)  # Never host activation.
    except (OSError, ValueError, TypeError, KeyError, RuntimeError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "invocation_error", "reason": str(exc)}), file=sys.stderr)
        return 2


def load_json(path):
    if path.stat().st_size > 16*1024*1024:
        raise ValueError("contract exceeds size limit")
    def unique_object(pairs):
        result={}
        for key,value in pairs:
            if key in result:raise ValueError("duplicate JSON object key")
            result[key]=value
        return result
    return json.loads(path.read_text(encoding="utf-8"),object_pairs_hook=unique_object)


if __name__ == "__main__":
    raise SystemExit(main())
