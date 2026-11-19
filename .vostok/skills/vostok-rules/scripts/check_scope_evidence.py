#!/usr/bin/env python3
"""Scope & Verification Supervisor — deterministic local checker (Spec 0003).

Exit 0: no structural scope violation + required evidence fresh/present when asked,
        and the change set was obtained completely for the selected mode.
Exit 1: policy_fail or unknown_incomplete (scope / evidence / essential info missing).
Exit 2: invocation_error or internal_error.

Does NOT claim: semantic business satisfaction, human acceptance (D-H), enforced,
agent obedience, or that the ScopeContract faithfully matches human intent.
Guarantee: comprobable structural facts vs the supplied contract only.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

SCHEMA = "vostok.supervision.v0"
DEFAULT_LIMITS = [
    "not_enforced",
    "not_semantic_satisfaction",
    "not_human_acceptance",
    "not_scope_contract_fidelity",
    "not_agent_obedience",
    "excluded_paths_not_auto_repaired",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def posix_rel(path: str) -> str:
    """Normalize to POSIX relative form without collapsing hidden-file dots.

    Important: do NOT use str.lstrip('./') — that strips any leading '.' or '/'
    characters and would turn '.pricing.js' into 'pricing.js'.
    """
    p = path.replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


# ---------------------------------------------------------------------------
# Contract
# ---------------------------------------------------------------------------

@dataclass
class Criterion:
    id: str
    text: str = ""
    check: str | None = None
    verified_inputs: list[str] = field(default_factory=list)
    unverified_yet: bool = False


@dataclass
class ScopeContract:
    work_id: str
    allowed_paths: list[str]
    excluded_paths: list[str]
    criteria: list[Criterion] = field(default_factory=list)
    governing_revision: str | None = None
    mode: str = "closed"  # closed: paths outside allowed are unexpected
    excluded_none_declared: bool = False

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not isinstance(self.work_id, str) or not self.work_id.strip():
            errors.append("work_id is required")
        if self.mode not in {"closed", "open"}:
            errors.append(f"invalid scope mode: {self.mode!r}; expected closed or open")
        if self.mode == "closed" and not self.allowed_paths:
            errors.append("allowed_paths empty in closed mode is ambiguous (CLARIFY)")
        if not self.excluded_paths and not self.excluded_none_declared:
            errors.append(
                "excluded_paths empty without excluded_none=true "
                "(must declare exclusions or none)"
            )
        # Contradictory allowed ∩ excluded
        for a in self.allowed_paths:
            for e in self.excluded_paths:
                if matches_pattern(a, e) or matches_pattern(e, a):
                    errors.append(f"allowed∩excluded contradiction: {a!r} vs {e!r}")
        for label, patterns in (("allowed_paths", self.allowed_paths), ("excluded_paths", self.excluded_paths)):
            for pattern in patterns:
                error = validate_relative_pattern(pattern)
                if error:
                    errors.append(f"{label} contains invalid path {pattern!r}: {error}")
        for c in self.criteria:
            if not c.id:
                errors.append("criterion missing id")
            if not c.check and not c.unverified_yet:
                errors.append(
                    f"criterion {c.id or '<missing-id>'} requires check or unverified_yet=true"
                )
            if c.check and not c.verified_inputs:
                errors.append(f"criterion {c.id} requires explicit verified_inputs")
            for token in c.verified_inputs:
                if not isinstance(token, str) or not token.strip():
                    errors.append(f"criterion {c.id} has invalid verified_input {token!r}")
                elif not token.startswith(("cmd:", "meta:")):
                    path_part = token.split("#", 1)[0]
                    path_error = validate_relative_pattern(path_part)
                    if path_error:
                        errors.append(
                            f"criterion {c.id} has unsafe verified_input {token!r}: {path_error}"
                        )
            if len(set(c.verified_inputs)) != len(c.verified_inputs):
                errors.append(f"criterion {c.id} has duplicate verified_inputs")
        ids = [c.id for c in self.criteria if c.id]
        duplicates = sorted({criterion_id for criterion_id in ids if ids.count(criterion_id) > 1})
        if duplicates:
            errors.append(f"duplicate criterion ids: {duplicates}")
        return errors


def load_contract(path: Path | None, args: argparse.Namespace) -> ScopeContract:
    data: dict[str, Any] = {}
    if path is not None:
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() in {".yaml", ".yml"}:
            try:
                import yaml  # type: ignore
            except ImportError as exc:
                raise RuntimeError(
                    "PyYAML not installed; use JSON contract or --allowed/--excluded flags"
                ) from exc
            loaded = yaml.safe_load(text)
        else:
            loaded = json.loads(text)
        if not isinstance(loaded, dict):
            raise ValueError("contract root must be an object")
        data = loaded

    if path is not None:
        contract_mode = data.get("mode", "closed")
        if not isinstance(contract_mode, str) or contract_mode not in {"closed", "open"}:
            raise ValueError("contract mode must be exactly 'closed' or 'open'")
        if args.scope_mode and args.scope_mode != contract_mode:
            raise ValueError("--scope-mode cannot override the contract mode")
        if args.allowed and list(args.allowed) != data.get("allowed_paths", []):
            raise ValueError("--allowed cannot override contract allowed_paths")
        if args.excluded and list(args.excluded) != data.get("excluded_paths", []):
            raise ValueError("--excluded cannot override contract excluded_paths")
        if (
            args.governing_revision
            and data.get("governing_revision")
            and args.governing_revision != data["governing_revision"]
        ):
            raise ValueError("--governing-revision cannot override contract governing_revision")

    work_id = args.work_id or data.get("work_id")
    if work_id is not None and not isinstance(work_id, str):
        raise ValueError("work_id must be a string")
    allowed_raw = args.allowed if args.allowed else data.get("allowed_paths", [])
    excluded_raw = args.excluded if args.excluded else data.get("excluded_paths", [])
    if not isinstance(allowed_raw, list) or any(not isinstance(value, str) for value in allowed_raw):
        raise ValueError("allowed_paths must be an array of strings")
    if not isinstance(excluded_raw, list) or any(not isinstance(value, str) for value in excluded_raw):
        raise ValueError("excluded_paths must be an array of strings")
    allowed = list(allowed_raw)
    excluded = list(excluded_raw)
    excluded_none_raw = args.excluded_none or data.get("excluded_none", False)
    if not isinstance(excluded_none_raw, bool):
        raise ValueError("excluded_none must be a boolean")
    excluded_none = excluded_none_raw
    governing = args.governing_revision or data.get("governing_revision")
    if governing is not None and not isinstance(governing, str):
        raise ValueError("governing_revision must be a string")
    mode = args.scope_mode or data.get("mode", "closed")
    if not isinstance(mode, str) or mode not in {"closed", "open"}:
        raise ValueError("mode must be exactly 'closed' or 'open'")

    criteria_raw = data.get("criteria", [])
    if not isinstance(criteria_raw, list):
        raise ValueError("criteria must be an array")
    criteria: list[Criterion] = []
    for item in criteria_raw:
        if isinstance(item, str):
            criteria.append(Criterion(id=item))
        elif isinstance(item, dict):
            criterion_id = item.get("id", item.get("criterion_id", ""))
            criterion_text = item.get("text", "")
            if not isinstance(criterion_id, str) or not isinstance(criterion_text, str):
                raise ValueError("criterion id and text must be strings")
            check = item.get("check")
            unverified_yet = item.get("unverified_yet", False)
            verified_inputs = item.get("verified_inputs", [])
            if check is not None and not isinstance(check, str):
                raise ValueError("criterion check must be a string")
            if not isinstance(unverified_yet, bool):
                raise ValueError("criterion unverified_yet must be a boolean")
            if not isinstance(verified_inputs, list) or any(not isinstance(value, str) for value in verified_inputs):
                raise ValueError("criterion verified_inputs must be an array of strings")
            criteria.append(
                Criterion(
                    id=criterion_id,
                    text=criterion_text,
                    check=check,
                    verified_inputs=list(verified_inputs),
                    unverified_yet=unverified_yet,
                )
            )
        else:
            raise ValueError("each criteria entry must be a string or object")
    if args.criterion_id:
        existing = next((criterion for criterion in criteria if criterion.id == args.criterion_id), None)
        if existing is None:
            if path is not None:
                raise ValueError(f"unknown criterion id in contract: {args.criterion_id}")
            criteria.append(
                Criterion(
                    id=args.criterion_id,
                    text=args.criterion_text or "",
                    check=args.check_command,
                    verified_inputs=list(args.verified_inputs),
                )
            )
        elif args.check_command:
            if existing.check != args.check_command:
                raise ValueError(
                    f"check command override does not match contract for {args.criterion_id}"
                )

    if work_id is None:
        raise ValueError("work_id required (--work-id or contract)")

    return ScopeContract(
        work_id=str(work_id),
        allowed_paths=[posix_rel(p) for p in allowed],
        excluded_paths=[posix_rel(p) for p in excluded],
        criteria=criteria,
        governing_revision=str(governing) if governing else None,
        mode=str(mode),
        excluded_none_declared=excluded_none,
    )


# ---------------------------------------------------------------------------
# Path matching / normalization
# ---------------------------------------------------------------------------

def normalize_under_root(root: Path, raw: str) -> tuple[str | None, str | None]:
    """Return (posix_relative, error). Rejects escapes and absolute outsides."""
    if not raw:
        return None, "empty path"
    candidate = raw.replace("\\", "/")
    if candidate.startswith("/"):
        # Absolute: must resolve under root
        try:
            resolved = Path(candidate).resolve()
            rel = resolved.relative_to(root.resolve())
            return posix_rel(str(rel)), None
        except Exception:
            return None, f"absolute path outside root: {raw}"
    # Disallow .. segments that escape
    parts = []
    for part in Path(candidate).parts:
        if part in ("", "."):
            continue
        if part == "..":
            if not parts:
                return None, f"path escapes root via ..: {raw}"
            parts.pop()
            continue
        parts.append(part)
    rel = "/".join(parts)
    # Symlink escape check if present on disk
    abs_path = root / rel
    if abs_path.is_symlink() or abs_path.exists():
        try:
            resolved = abs_path.resolve()
            resolved.relative_to(root.resolve())
        except Exception:
            return None, f"symlink or path escapes root: {raw}"
    return posix_rel(rel), None


def validate_relative_pattern(pattern: str) -> str | None:
    """Validate a portable relative path/glob without normalizing unsafe input away."""
    if not isinstance(pattern, str) or not pattern or pattern.strip() != pattern:
        return "must be a non-empty trimmed string"
    normalized = pattern.replace("\\", "/")
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        return "absolute paths are not allowed"
    parts = normalized.rstrip("/").split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return "empty, '.' and '..' path segments are not allowed"
    if any("**" in part and part != "**" for part in parts):
        return "'**' must be a complete path segment"
    for part in parts:
        if part.count("[") != part.count("]"):
            return "unbalanced glob character class"
    return None


def matches_pattern(path: str, pattern: str) -> bool:
    """Match slash-delimited globs; '*' and '?' never cross a path separator."""
    path = path.replace("\\", "/")
    pattern = pattern.replace("\\", "/")
    if not any(char in pattern for char in "*?["):
        if pattern.endswith("/"):
            return path.startswith(pattern)
        return path == pattern

    path_parts = path.split("/")
    pattern_parts = pattern.rstrip("/").split("/")

    def match_from(path_index: int, pattern_index: int) -> bool:
        if pattern_index == len(pattern_parts):
            return path_index == len(path_parts)
        token = pattern_parts[pattern_index]
        if token == "**":
            if pattern_index == len(pattern_parts) - 1:
                return True
            return any(
                match_from(next_path, pattern_index + 1)
                for next_path in range(path_index, len(path_parts) + 1)
            )
        if path_index >= len(path_parts) or not fnmatch.fnmatchcase(path_parts[path_index], token):
            return False
        return match_from(path_index + 1, pattern_index + 1)

    return match_from(0, 0)


def matches_any(path: str, patterns: Sequence[str]) -> bool:
    for pat in patterns:
        if matches_pattern(path, pat):
            return True
    return False


def patterns_resolvable(root: Path, patterns: Sequence[str]) -> list[str]:
    """Flag unsafe paths and wildcard patterns with no current filesystem match."""
    errors: list[str] = []
    for pattern in patterns:
        error = validate_relative_pattern(pattern)
        if error:
            errors.append(f"{pattern!r}: {error}")
            continue
        if any(char in pattern for char in "*?["):
            try:
                match = next(root.glob(pattern), None)
            except (OSError, ValueError) as exc:
                errors.append(f"{pattern!r}: glob cannot be resolved ({exc})")
                continue
            if match is None:
                errors.append(f"{pattern!r}: glob matches no existing path")
    return errors


# ---------------------------------------------------------------------------
# Change set collectors
# ---------------------------------------------------------------------------

@dataclass
class ChangeSetResult:
    paths: set[str] = field(default_factory=set)
    complete: bool = True
    errors: list[str] = field(default_factory=list)
    escapes: list[str] = field(default_factory=list)
    mode: str = ""
    notes: list[str] = field(default_factory=list)


def run_git(root: Path, args: Sequence[str]) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def collect_git(root: Path, baseline_ref: str | None) -> ChangeSetResult:
    result = ChangeSetResult(mode="git")
    # Ensure we're in a git work tree (root may be a subdir)
    code, out, err = run_git(root, ["rev-parse", "--is-inside-work-tree"])
    if code != 0 or out.strip() != "true":
        result.complete = False
        result.errors.append("not a git work tree; cannot use --diff-from=git")
        return result

    ref = baseline_ref or "HEAD"
    # Verify baseline exists
    code, _, err = run_git(root, ["rev-parse", "--verify", ref])
    if code != 0:
        result.complete = False
        result.errors.append(f"git baseline unavailable: {ref} ({err.strip() or 'missing'})")
        return result

    # Unified name-status: committed baseline..worktree including unstaged
    # Use status porcelain for staged+unstaged+untracked+renames+deletes
    code, porcelain, err = run_git(root, ["status", "--porcelain=v1", "-z", "-uall", "--", "."])
    if code != 0:
        result.complete = False
        result.errors.append(f"git status failed: {err.strip()}")
        return result

    # Also include committed diffs vs ref if working tree clean but commits ahead?
    # Spec: working tree complete vs HEAD (or named). Porcelain covers WT.
    # Additionally: diff --name-status ref for any divergence if ref != HEAD content
    # For fixture isolation we primarily care about WT vs baseline.

    def add_raw(raw: str) -> None:
        rel, err_msg = normalize_under_root(root, raw)
        if err_msg:
            if "escape" in err_msg or "outside" in err_msg:
                result.escapes.append(raw)
            result.errors.append(err_msg)
            result.complete = False
            return
        if rel:
            result.paths.add(rel)

    status_records = [record for record in porcelain.split("\0") if record]
    index = 0
    while index < len(status_records):
        record = status_records[index]
        index += 1
        status = record[:2]
        path = record[3:] if len(record) > 3 else ""
        if ("R" in status or "C" in status) and index < len(status_records):
            # With -z, Git emits destination in the status record and source
            # as the next NUL-delimited field (without quoted-path parsing).
            add_raw(path)
            add_raw(status_records[index])
            index += 1
        elif status.strip() and path:
            add_raw(path)

    # Ignore rules hide untracked files from normal porcelain output. We cannot
    # distinguish a pre-existing ignored file from one changed by this work,
    # so any such path makes the Git change set incomplete instead of green.
    code, ignored_out, err = run_git(
        root,
        ["ls-files", "--others", "--ignored", "--exclude-standard", "-z", "--", "."],
    )
    if code != 0:
        result.complete = False
        result.errors.append(f"git ignored-path scan failed: {err.strip()}")
    else:
        ignored_paths = [path for path in ignored_out.split("\0") if path]
        if ignored_paths:
            result.complete = False
            result.errors.append(
                "ignored untracked paths prevent complete Git scope verification: "
                + ", ".join(ignored_paths[:20])
            )
            for path in ignored_paths:
                add_raw(path)

    # If ref is not HEAD tip content, include diff names from ref to HEAD+WT via
    # `git diff --name-status ref` (covers unstaged vs ref and staged)
    code, diff_out, err = run_git(root, ["diff", "--name-status", "-z", "--find-renames", ref])
    if code != 0:
        result.complete = False
        result.errors.append(f"git diff failed: {err.strip()}")
        return result
    diff_records = [record for record in diff_out.split("\0") if record]
    index = 0
    while index < len(diff_records):
        code_letter = diff_records[index]
        index += 1
        if code_letter.startswith(("R", "C")) and index + 1 < len(diff_records):
            add_raw(diff_records[index])
            add_raw(diff_records[index + 1])
            index += 2
        elif index < len(diff_records):
            add_raw(diff_records[index])
            index += 1

    # Staged separately to guarantee staged+unstaged unification (diff above is unstaged;
    # porcelain already has staged; also pull staged diff)
    code, staged, err = run_git(root, ["diff", "--cached", "--name-status", "-z", "--find-renames", ref])
    if code != 0:
        result.complete = False
        result.errors.append(f"git diff --cached failed: {err.strip()}")
        return result
    staged_records = [record for record in staged.split("\0") if record]
    index = 0
    while index < len(staged_records):
        code_letter = staged_records[index]
        index += 1
        if code_letter.startswith(("R", "C")) and index + 1 < len(staged_records):
            add_raw(staged_records[index])
            add_raw(staged_records[index + 1])
            index += 2
        elif index < len(staged_records):
            add_raw(staged_records[index])
            index += 1

    result.notes.append(f"git change set vs {ref}; sources=porcelain+diff+cached")
    return result


def collect_baseline_tree(root: Path, pairs: Sequence[str]) -> ChangeSetResult:
    """Compare declared pairs for diagnostics, never claim whole-tree coverage."""
    result = ChangeSetResult(
        mode="baseline-tree",
        complete=False,
        errors=[
            "baseline-tree compares declared pairs only and cannot prove complete workspace coverage; "
            "use git mode or a manifest cross-checked against Git"
        ],
    )
    if not pairs:
        result.errors.append("baseline-tree requires --baseline-pair current:baseline")
        return result
    for pair in pairs:
        if ":" not in pair:
            result.errors.append(f"invalid baseline pair: {pair}")
            continue
        current_rel, baseline_rel = pair.split(":", 1)
        cur_n, err1 = normalize_under_root(root, current_rel)
        base_n, err2 = normalize_under_root(root, baseline_rel)
        if err1 or err2:
            result.complete = False
            result.errors.append(err1 or err2 or "normalize error")
            if err1 and "escape" in err1:
                result.escapes.append(current_rel)
            if err2 and "escape" in err2:
                result.escapes.append(baseline_rel)
            continue
        assert cur_n and base_n
        cur_path = root / cur_n
        base_path = root / base_n
        if not base_path.is_file():
            result.complete = False
            result.errors.append(f"baseline missing: {base_n}")
            continue
        if not cur_path.is_file():
            # Treat missing current as change (deleted)
            result.paths.add(cur_n)
            continue
        cur_bytes = cur_path.read_bytes()
        base_bytes = base_path.read_bytes()
        if cur_bytes != base_bytes:
            result.paths.add(cur_n)
    return result


def collect_manifest(
    root: Path, paths: Sequence[str], coverage_complete: bool
) -> ChangeSetResult:
    result = ChangeSetResult(mode="manifest")
    if not coverage_complete:
        result.complete = False
        result.errors.append(
            "manifest mode without --manifest-complete declaration → UNKNOWN "
            "(list alone does not prove full coverage)"
        )
        # Still record declared paths for transparency
    for raw in paths:
        rel, err_msg = normalize_under_root(root, raw)
        if err_msg:
            result.complete = False
            result.errors.append(err_msg)
            if "escape" in err_msg or "outside" in err_msg:
                result.escapes.append(raw)
            continue
        if rel:
            result.paths.add(rel)
    return result


def collect_changes(root: Path, args: argparse.Namespace) -> ChangeSetResult:
    if args.diff_from == "git":
        return collect_git(root, args.git_baseline)
    if args.diff_from == "baseline-tree":
        return collect_baseline_tree(root, args.baseline_pair)
    changes = collect_manifest(root, args.manifest_path, args.manifest_complete)
    if args.manifest_complete:
        # A caller's completeness flag is an assertion, not coverage evidence.
        # Cross-check it against Git before allowing a green result.
        git_changes = collect_git(root, args.git_baseline)
        if not git_changes.complete:
            changes.complete = False
            changes.errors.extend(["manifest cannot be independently checked"] + git_changes.errors)
        elif changes.paths != git_changes.paths:
            changes.complete = False
            changes.errors.append(
                "manifest does not match Git change set: "
                f"missing={sorted(git_changes.paths - changes.paths)}, "
                f"extra={sorted(changes.paths - git_changes.paths)}"
            )
        else:
            changes.notes.append("manifest path set cross-checked against Git")
    return changes


# ---------------------------------------------------------------------------
# Scope evaluation
# ---------------------------------------------------------------------------

@dataclass
class ScopeEval:
    ok: bool
    violations: list[str] = field(default_factory=list)
    unexpected: list[str] = field(default_factory=list)
    changed_paths: list[str] = field(default_factory=list)
    signal_class: str = "UNKNOWN"
    limits: str = (
        "VERIFIED = diff∩excluded (or closed-mode membership) vs supplied "
        "ScopeContract only; not intent fidelity"
    )


def evaluate_scope(contract: ScopeContract, changes: ChangeSetResult) -> ScopeEval:
    changed = sorted(changes.paths)
    if not changes.complete:
        return ScopeEval(
            ok=False,
            changed_paths=changed,
            signal_class="UNKNOWN",
        )
    if changes.escapes:
        return ScopeEval(
            ok=False,
            violations=list(changes.escapes),
            changed_paths=changed,
            signal_class="VERIFIED",
        )

    violations = [p for p in changed if matches_any(p, contract.excluded_paths)]
    unexpected: list[str] = []
    if contract.mode == "closed":
        unexpected = [
            p
            for p in changed
            if not matches_any(p, contract.allowed_paths)
            and p not in violations
        ]
    ok = not violations and not unexpected
    return ScopeEval(
        ok=ok,
        violations=violations,
        unexpected=unexpected,
        changed_paths=changed,
        signal_class="VERIFIED",
    )


# ---------------------------------------------------------------------------
# Evidence freshness
# ---------------------------------------------------------------------------

@dataclass
class EvidenceEval:
    criterion_id: str | None
    check: str | None
    result: str  # pass / fail / unknown
    sufficiency: str
    verified_inputs: list[str]
    content_revision: str | None
    expected_revision: str | None
    signal_class: str
    exit_code: int | None = None
    d_ac_hint: str | None = None
    limits: list[str] = field(default_factory=list)


def materialize_verified_inputs(
    root: Path, inputs: Sequence[str], command: str | None
) -> tuple[list[str], list[str]]:
    """Return (canonical tokens, errors). Tokens are path:<rel> or cmd:<cmd> or meta:."""
    tokens: list[str] = []
    errors: list[str] = []
    for raw in inputs:
        raw = raw.strip()
        if not raw:
            continue
        if raw.startswith("cmd:"):
            tokens.append(raw)
            continue
        if raw.startswith("meta:"):
            tokens.append(raw)
            continue
        # package.json#scripts.test style → hash whole file + meta marker
        if "#" in raw and not raw.startswith("#"):
            path_part, frag = raw.split("#", 1)
            rel, err = normalize_under_root(root, path_part)
            if err or not rel:
                errors.append(err or f"bad input {raw}")
                continue
            tokens.append(f"path:{rel}")
            tokens.append(f"meta:{rel}#{frag}")
            continue
        rel, err = normalize_under_root(root, raw)
        if err or not rel:
            errors.append(err or f"bad input {raw}")
            continue
        tokens.append(f"path:{rel}")
    if command:
        tokens.append(f"cmd:{command}")
    # Stable unique order
    tokens = sorted(set(tokens))
    return tokens, errors


def digest_verified_inputs(root: Path, tokens: Sequence[str]) -> tuple[str | None, list[str]]:
    errors: list[str] = []
    chunks: list[bytes] = []
    for tok in tokens:
        chunks.append(tok.encode("utf-8"))
        chunks.append(b"\0")
        if tok.startswith("path:"):
            rel = tok[len("path:") :]
            path = root / rel
            if not path.is_file():
                errors.append(f"verified input missing: {rel}")
                chunks.append(b"MISSING")
            else:
                # Symlink escape already checked at normalize time for listed paths;
                # re-check resolve
                try:
                    path.resolve().relative_to(root.resolve())
                except Exception:
                    errors.append(f"verified input escapes root: {rel}")
                    return None, errors
                chunks.append(path.read_bytes())
        elif tok.startswith("cmd:") or tok.startswith("meta:"):
            chunks.append(tok.encode("utf-8"))
        chunks.append(b"\n")
    if errors and any("escapes" in e for e in errors):
        return None, errors
    return sha256_bytes(b"".join(chunks)), errors


def execute_check(root: Path, command: str, timeout_seconds: int) -> tuple[int | None, dict[str, Any], str | None]:
    """Execute a declared argv without a shell and return bounded provenance."""
    try:
        argv = shlex.split(command)
    except ValueError as exc:
        return None, {}, f"invalid check command: {exc}"
    if not argv:
        return None, {}, "check command is empty"

    def output_info(handle: Any) -> dict[str, Any]:
        handle.flush()
        size = handle.seek(0, os.SEEK_END)
        digest = hashlib.sha256()
        handle.seek(0)
        while True:
            chunk = handle.read(65536)
            if not chunk:
                break
            digest.update(chunk)
        handle.seek(max(0, size - 4096))
        excerpt = handle.read(4096).decode("utf-8", errors="replace")
        return {"sha256": digest.hexdigest(), "excerpt": excerpt, "truncated": size > 4096}

    try:
        with tempfile.TemporaryFile() as stdout_file, tempfile.TemporaryFile() as stderr_file:
            try:
                proc = subprocess.run(
                    argv,
                    cwd=str(root),
                    stdout=stdout_file,
                    stderr=stderr_file,
                    timeout=timeout_seconds,
                    check=False,
                    shell=False,
                )
            except subprocess.TimeoutExpired:
                stdout_info = output_info(stdout_file)
                stderr_info = output_info(stderr_file)
                return None, {
                    "command": command,
                    "completed": False,
                    "timed_out": True,
                    "timeout_seconds": timeout_seconds,
                    "stdout_sha256": stdout_info["sha256"],
                    "stderr_sha256": stderr_info["sha256"],
                    "stdout_excerpt": stdout_info["excerpt"],
                    "stderr_excerpt": stderr_info["excerpt"],
                    "output_truncated": stdout_info["truncated"] or stderr_info["truncated"],
                }, "check command timed out"
            stdout_info = output_info(stdout_file)
            stderr_info = output_info(stderr_file)
    except OSError as exc:
        return None, {}, f"check command could not start: {exc}"
    return proc.returncode, {
        "command": command,
        "completed": True,
        "timed_out": False,
        "stdout_sha256": stdout_info["sha256"],
        "stderr_sha256": stderr_info["sha256"],
        "stdout_excerpt": stdout_info["excerpt"],
        "stderr_excerpt": stderr_info["excerpt"],
        "output_truncated": stdout_info["truncated"] or stderr_info["truncated"],
    }, None


def evaluate_evidence(
    root: Path,
    *,
    criterion_id: str | None,
    check_command: str | None,
    verified_inputs: Sequence[str],
    evidence_revision: str | None,
    require_evidence: bool,
    check_exit_code: int | None,
    check_executed: bool,
    declared_only: bool,
) -> EvidenceEval:
    limits = [
        "content_revision binds declared verified_inputs only",
        "hash match ≠ environment reproducibility",
        "hash match alone ≠ command was executed",
    ]
    tokens, mat_errors = materialize_verified_inputs(root, verified_inputs, check_command)

    if declared_only:
        return EvidenceEval(
            criterion_id=criterion_id,
            check=check_command,
            result="unknown",
            sufficiency="insufficient",
            verified_inputs=tokens,
            content_revision=None,
            expected_revision=evidence_revision,
            signal_class="DECLARED",
            d_ac_hint="CLARIFY",
            limits=limits + ["narrative_only_not_verified"],
        )

    # No execution / revision signal at all while evidence is required.
    if require_evidence and not check_executed and check_exit_code is None and not evidence_revision:
        return EvidenceEval(
            criterion_id=criterion_id,
            check=check_command,
            result="unknown",
            sufficiency="absent",
            verified_inputs=tokens,
            content_revision=None,
            expected_revision=None,
            signal_class="OBSERVED",
            d_ac_hint="REVERIFY",
            limits=limits,
        )

    if not tokens and require_evidence:
        return EvidenceEval(
            criterion_id=criterion_id,
            check=check_command,
            result="unknown",
            sufficiency="insufficient",
            verified_inputs=[],
            content_revision=None,
            expected_revision=evidence_revision,
            signal_class="UNKNOWN",
            d_ac_hint="CLARIFY",
            limits=limits + ["verified_inputs_empty"],
        )

    digest, dig_errors = digest_verified_inputs(root, tokens)
    all_errors = mat_errors + dig_errors

    # This function receives check_executed only from the in-process runner.
    # The CLI rejects caller-supplied execution flags before reaching here.
    if check_exit_code is not None and not check_executed:
        return EvidenceEval(
            criterion_id=criterion_id,
            check=check_command,
            result="unknown",
            sufficiency="insufficient",
            verified_inputs=tokens,
            content_revision=digest,
            expected_revision=evidence_revision,
            signal_class="OBSERVED",
            exit_code=check_exit_code,
            d_ac_hint="REVERIFY",
            limits=limits
            + [
                "exit_code_unbound_without_check_executed",
                "pass_requires_content_revision_binding",
            ],
        )

    if check_exit_code is not None:
        if check_exit_code == 0:
            result = "pass"
        else:
            result = "fail"
        signal = "OBSERVED"
    elif check_executed:
        result = "unknown"
        signal = "OBSERVED"
    else:
        result = "unknown"
        signal = "UNKNOWN"

    sufficiency = "sufficient"
    d_ac = "CONTINUE"

    if require_evidence and result == "unknown":
        sufficiency = "insufficient"
        d_ac = "REVERIFY"

    if result == "fail":
        # Failure is useful for REPAIR even before a digest bind, but still
        # record current digest when inputs exist.
        sufficiency = "sufficient"
        d_ac = "REPAIR"
        signal = "OBSERVED"

    # PASS claims must be bound to content_revision of verified_inputs.
    if result == "pass":
        if digest is None:
            sufficiency = "not_observable"
            d_ac = "CLARIFY"
            signal = "UNKNOWN"
            result = "unknown"
            limits = limits + ["pass_without_digest"]
        elif evidence_revision is None:
            sufficiency = "insufficient"
            d_ac = "REVERIFY"
            signal = "OBSERVED"
            result = "unknown"
            limits = limits + [
                "pass_requires_evidence_revision",
                "pass_requires_content_revision_binding",
            ]
        elif evidence_revision != digest:
            sufficiency = "obsolete"
            d_ac = "REVERIFY"
            signal = "VERIFIED"
            result = "unknown"
        else:
            signal = "VERIFIED"
            sufficiency = "sufficient"
            d_ac = "CONTINUE"

    elif evidence_revision is not None and digest is not None:
        if evidence_revision != digest:
            sufficiency = "obsolete"
            d_ac = "REVERIFY"
            signal = "VERIFIED"
            if result != "fail":
                result = "unknown"
        elif result != "fail" and not check_executed and check_exit_code is None:
            sufficiency = "insufficient"
            d_ac = "REVERIFY"
            signal = "OBSERVED"
            limits = limits + ["revision_matches_but_no_execution_observed"]

    if evidence_revision is not None and digest is None:
        sufficiency = "not_observable"
        d_ac = "CLARIFY"
        signal = "UNKNOWN"

    if all_errors and sufficiency == "sufficient":
        sufficiency = "insufficient"
        d_ac = "CLARIFY"
        signal = "UNKNOWN"

    if require_evidence and sufficiency == "absent":
        d_ac = "REVERIFY"

    return EvidenceEval(
        criterion_id=criterion_id,
        check=check_command,
        result=result,
        sufficiency=sufficiency,
        verified_inputs=tokens,
        content_revision=digest,
        expected_revision=evidence_revision,
        signal_class=signal,
        exit_code=check_exit_code,
        d_ac_hint=d_ac,
        limits=limits + ([f"input_error:{e}" for e in all_errors] if all_errors else []),
    )


# ---------------------------------------------------------------------------
# Verdict assembly
# ---------------------------------------------------------------------------

@dataclass
class Verdict:
    work_id: str
    outcome_class: str
    gate_hint: str
    signals: list[dict[str, Any]]
    evidence: list[dict[str, Any]]
    limits: list[str]
    recovery: dict[str, Any] | None = None
    scope: dict[str, Any] | None = None
    content_revision: str | None = None
    governing_revision: str | None = None
    sufficiency: str | None = None
    transition_recommendation: str | None = None
    schema: str = SCHEMA

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "work_id": self.work_id,
            "schema": self.schema,
            "outcome_class": self.outcome_class,
            "signals": self.signals,
            "evidence": self.evidence,
            "gate_hint": self.gate_hint,
            "limits": self.limits,
        }
        if self.scope is not None:
            d["scope"] = self.scope
        if self.content_revision is not None:
            d["content_revision"] = self.content_revision
        if self.governing_revision is not None:
            d["governing_revision"] = self.governing_revision
        if self.sufficiency is not None:
            d["sufficiency"] = self.sufficiency
        if self.transition_recommendation is not None:
            d["transition_recommendation"] = self.transition_recommendation
        if self.recovery is not None:
            d["recovery"] = self.recovery
        return d


def choose_gate(
    *,
    scope: ScopeEval,
    changes: ChangeSetResult,
    evidence: EvidenceEval | Sequence[EvidenceEval] | None,
    contract_errors: list[str],
    repair_attempts: int,
    max_repair: int,
) -> tuple[str, str, int]:
    """Return (outcome_class, gate_hint, exit_code)."""
    if contract_errors:
        return "invocation_error", "CLARIFY", 2
    if changes.escapes:
        return "policy_fail", "STOP", 1
    if not changes.complete:
        return "unknown_incomplete", "CLARIFY", 1
    if scope.violations:
        return "policy_fail", "STOP", 1
    if scope.unexpected:
        return "policy_fail", "CLARIFY", 1

    evidence_items = (
        list(evidence)
        if isinstance(evidence, (list, tuple))
        else ([evidence] if evidence is not None else [])
    )
    for item in evidence_items:
        if item.sufficiency == "absent":
            return "policy_fail", "REVERIFY", 1
        if item.sufficiency == "obsolete":
            return "policy_fail", "REVERIFY", 1
        if item.sufficiency in {"insufficient", "contradictory", "not_observable", "non_reproducible"}:
            return "policy_fail", item.d_ac_hint or "CLARIFY", 1
        if item.result == "fail":
            if repair_attempts >= max_repair:
                return "policy_fail", "STOP", 1
            return "policy_fail", "REPAIR", 1
        if item.signal_class == "DECLARED":
            return "policy_fail", "CLARIFY", 1

    # Structural OK
    if not evidence_items or all(
        item.result == "pass" and item.sufficiency == "sufficient"
        for item in evidence_items
    ):
        return "ok", "READY_FOR_REVIEW", 0
    return "ok", "CONTINUE", 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Vostok Scope & Verification Supervisor (Spec 0003)",
    )
    p.add_argument("--root", required=True, help="Work root directory")
    p.add_argument("--contract", help="Path to ScopeContract JSON (or YAML if PyYAML available)")
    p.add_argument("--work-id", help="Override / set work_id")
    p.add_argument("--allowed", action="append", default=[], help="Allowed path/glob (repeatable)")
    p.add_argument("--excluded", action="append", default=[], help="Excluded path/glob (repeatable)")
    p.add_argument(
        "--excluded-none",
        action="store_true",
        help="Declare that excluded_paths is intentionally empty",
    )
    p.add_argument("--governing-revision", help="Governing intent/eco revision id or digest")
    p.add_argument("--scope-mode", choices=["closed", "open"], default=None)
    p.add_argument(
        "--diff-from",
        choices=["git", "baseline-tree", "manifest"],
        default="git",
    )
    p.add_argument(
        "--git-baseline",
        default=None,
        help="Git ref for diff baseline (default HEAD)",
    )
    p.add_argument(
        "--baseline-pair",
        action="append",
        default=[],
        help="baseline-tree pair current:baseline (repeatable)",
    )
    p.add_argument(
        "--manifest-path",
        action="append",
        default=[],
        help="Path claimed touched (manifest mode)",
    )
    p.add_argument(
        "--manifest-complete",
        action="store_true",
        help="Caller declares manifest lists the complete change set",
    )
    p.add_argument(
        "--verified-input",
        action="append",
        default=[],
        dest="verified_inputs",
        help="Member of verified_inputs set (path, path#frag, cmd:..., meta:...)",
    )
    p.add_argument("--check-command", help="Canonical check command string")
    p.add_argument("--criterion-id", help="Criterion id for evidence binding")
    p.add_argument("--criterion-text", help="Optional criterion text")
    p.add_argument(
        "--criterion-evidence",
        action="append",
        default=[],
        metavar="JSON",
        help=(
            "Evidence binding for one criterion (repeatable JSON object with "
            "criterion_id, contract-matching verified_inputs, and optional evidence_revision)"
        ),
    )
    p.add_argument(
        "--evidence-revision",
        help="Previously recorded content_revision digest to compare",
    )
    p.add_argument(
        "--require-evidence",
        action="store_true",
        help="Fail if check evidence is absent",
    )
    p.add_argument(
        "--check-exit-code",
        type=int,
        default=None,
        help="Deprecated caller claim; rejected as evidence (use --execute-check)",
    )
    p.add_argument(
        "--check-executed",
        action="store_true",
        help="Deprecated declaration; cannot establish execution (use --execute-check)",
    )
    p.add_argument(
        "--execute-check",
        action="store_true",
        help="Execute each required criterion check directly using argv without a shell",
    )
    p.add_argument(
        "--check-timeout-seconds",
        type=int,
        default=300,
        help="Timeout for --execute-check (default 300 seconds)",
    )
    p.add_argument(
        "--declared-only",
        action="store_true",
        help="Agent narrative without technical check (stays DECLARED)",
    )
    p.add_argument(
        "--repair-attempts",
        type=int,
        default=0,
        help="Prior repair attempts for this failure class",
    )
    p.add_argument(
        "--max-repair",
        type=int,
        default=2,
        help="Maximum repair attempts before STOP (default 2)",
    )
    p.add_argument(
        "--print-digest",
        action="store_true",
        help="Compute and print content_revision for verified_inputs, then exit 0",
    )
    p.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
    )
    return p


def parse_criterion_evidence(raw_items: Sequence[str], contract: ScopeContract) -> dict[str, dict[str, Any]]:
    """Parse repeatable per-criterion evidence bindings and reject ambiguous input."""
    declared = {criterion.id: criterion for criterion in contract.criteria}
    parsed: dict[str, dict[str, Any]] = {}
    for raw in raw_items:
        try:
            item = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid --criterion-evidence JSON: {exc}") from exc
        if not isinstance(item, dict):
            raise ValueError("--criterion-evidence must be a JSON object")
        criterion_id = item.get("criterion_id")
        if not isinstance(criterion_id, str) or not criterion_id:
            raise ValueError("--criterion-evidence requires criterion_id")
        if criterion_id not in declared:
            raise ValueError(f"evidence references unknown criterion: {criterion_id}")
        criterion = declared[criterion_id]
        if not criterion.check or criterion.unverified_yet:
            raise ValueError(f"criterion does not require a check: {criterion_id}")
        if criterion_id in parsed:
            raise ValueError(f"duplicate evidence for criterion: {criterion_id}")

        command = item.get("check_command", criterion.check)
        if command != criterion.check:
            raise ValueError(
                f"check command does not match contract for {criterion_id}: {command!r}"
            )
        inputs = item.get("verified_inputs", [])
        if not isinstance(inputs, list) or any(not isinstance(value, str) for value in inputs):
            raise ValueError(f"verified_inputs must be a string array for {criterion_id}")
        if set(inputs) != set(criterion.verified_inputs):
            raise ValueError(
                f"verified_inputs do not match contract for {criterion_id}: "
                f"expected={criterion.verified_inputs!r}"
            )
        revision = item.get("evidence_revision")
        if revision is not None and not isinstance(revision, str):
            raise ValueError(f"evidence_revision must be a string for {criterion_id}")
        if "check_exit_code" in item or "check_executed" in item:
            raise ValueError(
                f"caller-supplied execution flags are not accepted for {criterion_id}; "
                "use --execute-check"
            )

        parsed[criterion_id] = {
            "check_command": command,
            "verified_inputs": inputs,
            "evidence_revision": revision,
        }
    return parsed


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        root = Path(args.root).resolve()
        if not root.exists() or not root.is_dir():
            verdict = Verdict(
                work_id=args.work_id or "unknown",
                outcome_class="invocation_error",
                gate_hint="STOP",
                signals=[],
                evidence=[],
                limits=DEFAULT_LIMITS,
            )
            emit(verdict, args.format)
            eprint(f"root does not exist or is not a directory: {root}")
            return 2

        # Digest-only mode (helper for experiments)
        if args.print_digest:
            tokens, errs = materialize_verified_inputs(
                root, args.verified_inputs, args.check_command
            )
            digest, derrs = digest_verified_inputs(root, tokens)
            out = {
                "verified_inputs": tokens,
                "content_revision": digest,
                "errors": errs + derrs,
            }
            print(json.dumps(out, indent=2, sort_keys=True))
            return 0 if digest and not (errs + derrs) else 1

        contract_path = Path(args.contract).resolve() if args.contract else None
        if contract_path and not contract_path.is_file():
            emit(
                Verdict(
                    work_id=args.work_id or "unknown",
                    outcome_class="invocation_error",
                    gate_hint="STOP",
                    signals=[],
                    evidence=[],
                    limits=DEFAULT_LIMITS,
                ),
                args.format,
            )
            eprint(f"contract not found: {contract_path}")
            return 2

        try:
            contract = load_contract(contract_path, args)
        except Exception as exc:
            emit(
                Verdict(
                    work_id=args.work_id or "unknown",
                    outcome_class="invocation_error",
                    gate_hint="CLARIFY",
                    signals=[],
                    evidence=[],
                    limits=DEFAULT_LIMITS,
                ),
                args.format,
            )
            eprint(f"invocation_error: {exc}")
            return 2

        contract_errors = contract.validate()
        ambig = patterns_resolvable(root, contract.allowed_paths + contract.excluded_paths)
        if ambig:
            contract_errors.append(f"ambiguous globs/paths: {ambig}")
        try:
            criterion_bindings = parse_criterion_evidence(args.criterion_evidence, contract)
        except ValueError as exc:
            criterion_bindings = {}
            contract_errors.append(str(exc))
        if args.criterion_evidence and (
            args.verified_inputs
            or args.check_command
            or args.evidence_revision
            or args.check_exit_code is not None
            or args.check_executed
            or args.require_evidence
            or args.declared_only
        ):
            contract_errors.append(
                "use --criterion-evidence or legacy single-check flags, not both"
            )
        if args.check_exit_code is not None or args.check_executed:
            contract_errors.append(
                "caller-supplied check exit/execution flags are not evidence; use --execute-check"
            )
        if args.check_timeout_seconds < 1 or args.check_timeout_seconds > 3600:
            contract_errors.append("check timeout must be between 1 and 3600 seconds")
        if args.execute_check and args.declared_only:
            contract_errors.append("--execute-check cannot be combined with --declared-only")
        if args.execute_check and not any(
            criterion.check and not criterion.unverified_yet for criterion in contract.criteria
        ):
            contract_errors.append("--execute-check requires at least one criterion check in the contract")
        required_contract_checks = any(
            criterion.check and not criterion.unverified_yet for criterion in contract.criteria
        )
        if not required_contract_checks and (
            args.execute_check
            or args.check_command
            or args.check_exit_code is not None
            or args.check_executed
            or args.evidence_revision
            or args.verified_inputs
            or args.require_evidence
        ):
            contract_errors.append("evidence flags require a checked criterion in the contract")

        # Collect changes before evaluating evidence.
        changes = collect_changes(root, args)

        scope = evaluate_scope(contract, changes) if not contract_errors else ScopeEval(
            ok=False, signal_class="UNKNOWN"
        )

        evidence_items: list[EvidenceEval] = []
        execution_signals: list[dict[str, Any]] = []
        # Criteria that declare a check (and are not unverified_yet) imply
        # evidence is required — otherwise VERIFY can go green with no check.
        required_criteria = [
            criterion
            for criterion in contract.criteria
            if criterion.check and not criterion.unverified_yet
        ]
        legacy_evidence_requested = (
            args.require_evidence
            or args.declared_only
            or args.evidence_revision is not None
            or args.execute_check
            or bool(args.verified_inputs)
        )
        if not contract_errors and required_criteria:
            for index, criterion in enumerate(required_criteria):
                binding = criterion_bindings.get(criterion.id)
                use_legacy = (
                    not args.criterion_evidence
                    and legacy_evidence_requested
                    and (
                        len(required_criteria) == 1
                        or args.criterion_id == criterion.id
                        or (args.criterion_id is None and index == 0)
                    )
                )
                if args.verified_inputs and set(args.verified_inputs) != set(criterion.verified_inputs):
                    contract_errors.append(
                        f"verified_inputs do not match contract for {criterion.id}"
                    )
                    continue
                if args.check_command and args.check_command != criterion.check:
                    contract_errors.append(
                        f"check command override does not match contract for {criterion.id}"
                    )
                    continue
                declared_inputs = criterion.verified_inputs
                command = criterion.check
                evidence_revision = (
                    binding["evidence_revision"] if binding is not None
                    else (args.evidence_revision if use_legacy else None)
                )
                observed_exit_code: int | None = None
                check_was_executed = False
                if args.execute_check:
                    tokens, token_errors = materialize_verified_inputs(
                        root, declared_inputs, command
                    )
                    before_revision, before_errors = digest_verified_inputs(root, tokens)
                    if token_errors or before_errors or before_revision is None:
                        execution_signals.append({
                            "name": "check_execution",
                            "criterion_id": criterion.id,
                            "class": "UNKNOWN",
                            "errors": token_errors + before_errors,
                        })
                    else:
                        observed_exit_code, execution_info, execution_error = execute_check(
                            root, command or "", args.check_timeout_seconds
                        )
                        after_revision, after_errors = digest_verified_inputs(root, tokens)
                        execution_info["criterion_id"] = criterion.id
                        execution_info["class"] = "OBSERVED" if observed_exit_code is not None else "UNKNOWN"
                        if execution_error:
                            execution_info["error"] = execution_error
                        if after_errors:
                            execution_info["errors"] = after_errors
                        execution_signals.append({"name": "check_execution", **execution_info})
                        check_was_executed = observed_exit_code is not None
                        # Bind this run to the exact pre-run content. A check
                        # that mutates its inputs will therefore become stale.
                        evidence_revision = before_revision
                        if after_revision != before_revision:
                            execution_signals[-1]["input_content_changed_during_check"] = True
                elif binding is not None and binding["evidence_revision"] is None:
                    evidence_revision = None

                evidence_items.append(
                    evaluate_evidence(
                        root,
                        criterion_id=criterion.id,
                        check_command=command,
                        verified_inputs=declared_inputs,
                        evidence_revision=evidence_revision,
                        require_evidence=True,
                        check_exit_code=observed_exit_code,
                        check_executed=check_was_executed,
                        declared_only=args.declared_only,
                    )
                )
        elif not contract_errors and legacy_evidence_requested:
            evidence_items.append(
                evaluate_evidence(
                    root,
                    criterion_id=args.criterion_id,
                    check_command=args.check_command,
                    verified_inputs=args.verified_inputs,
                    evidence_revision=args.evidence_revision,
                    require_evidence=args.require_evidence,
                    check_exit_code=None,
                    check_executed=False,
                    declared_only=args.declared_only,
                )
            )

        if execution_signals:
            # Re-read scope after checks: a verification command can create or
            # modify paths. Never report the pre-check set as the final tree.
            final_changes = collect_changes(root, args)
            same_scope = (
                final_changes.complete == changes.complete
                and final_changes.paths == changes.paths
                and final_changes.escapes == changes.escapes
            )
            if not same_scope:
                final_changes.complete = False
                final_changes.errors.append("change set changed during check execution")
            changes = final_changes
            scope = evaluate_scope(contract, changes) if not contract_errors else ScopeEval(
                ok=False, signal_class="UNKNOWN"
            )
        evidence = evidence_items[0] if len(evidence_items) == 1 else None

        outcome, gate, exit_code = choose_gate(
            scope=scope,
            changes=changes,
            evidence=evidence_items,
            contract_errors=contract_errors,
            repair_attempts=args.repair_attempts,
            max_repair=args.max_repair,
        )
        if contract_errors:
            outcome, gate, exit_code = "invocation_error", "CLARIFY", 2

        signals: list[dict[str, Any]] = [
            {
                "name": "diff_paths",
                "class": "OBSERVED" if changes.complete else "UNKNOWN",
                "value": sorted(changes.paths),
                "complete": changes.complete,
                "errors": changes.errors,
                "mode": changes.mode,
            }
        ]
        signals.extend(execution_signals)
        if not contract_errors:
            signals.append(
                {
                    "name": "scope_check",
                    "class": scope.signal_class,
                    "value": {
                        "ok": scope.ok,
                        "violations": scope.violations,
                        "unexpected": scope.unexpected,
                    },
                    "limits": scope.limits,
                }
            )

        evidence_out: list[dict[str, Any]] = []
        for evidence in evidence_items:
            evidence_out.append(
                {
                    "criterion_id": evidence.criterion_id,
                    "check": evidence.check,
                    "result": evidence.result,
                    "exit_code": evidence.exit_code,
                    "sufficiency": evidence.sufficiency,
                    "verified_inputs": evidence.verified_inputs,
                    "content_revision": evidence.content_revision,
                    "expected_revision": evidence.expected_revision,
                    "class": evidence.signal_class,
                    "d_ac_hint": evidence.d_ac_hint,
                    "limits": evidence.limits,
                }
            )

        recovery = {
            "max_repair_attempts": args.max_repair,
            "repair_attempts": args.repair_attempts,
            "excluded_auto_repair": False,
            "destructive_rollback": False,
            "policy": (
                "Repair only within allowed_paths; never auto-edit excluded; "
                "fixture reset only via declared protocol; no git reset --hard"
            ),
        }

        if evidence is not None:
            overall_sufficiency = evidence.sufficiency
        elif evidence_items:
            overall_sufficiency = (
                "sufficient"
                if all(item.sufficiency == "sufficient" for item in evidence_items)
                else "insufficient"
            )
        else:
            overall_sufficiency = "unknown_incomplete" if not changes.complete else "n/a"

        verdict = Verdict(
            work_id=contract.work_id,
            outcome_class=outcome,
            gate_hint=gate,
            signals=signals,
            evidence=evidence_out,
            limits=list(DEFAULT_LIMITS),
            recovery=recovery,
            scope={
                "allowed_paths": contract.allowed_paths,
                "excluded_paths": contract.excluded_paths,
                "mode": contract.mode,
                "changed_paths": scope.changed_paths,
                "violations": scope.violations,
                "unexpected": scope.unexpected,
            },
            content_revision=evidence.content_revision if evidence else None,
            governing_revision=contract.governing_revision,
            sufficiency=overall_sufficiency,
            transition_recommendation=gate,
        )
        if contract_errors:
            verdict.signals.append(
                {
                    "name": "contract_validation",
                    "class": "OBSERVED",
                    "value": {"ok": False, "errors": contract_errors},
                }
            )

        emit(verdict, args.format)
        return exit_code

    except Exception as exc:  # internal_error
        eprint(f"internal_error: {exc}")
        try:
            emit(
                Verdict(
                    work_id=getattr(args, "work_id", None) or "unknown",
                    outcome_class="internal_error",
                    gate_hint="STOP",
                    signals=[],
                    evidence=[],
                    limits=DEFAULT_LIMITS,
                ),
                getattr(args, "format", "json"),
            )
        except Exception:
            pass
        return 2


def emit(verdict: Verdict, fmt: str) -> None:
    data = verdict.to_dict()
    if fmt == "json":
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print(f"work_id={data['work_id']}")
        print(f"outcome_class={data['outcome_class']}")
        print(f"gate_hint={data['gate_hint']}")
        print(f"sufficiency={data.get('sufficiency')}")
        scope = data.get("scope") or {}
        if scope.get("violations"):
            print(f"violations={scope['violations']}")
        if scope.get("unexpected"):
            print(f"unexpected={scope['unexpected']}")
        for ev in data.get("evidence") or []:
            print(
                f"evidence criterion={ev.get('criterion_id')} "
                f"result={ev.get('result')} sufficiency={ev.get('sufficiency')} "
                f"class={ev.get('class')}"
            )
        print(f"limits={data['limits']}")


if __name__ == "__main__":
    sys.exit(main())
