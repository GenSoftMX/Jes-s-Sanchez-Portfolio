"""Portable G0/G1/G3 evaluator; candidate commands require exact authorization.

No caller-supplied exits/results are accepted. This module does not activate a
host profile or authenticate reviews. Human/independent obligations stay pending.

Multiple working directories are expressed as separate typed checks (one cwd each),
never by shell-concatenating `cd` chains. Declared check outputs may be added as
extra `--allowed` paths for the post-check 0003 bridge only; ignored/generated
files outside that set still yield UNKNOWN. Global ignore exemptions are forbidden.
"""
import hashlib
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from repository_rule_contracts import bind, matches, relative_path, require

BASE_ENV_KEYS={"PATH","HOME","LANG","LC_ALL","TMPDIR","SYSTEMROOT"}
EARLY_STAGES={"intent","context","plan"}
SCOPE_BRIDGE="scope_supervisor_v1"
EXCLUDED_DIRS={"node_modules",".venv","venv","dist","build","__pycache__",".next",".astro",".dart_tool","coverage",".git"}


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()


def _explicit_excluded_dirs(patterns):
    return {part for pattern in patterns for part in str(pattern).split("/") if part in EXCLUDED_DIRS and part!=".git"}


def list_files(root,include_dirs=()):
    root=Path(root)
    excluded=(EXCLUDED_DIRS-set(include_dirs)) if include_dirs else EXCLUDED_DIRS
    candidates=[]
    for directory,dirs,files in os.walk(root,followlinks=False):
        dirs[:]=[name for name in dirs if name not in excluded and name!=".git"]
        dir_path=Path(directory)
        for name in files:
            candidates.append(dir_path/name)
            require(len(candidates)<=100000,"check input discovery exceeds limit")
    return candidates


def match_files(root,patterns,reader=None,*,require_each=True):
    for pattern in patterns:
        relative_path(pattern,patterns=True)
    selected={}
    candidates=[(path,path.relative_to(root).as_posix()) for path in list_files(root,include_dirs=_explicit_excluded_dirs(patterns)) if not path.is_dir()]
    total=0
    for pattern in patterns:
        found=False
        for path,relative in candidates:
            if matches(pattern,relative):
                if reader is None:
                    selected[relative]=None
                elif relative not in selected:
                    content=reader(root,relative);total+=len(content)
                    require(total<=32*1024*1024,"check input bytes exceed limit")
                    selected[relative]=hashlib.sha256(content).hexdigest()
                found=True
        if require_each:
            require(found,"check input pattern has no files")
    return selected


def inputs(root,patterns,reader):
    return digest(match_files(root,patterns,reader,require_each=True))


def declared_output_paths(root,checks,check_ids):
    """Concrete files matching authorized check output patterns (E09 strategy)."""
    patterns=[pattern for cid in check_ids for pattern in (checks[cid].get("outputs") or [])]
    if not patterns:
        return []
    return sorted(match_files(root,patterns,reader=None,require_each=False))


def ephemeral_files(root,patterns):
    """Stream-hash files matching ephemeral_outputs without the 512KB text-source cap."""
    selected={}
    if not patterns:
        return selected
    for pattern in patterns:
        relative_path(pattern,patterns=True)
    candidates=[(path,path.relative_to(root).as_posix()) for path in list_files(root,include_dirs=_explicit_excluded_dirs(patterns))]
    for pattern in patterns:
        for path,relative in candidates:
            if relative not in selected and matches(pattern,relative) and path.is_file() and not path.is_symlink():
                h=hashlib.sha256()
                try:
                    with path.open("rb") as handle:
                        for block in iter(lambda:handle.read(1024*1024),b""):
                            h.update(block)
                    selected[relative]=h.hexdigest()
                except OSError:
                    selected[relative]="unreadable"
    return selected


def _ignored_untracked(root):
    try:
        result=subprocess.run(["git","-C",str(root),"ls-files","--others","--ignored","--exclude-standard","-z","--","."],
                              capture_output=True,check=False)
    except OSError:
        return []
    if result.returncode!=0:
        return []
    return [path for path in result.stdout.decode().split("\0") if path]


def run_check(root,check,reader):
    """The operator authorizes this whole typed check before it is invoked."""
    cwd=root/check["cwd"]
    require(cwd.resolve().is_relative_to(root) and cwd.is_dir(),"check cwd escapes or is missing")
    require(cwd.absolute()==cwd.resolve(),"symlink check cwd is unsupported")
    before=inputs(root,check["inputs"],reader)
    ephemeral_patterns=check.get("ephemeral_outputs") or []
    ephemeral_before=ephemeral_files(root,ephemeral_patterns)
    env={key:os.environ[key] for key in BASE_ENV_KEYS|set(check["env_keys"]) if key in os.environ}
    env["PYTHONDONTWRITEBYTECODE"]="1"
    record={"check_digest":digest(check),"input_digest_before":before,"cwd":check["cwd"],
            "environment_digest":digest(env),"environment_keys":sorted(env),"exit_code":None,
            "observed_only":True}
    started=time.monotonic()
    try:
        with tempfile.TemporaryFile() as out,tempfile.TemporaryFile() as err:
            process=subprocess.Popen(check["argv"],cwd=cwd,env=env,stdout=out,stderr=err,shell=False,start_new_session=True)
            try:
                process.wait(timeout=check["timeout"])
            except subprocess.TimeoutExpired:
                os.killpg(process.pid,signal.SIGKILL);process.wait()
                raise
            finally:
                # Checks are finite commands, not persistent services. Stop
                # any child left in this command's own process group.
                try:os.killpg(process.pid,signal.SIGKILL)
                except ProcessLookupError:pass
            for name,stream in (("stdout",out),("stderr",err)):
                size=stream.tell();stream.seek(0);h=hashlib.sha256()
                for block in iter(lambda:stream.read(1024*1024),b""):h.update(block)
                record[name+"_sha256"]=h.hexdigest();record[name+"_bytes"]=size
        record["exit_code"]=process.returncode
        record["state"]="pass_technical" if process.returncode==0 else "fail"
    except subprocess.TimeoutExpired:
        record["state"]="unknown";record["reason"]="check_timeout"
    except OSError:
        record["state"]="unknown";record["reason"]="check_unavailable"
    record["duration_ms"]=round((time.monotonic()-started)*1000)
    try:
        after=inputs(root,check["inputs"],reader)
        record["input_digest_after"]=after
        if after!=before:
            record["state"]="unknown";record["reason"]="inputs_changed_during_check"
    except (OSError,ValueError):
        record["state"]="unknown";record["reason"]="inputs_unreadable_after_check"
    if record.get("state")=="pass_technical" and check.get("outputs"):
        produced=match_files(root,check["outputs"],reader=None,require_each=False)
        record["declared_outputs"]=sorted(produced)
        record["declared_outputs_digest"]=digest(sorted(produced))
        if not produced:
            record["state"]="unknown";record["reason"]="declared_outputs_missing"
    if ephemeral_patterns:
        ephemeral_after=ephemeral_files(root,ephemeral_patterns)
        ignored_after=set(_ignored_untracked(root))
        created_ephemeral={k:v for k,v in ephemeral_after.items() if k not in ephemeral_before and k in ignored_after}
        cleaned=[]
        for rel_path in sorted(created_ephemeral):
            target=root/rel_path
            if (target.is_file() or target.is_symlink()) and target.parent.resolve().is_relative_to(root):
                try:
                    target.unlink()
                    cleaned.append(rel_path)
                except OSError:
                    pass
                parent=target.parent
                while parent!=root and parent.is_relative_to(root):
                    try:parent.rmdir()
                    except OSError:break
                    parent=parent.parent
        record["ephemeral_outputs_cleaned"]=cleaned
        record["ephemeral_outputs_digest"]=digest(created_ephemeral)
    return record


def scope_v1(root,task,helper,extra_allowed=None):
    # Explicit versioned bridge: preserve the closed 0003 implementation. These
    # environment overrides disable receiver-configured Git filesystem helpers.
    # Multiple cwds are NOT expressed here; only additional exact allowed paths
    # from declared check outputs may be appended after authorized execution.
    env=dict(os.environ,GIT_CONFIG_COUNT="2",GIT_CONFIG_KEY_0="core.fsmonitor",GIT_CONFIG_VALUE_0="false",
             GIT_CONFIG_KEY_1="core.untrackedCache",GIT_CONFIG_VALUE_1="false",GIT_OPTIONAL_LOCKS="0",
             GIT_PAGER="cat",GIT_CONFIG_NOSYSTEM="1",PYTHONDONTWRITEBYTECODE="1")
    command=[sys.executable,str(helper),"--root",str(root),"--work-id",task["id"],
             "--governing-revision",task["revision"],"--excluded-none","--diff-from","git"]
    allowed=[]
    for path in list(task["paths"])+list(extra_allowed or []):
        relative_path(path)
        if path not in allowed:
            allowed.append(path)
            command.extend(["--allowed",path])
    try:
        result=subprocess.run(command,capture_output=True,text=True,env=env,timeout=30)
        value=json.loads(result.stdout)
        require(isinstance(value,dict),"invalid scope response")
        return {"bridge":SCOPE_BRIDGE,"exit_code":result.returncode,"outcome_class":value.get("outcome_class"),
                "gate_hint":value.get("gate_hint"),"scope":value.get("scope"),"limits":value.get("limits",[]),
                "allowed_paths":allowed,
                "helper_sha256":hashlib.sha256(helper.read_bytes()).hexdigest()}
    except (OSError,ValueError,subprocess.TimeoutExpired):
        return {"bridge":SCOPE_BRIDGE,"exit_code":2,"outcome_class":"unknown_incomplete","reason":"scope_bridge_unavailable",
                "allowed_paths":allowed}


def evaluate(root,inventory,mapping,task,phase,authorized,reviews,reader,helper,scanner,prior_mapping=None):
    require(phase in {"preflight","verify"},"unsupported evaluation phase")
    require(isinstance(authorized,list) and all(isinstance(a,str) for a in authorized),"invalid check authorizations")
    require(isinstance(reviews,dict),"invalid guided reviews")
    # E07: there is no parameter for caller-supplied exits or fabricated check rows.
    result={"schema":"vostok.rule-validation-verdict.v1","phase":phase,"status":"blocked",
            "inventory_digest":inventory.get("inventory_digest"),"map_digest":digest(mapping),"task_digest":digest(task),
            "binding":None,"rules":[],"checks":{},"blockers":[],
            "limits":["semantic_interpretation_guided","reviews_not_authenticated","no_host_protection",
                      "no_human_acceptance","external_processes_not_controlled",
                      "prior_agreement_required_when_modifying_rules",
                      "no_caller_supplied_exits","no_global_ignore_exemption",
                      "multi_cwd_via_separate_checks_only",f"bridge:{SCOPE_BRIDGE}"]}
    if not inventory.get("complete",False):
        result["blockers"]=[{"reason":"incomplete_inventory"}]
        return result
    binding=bind(inventory,mapping,task,digest(mapping),digest(task),prior_mapping=prior_mapping)
    blockers=list(binding["blockers"])
    result["binding"]=binding
    result["blockers"]=blockers
    active={row["rule"] for row in binding["rules"] if row["applicability"]=="applicable"}
    necessary=[]
    execute_ids=[]
    for rule in mapping["rules"]:
        rid=rule["id"]
        if rid not in active:
            result["rules"].append({"rule":rid,"state":"not_applicable" if next(row for row in binding["rules"] if row["rule"]==rid)["applicability"]=="not_applicable" else "unknown"})
            continue
        required=rule["modality"] in {"mandatory","prohibited","ambiguous"}
        evaluation=rule["evaluation"]
        row={"rule":rid,"state":"not_evaluated","mode":evaluation["mode"]}
        result["rules"].append(row)
        if not required:
            row["reason"]="nonmandatory_advice";continue
        if phase=="preflight" and evaluation["stage"] not in EARLY_STAGES:
            row["reason"]="scheduled_for_later_stage"
            if evaluation["mode"]=="deterministic":necessary.extend(evaluation["checks"])
            continue
        if evaluation["mode"] in {"human","independent"}:
            row["state"]="pending_human";blockers.append({"rule":rid,"reason":"external_reviewer_required"})
        elif evaluation["mode"]=="guided":
            review=reviews.get(rid)
            if not isinstance(review,dict) or set(review)!={"state","note","map_digest","task_digest"} or review.get("state")!="reviewed_guided" or not isinstance(review.get("note"),str) or not review["note"] or review.get("map_digest")!=digest(mapping) or review.get("task_digest")!=digest(task):
                row["state"]="unknown";blockers.append({"rule":rid,"reason":"guided_review_missing_or_stale"})
            else:row["state"]="reviewed_guided"
        elif evaluation["mode"]=="deterministic":
            necessary.extend(evaluation["checks"]);execute_ids.extend(evaluation["checks"])
        else:
            row["state"]="unknown";blockers.append({"rule":rid,"reason":"evaluation_unsupported"})
    necessary=sorted(set(necessary))
    for cid in necessary:
        if digest(mapping["checks"][cid]) not in authorized:
            blockers.append({"check":cid,"reason":"candidate_check_not_authorized",
                             "required_authorization_digest":digest(mapping["checks"][cid]),"candidate":mapping["checks"][cid]})
    # Do not run target code on unresolved policy or missing authorization.
    if blockers:return result
    if phase=="preflight" and not execute_ids:
        result["status"]="ready_for_execution";return result
    scope=scope_v1(root,task,helper)
    result[SCOPE_BRIDGE]=scope
    if scope["exit_code"]!=0:
        blockers.append({"reason":"scope_unknown_or_failed"});return result
    for cid in sorted(set(execute_ids)):
        try:record=run_check(root,mapping["checks"][cid],reader)
        except (OSError,ValueError):record={"state":"unknown","reason":"invalid_or_unreadable_check_inputs","observed_only":True}
        result["checks"][cid]=record
    for row in result["rules"]:
        if row["rule"] not in active or row["mode"]!="deterministic":continue
        rule=next(rule for rule in mapping["rules"] if rule["id"]==row["rule"])
        if rule["modality"] not in {"mandatory","prohibited","ambiguous"}:continue
        if phase=="preflight" and rule["evaluation"]["stage"] not in EARLY_STAGES:continue
        states=[result["checks"][cid]["state"] for cid in rule["evaluation"]["checks"]]
        row["state"]="pass_technical" if all(state=="pass_technical" for state in states) else ("fail" if "fail" in states else "unknown")
        if row["state"]!="pass_technical":blockers.append({"rule":row["rule"],"reason":"check_failed_or_unknown"})
    # Post-check scope (E09): record declared outputs and pass them as extra
    # --allowed for attribution, but never treat Git-ignored untracked files as
    # green. Spec 0003 reports UNKNOWN/incomplete for ignored paths; 0004 keeps
    # that fail-closed result and only distinguishes declared vs undeclared sets.
    extra=[]
    if not any(b.get("reason")=="check_failed_or_unknown" for b in blockers):
        successful=[cid for cid in sorted(set(execute_ids)) if result["checks"].get(cid,{}).get("state")=="pass_technical"]
        extra=declared_output_paths(root,mapping["checks"],successful)
    after=scope_v1(root,task,helper,extra_allowed=extra)
    result[f"{SCOPE_BRIDGE}_after"]=after
    result["declared_outputs_recorded"]=extra
    if after["exit_code"]!=0:
        ignored=sorted(_ignored_untracked(root))
        unexpected=[path for path in ignored if path not in set(extra)]
        if ignored and not unexpected:
            blockers.append({"reason":"declared_ignored_outputs_unknown","paths":ignored,
                             "strategy":"keep_unknown_until_non_ignored_evidence_or_bridge_extension"})
        else:
            blockers.append({"reason":"scope_after_checks_unknown_or_failed",
                             "undeclared_ignored_paths":unexpected[:50]})
    try:
        current=scanner(root)
        if not current["complete"] or current["inventory_digest"]!=inventory["inventory_digest"]:
            blockers.append({"reason":"sources_or_reader_changed_during_verification"})
    except (OSError,ValueError,RuntimeError,subprocess.SubprocessError):
        blockers.append({"reason":"source_freshness_unknown"})
    result["status"]="blocked" if blockers else ("ready_for_execution" if phase=="preflight" else "ready_for_review")
    return result
