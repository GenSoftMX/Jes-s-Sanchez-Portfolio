"""Disposable map cache for the task entrypoint; never a permission or review actor.

Entries are immutable, tied to worktree and reader, and validated against the
current inventory. Multiple different usable maps block rather than selecting by
mtime. Only exact carry of previously reviewed units can prepare an updated map.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from repository_rule_contracts import draft, require, validate_map

CACHE_SCHEMA = "vostok.rule-map-cache.v1"
MAX_ENTRIES = 128


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def cache_directory(root, admin, requested=None):
    directory = Path(requested).resolve() if requested else Path(admin).resolve() / "vostok-rules/task-cache"
    require(not directory.is_relative_to(root) or directory.is_relative_to(Path(admin).resolve() / "vostok-rules"),
            "task cache must be administrative or outside the receiver")
    return directory


def write_immutable(directory, name, value):
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    content = json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(content)
    except FileExistsError:
        require(not path.is_symlink() and path.is_file() and path.read_text() == content,
                "existing cache entry conflicts; nothing overwritten")
    return path


def remember(directory, inventory, mapping):
    entry = {"schema": CACHE_SCHEMA, "worktree_id": inventory["worktree_id"],
             "reader_sha256": inventory["reader_sha256"], "mapping": mapping}
    return write_immutable(directory, "map-" + digest(entry) + ".json", entry)


def blocked(reason, *, details=None, next_step="Provide an explicitly reviewed current map with --map."):
    return None, {"mode": "blocked", "blockers": [{"reason": reason, **(details or {})}], "next_step": next_step}


def select_mapping(inventory, directory, explicit, loader):
    """Return (mapping or None, descriptive cache metadata); never run checks."""
    if not inventory.get("complete"):
        return blocked("incomplete_inventory", details={"errors": inventory.get("errors", [])},
                       next_step="Resolve the inventory blockers before integration.")
    total = sum(len(source["units"]) for source in inventory["sources"])
    if explicit is not None:
        try:
            mapping = loader(explicit)
            blockers = validate_map(inventory, mapping)
        except (OSError, ValueError, TypeError, KeyError) as error:
            return blocked("explicit_map_invalid_or_stale", details={"detail": str(error)[:500]})
        if blockers:
            return None, {"mode": "blocked", "blockers": blockers,
                          "next_step": "Finish interpretation/review and validate the map before use."}
        path = remember(directory, inventory, mapping)
        return mapping, {"mode": "explicit", "entry": str(path), "reused_units": 0, "unresolved_units": 0}

    paths = sorted(directory.glob("map-*.json")) if directory.is_dir() else []
    if not paths:
        return blocked("rule_map_missing")
    if len(paths) > MAX_ENTRIES:
        return blocked("cache_entry_limit", next_step="Choose a smaller explicit cache directory or an explicit map.")
    candidates, partial, incompatible = {}, [], []
    for path in paths:
        try:
            require(not path.is_symlink(), "symlink cache entry is unsupported")
            entry = loader(path)
            require(isinstance(entry, dict) and set(entry) == {"schema", "worktree_id", "reader_sha256", "mapping"}
                    and entry["schema"] == CACHE_SCHEMA, "invalid cache entry")
            require(isinstance(entry["mapping"], dict), "invalid cached map")
            require(path.name == "map-" + digest(entry) + ".json", "cache content differs from its digest")
            if entry["worktree_id"] != inventory["worktree_id"]:
                incompatible.append({"entry": str(path), "reason": "foreign_worktree"})
                continue
            if entry["reader_sha256"] != inventory["reader_sha256"] or entry["mapping"].get("reader") != inventory["reader"]:
                incompatible.append({"entry": str(path), "reason": "incompatible_reader"})
                continue
            mapping = entry["mapping"]
            mode = "reused"
            if mapping.get("inventory_digest") != inventory["inventory_digest"]:
                mapping = draft(inventory, prior_mapping=mapping)
                mode = "carried"
            blockers = validate_map(inventory, mapping)
            if blockers:
                partial.append((mapping, blockers))
                continue
            key = digest(mapping)
            candidates[key] = (mapping, mode)
        except (OSError, ValueError, TypeError, KeyError) as error:
            return blocked("cache_entry_invalid", details={"entry": str(path), "detail": str(error)[:500]})
    if len(candidates) > 1:
        return blocked("ambiguous_rule_maps", details={"map_digests": sorted(candidates)},
                       next_step="Choose the intended reviewed map explicitly with --map; no map was selected by timestamp.")
    if candidates:
        mapping, mode = next(iter(candidates.values()))
        path = remember(directory, inventory, mapping)
        return mapping, {"mode": mode, "entry": str(path), "reused_units": total,
                         "unresolved_units": 0, "excluded_incompatible_entries": incompatible}
    if partial:
        # A draft is a request for interpretation, never an executable selection.
        # Several partial interpretations remain ambiguous; do not blend them.
        drafts = {digest(mapping): (mapping, blockers) for mapping, blockers in partial}
        if len(drafts) != 1:
            return blocked("ambiguous_partial_maps", next_step="Choose a prior map explicitly for guided interpretation.")
        mapping, blockers = next(iter(drafts.values()))
        path = write_immutable(directory, "draft-" + digest(mapping) + ".json", mapping)
        unresolved = sum(t["kind"] == "unresolved" for t in mapping["treatments"].values())
        return None, {"mode": "needs_interpretation", "draft": str(path), "blockers": blockers,
                      "reused_units": total - unresolved, "unresolved_units": unresolved,
                      "next_step": "Review the generated draft and pass the completed map explicitly with --map."}
    return blocked("cache_incompatible", details={"entries": incompatible})


def task_result(result, phase, cache, *, details=False):
    """A view of the existing phase verdict, not a second state machine."""
    effective = result.get("phase_result", result)
    binding = effective.get("binding") or (effective if effective.get("schema") == "vostok.task-rule-binding.v1" else {})
    blockers = list(result.get("blockers", []))
    if effective is not result:
        blockers.extend(effective.get("blockers", []))
    if result.get("status") == "blocked_protection_unavailable" and not blockers:
        blockers = [{"reason": reason} for reason in result.get("limits", [])[:1]]
    status = result.get("status", "blocked")
    next_step = cache.get("next_step")
    if not next_step:
        next_step = ("Execute only the declared task paths." if effective.get("status") == "ready_for_execution"
                     else "Review the verified result; human acceptance remains separate." if effective.get("status") == "ready_for_review"
                     else "Resolve the reported blockers; no authorization is inferred.")
    view = {"schema": "vostok.rule-task-result.v1", "status": status, "phase": phase,
            "map_digest": binding.get("map_digest"), "task_digest": binding.get("task_digest"),
            "task_id": binding.get("task_id"), "binding_digest": digest(binding) if binding else None,
            "rule_count": len(binding.get("rules", [])), "check_count": len(effective.get("checks", {})),
            "blockers": blockers, "cache": {k: v for k, v in cache.items() if k not in {"blockers", "next_step"}}, "next_step": next_step,
            "limits": ["summary_of_existing_evaluation", "cache_is_not_authorization", "no_human_acceptance", "no_universal_protection"]}
    if details:
        view["detail"] = result
    return view
