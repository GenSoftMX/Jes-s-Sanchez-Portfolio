"""Versioned contracts for derived rule maps and deterministic task bindings.

The harness interprets prose. This module checks traceability/coverage and
never claims semantic completeness or authenticates a reviewer.
"""
import functools
import re

MAP_SCHEMA = "vostok.repository-rule-map.v1"
TASK_SCHEMA = "vostok.rule-task.v1"
BINDING_SCHEMA = "vostok.task-rule-binding.v1"
DOMAINS = {"governance", "architecture_api", "style_lint", "structure", "domain_use_cases",
           "testing", "security", "dependencies", "documentation_i18n", "git_release", "operations"}
RESOURCES = {"rule", "procedure", "knowledge", "configuration", "example"}
MODALITIES = {"mandatory", "prohibited", "recommended", "informative", "ambiguous"}
MODES = {"deterministic", "guided", "human", "independent", "unsupported"}
STAGES = {"intent", "context", "plan", "execute", "verify", "acceptance", "handoff"}
RULE_FIELDS = {"id", "source_units", "quote", "resource", "domains", "modality", "scope",
               "authority", "evaluation"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strings(value, *, nonempty=True, unique=True):
    return isinstance(value, list) and (bool(value) or not nonempty) and all(isinstance(s, str) and s for s in value) and (not unique or len(set(value)) == len(value))


def relative_path(value, patterns=False):
    require(isinstance(value, str) and value and not value.startswith("/") and "\\" not in value,
            "paths must be relative POSIX paths")
    require(all(p not in {"", ".", ".."} for p in value.rstrip("/").split("/")), "unsafe path component")
    require(not any(ord(c) < 32 for c in value), "control character in path")
    require(not value.endswith("/"), "use an explicit /** pattern for a directory")
    require(not patterns or not any(c in value for c in "[]{}"), "unsupported glob syntax")
    require(patterns or not any(c in value for c in "*?[]{}"), "task paths must be exact files")
    return value


@functools.lru_cache(maxsize=512)
def _compile_glob(pattern):
    relative_path(pattern, patterns=True)
    expression, index = "", 0
    while index < len(pattern):
        if pattern[index:index+3] == "**/":
            expression += "(?:.*/)?"; index += 3
        elif pattern[index:index+2] == "**":
            expression += ".*"; index += 2
        elif pattern[index] == "*":
            expression += "[^/]*"; index += 1
        elif pattern[index] == "?":
            expression += "[^/]"; index += 1
        else:
            expression += re.escape(pattern[index]); index += 1
    return re.compile(expression)


def matches(pattern, path):
    """Glob with * within a segment and ** across segments, no shell parsing."""
    compiled = _compile_glob(pattern)
    relative_path(path)
    return compiled.fullmatch(path) is not None


def draft(inventory, prior_mapping=None):
    all_units = {unit["id"]: unit for source in inventory["sources"] for unit in source["units"]}
    reusable_units = {uid for uid, unit in all_units.items() if not unit.get("ambiguous_duplicate", False)}
    treatments = {
        uid: {"kind": "unresolved", "reason": "needs_harness_interpretation", "rules": []}
        for uid in all_units
    }
    carried_rules = []
    carried_checks = {}
    carried_conflicts = []
    if prior_mapping is not None:
        require(isinstance(prior_mapping, dict) and isinstance(prior_mapping.get("treatments"), dict)
                and isinstance(prior_mapping.get("rules"), list), "invalid prior mapping for draft carry-from")
        if prior_mapping.get("reader") != inventory["reader"]:
            # Version migration is a new source review, never inferred from a
            # matching quote or caller-edited identifier.
            return draft(inventory)
        prior_treatments = prior_mapping["treatments"]
        valid_rules = {}
        for rule in prior_mapping["rules"]:
            if not isinstance(rule, dict) or not strings(rule.get("source_units", [])):
                continue
            if not set(rule["source_units"]) <= reusable_units:
                continue
            if not all(isinstance(prior_treatments.get(u), dict)
                       and prior_treatments[u].get("kind") == "obligation"
                       and rule.get("id") in prior_treatments[u].get("rules", [])
                       for u in rule["source_units"]):
                continue
            text = "\n".join((all_units[uid]["text"] or all_units[uid].get("redacted_structure") or "")
                             for uid in rule["source_units"])
            if isinstance(rule.get("quote"), str) and rule["quote"] and rule["quote"] in text:
                valid_rules[rule["id"]] = rule
        # A source treatment can own several obligations. If one cannot carry,
        # do not keep a convenient subset and mark that same source reviewed.
        while True:
            invalid = {rid for rid, rule in valid_rules.items()
                       if any(not set(prior_treatments[uid]["rules"]) <= set(valid_rules)
                              for uid in rule["source_units"])}
            if not invalid:
                break
            for rid in invalid:
                del valid_rules[rid]
        carried_rules = list(valid_rules.values())
        for uid in reusable_units:
            prior_t = prior_treatments.get(uid)
            if not isinstance(prior_t, dict) or prior_t.get("kind") not in {"obligation", "information", "example"}:
                continue
            if not isinstance(prior_t.get("reason"), str) or not prior_t["reason"]:
                continue
            if prior_t["kind"] == "obligation":
                kept = [rid for rid in prior_t.get("rules", []) if rid in valid_rules]
                if kept and len(kept) == len(prior_t.get("rules", [])):
                    treatments[uid] = {"kind": "obligation", "reason": prior_t["reason"], "rules": kept}
            else:
                treatments[uid] = {"kind": prior_t["kind"], "reason": prior_t["reason"], "rules": []}
        if isinstance(prior_mapping.get("checks"), dict):
            carried_checks = dict(prior_mapping["checks"])
        if isinstance(prior_mapping.get("conflicts"), list):
            carried_conflicts = [
                c for c in prior_mapping["conflicts"]
                if isinstance(c, dict) and set(c.get("rules", [])) <= set(valid_rules)
            ]
    has_unresolved = any(t["kind"] == "unresolved" for t in treatments.values())
    review = (
        dict(prior_mapping["review"])
        if prior_mapping is not None and not has_unresolved
        and isinstance(prior_mapping.get("review"), dict)
        and set(prior_mapping["review"]) == {"kind", "note"}
        else {"kind": "not_reviewed", "note": "Independent semantic corpus review pending"}
    )
    return {"schema": MAP_SCHEMA, "inventory_digest": inventory["inventory_digest"],
            "reader": inventory["reader"],
            "treatments": treatments,
            "rules": carried_rules, "checks": carried_checks, "conflicts": carried_conflicts,
            "review": review}


def validate_map(inventory, mapping):
    require(isinstance(mapping, dict) and set(mapping) == {"schema", "inventory_digest", "reader", "treatments", "rules", "checks", "conflicts", "review"}, "invalid map fields")
    require(mapping["schema"] == MAP_SCHEMA, "unsupported rule map schema")
    require(mapping["inventory_digest"] == inventory["inventory_digest"] and mapping["reader"] == inventory["reader"], "stale inventory or reader")
    require(inventory["complete"], "incomplete source inventory")
    all_units = {unit["id"]: unit for source in inventory["sources"] for unit in source["units"]}
    treatments = mapping["treatments"]
    require(isinstance(treatments, dict) and set(treatments) == set(all_units), "source unit omitted or invented")
    require(isinstance(mapping["rules"], list), "rules must be a list")
    rule_ids = set()
    blocked = []
    for rule in mapping["rules"]:
        require(isinstance(rule, dict) and set(rule) == RULE_FIELDS, "invalid rule fields")
        rid = rule["id"]
        require(isinstance(rid, str) and re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,79}", rid) is not None and rid not in rule_ids, "invalid or duplicate rule id")
        rule_ids.add(rid)
        require(strings(rule["source_units"]) and set(rule["source_units"]) <= set(all_units), f"unknown source unit: {rid}")
        text = "\n".join((all_units[uid]["text"] or all_units[uid].get("redacted_structure") or "") for uid in rule["source_units"])
        require(isinstance(rule["quote"], str) and rule["quote"] and rule["quote"] in text, f"rule quote does not match source: {rid}")
        require(rule["resource"] in RESOURCES and rule["modality"] in MODALITIES, f"invalid rule classification: {rid}")
        require(strings(rule["domains"]) and set(rule["domains"]) <= DOMAINS, f"invalid domain: {rid}")
        scope = rule["scope"]
        require(isinstance(scope, dict) and set(scope) == {"paths", "change_types", "operations", "stages", "conditions"}, f"invalid scope: {rid}")
        for key in ("paths", "change_types", "operations", "stages"):
            require(strings(scope[key]), f"empty or invalid scope {key}: {rid}")
        for path in scope["paths"]:
            relative_path(path, patterns=True)
        require(set(scope["stages"]) <= STAGES, f"unsupported stage: {rid}")
        require(isinstance(scope["conditions"], dict) and all(isinstance(k,str) and k and (type(v) in (str,bool,int)) for k,v in scope["conditions"].items()), f"invalid conditions: {rid}")
        authority = rule["authority"]
        require(isinstance(authority, dict) and set(authority) == {"status", "provenance", "delegation"}, f"invalid authority: {rid}")
        require(authority["status"] in {"declared", "accepted", "proposed", "unknown"} and isinstance(authority["provenance"], str) and authority["provenance"] and isinstance(authority["delegation"], str), f"invalid authority: {rid}")
        if authority["status"] in {"proposed", "unknown"} and rule["modality"] in {"mandatory", "prohibited"}:
            blocked.append({"rule": rid, "reason": "unresolved_authority"})
        evaluation = rule["evaluation"]
        require(isinstance(evaluation, dict) and set(evaluation) == {"mode", "checks", "stage", "requirement"}, f"invalid evaluation: {rid}")
        require(evaluation["mode"] in MODES and strings(evaluation["checks"],nonempty=False) and evaluation["stage"] in STAGES and isinstance(evaluation["requirement"],str) and evaluation["requirement"], f"invalid evaluation: {rid}")
        if evaluation["mode"] == "deterministic":
            require(bool(evaluation["checks"]), f"deterministic rule has no check: {rid}")
    for uid, treatment in treatments.items():
        require(isinstance(treatment,dict) and set(treatment)=={"kind","reason","rules"}, "invalid treatment fields")
        require(treatment["kind"] in {"obligation","information","example","unresolved"} and isinstance(treatment["reason"],str) and treatment["reason"] and strings(treatment["rules"],nonempty=False), "invalid unit treatment")
        require(set(treatment["rules"]) <= rule_ids, "treatment names an unknown rule")
        if treatment["kind"] == "obligation":
            require(bool(treatment["rules"]), "obligation lacks a rule")
        else:
            require(not treatment["rules"], "non-obligation cannot silently own rules")
        if treatment["kind"] == "unresolved":
            blocked.append({"unit": uid, "reason": "interpretation_pending"})
    for rule in mapping["rules"]:
        for uid in rule["source_units"]:
            require(rule["id"] in treatments[uid]["rules"], "rule and source treatment disagree")
    checks = mapping["checks"]
    require(isinstance(checks,dict), "checks must be a dictionary")
    for cid, check in checks.items():
        require(isinstance(cid,str) and cid and isinstance(check,dict)
                and {"argv","cwd","inputs","timeout","env_keys","outputs"}<=set(check)
                and set(check)<={"argv","cwd","inputs","timeout","env_keys","outputs","ephemeral_outputs"},
                "invalid check definition")
        ephemeral=check.get("ephemeral_outputs",[])
        require(strings(check["argv"],unique=False) and strings(check["inputs"]) and strings(check["env_keys"],nonempty=False)
                and strings(check["outputs"],nonempty=False) and strings(ephemeral,nonempty=False), "invalid check arguments/inputs")
        require(type(check["timeout"]) is int and 1 <= check["timeout"] <= 1800, "invalid check timeout")
        if check["cwd"] != ".": relative_path(check["cwd"])
        for path in check["inputs"]+check["outputs"]+ephemeral: relative_path(path,patterns=True)
    for rule in mapping["rules"]:
        require(set(rule["evaluation"]["checks"]) <= set(checks), "unknown check reference")
    require(isinstance(mapping["conflicts"],list), "invalid conflicts")
    for conflict in mapping["conflicts"]:
        require(isinstance(conflict,dict) and set(conflict)=={"rules","reason"} and strings(conflict["rules"]) and set(conflict["rules"])<=rule_ids and isinstance(conflict["reason"],str) and conflict["reason"], "invalid conflict record")
    review=mapping["review"]
    require(isinstance(review,dict) and set(review)=={"kind","note"} and review["kind"] in {"not_reviewed","reviewed_guided"} and isinstance(review["note"],str) and review["note"], "invalid review record")
    if review["kind"] != "reviewed_guided": blocked.append({"reason":"source_review_pending"})
    return blocked


def validate_task(task):
    require(isinstance(task,dict) and set(task)=={"schema","id","revision","paths","change_types","operations","facts"}, "invalid task fields")
    require(task["schema"]==TASK_SCHEMA and isinstance(task["id"],str) and task["id"] and isinstance(task["revision"],str) and task["revision"], "invalid task identity/revision")
    for key in ("paths","change_types","operations"):
        require(strings(task[key]),f"task requires {key}")
    for path in task["paths"]:relative_path(path)
    require(isinstance(task["facts"],dict) and all(isinstance(k,str) and k and type(v) in (bool,str,int) for k,v in task["facts"].items()), "invalid task facts")


def applicability(rule,task):
    scope=rule["scope"]
    if not any(matches(pattern,path) for pattern in scope["paths"] for path in task["paths"]):
        return "not_applicable","path_outside_scope"
    for key in ("change_types","operations"):
        if "*" not in scope[key] and not set(scope[key])&set(task[key]):
            return "not_applicable",f"{key}_outside_scope"
    unknown=[]
    for key,value in scope["conditions"].items():
        if key not in task["facts"]:unknown.append(key)
        elif type(task["facts"][key]) is not type(value) or task["facts"][key]!=value:
            return "not_applicable",f"condition_not_met:{key}"
    if unknown:return "unknown","missing_conditions:"+",".join(sorted(unknown))
    return "applicable","scope_matches"


def obligation_source_paths(inventory,mapping):
    paths=set()
    treatments=mapping["treatments"]
    for source in inventory["sources"]:
        for unit in source["units"]:
            treatment=treatments.get(unit["id"])
            if treatment and treatment["kind"]=="obligation":
                paths.add(source["path"])
    return paths


def path_touches(task_path,source_path):
    return task_path==source_path or task_path.startswith(source_path.rstrip("/")+"/")


def is_rule_surface(path):
    """Harness instruction surfaces; used when a weakened map drops obligation ownership."""
    parts = path.split("/")
    return parts[-1] in {"AGENTS.md", "CLAUDE.md", ".cursorrules"} or ".vostok" in parts or ".agents" in parts


def modifies_repository_rules(inventory,mapping,task,prior_mapping=None):
    """A positive declaration adds scope; a negative one cannot erase known sources."""
    fact=task["facts"].get("modifies_repository_rules")
    if fact is True:
        return True
    sources=obligation_source_paths(inventory,mapping)
    if prior_mapping is not None:
        sources |= obligation_source_paths(inventory,prior_mapping)
    elif fact is not False:
        sources |= {source["path"] for source in inventory.get("sources",[]) if isinstance(source,dict) and source.get("path")}
    return any(is_rule_surface(path) or any(path_touches(path,source) for source in sources) for path in task["paths"])


def agreement_weakening(prior_mapping,mapping,task):
    """Detect removed/weakened mandatory or prohibited obligations vs prior agreement.

    Deleting a guard from the map counts even when the current task path would
    not have activated it; narrowing that drops a previously active path also
    counts. This blocks self-justifying rewrites of the agreement.
    """
    require(isinstance(prior_mapping,dict) and prior_mapping.get("schema")==MAP_SCHEMA,"invalid prior agreement map")
    require(isinstance(prior_mapping.get("rules"),list),"invalid prior agreement rules")
    current={rule["id"]:rule for rule in mapping["rules"]}
    lost=[]
    for prior in prior_mapping["rules"]:
        if prior["modality"] not in {"mandatory","prohibited"}:
            continue
        rid=prior["id"]
        rule=current.get(rid)
        if rule is None:
            lost.append({"rule":rid,"reason":"removed_from_map"})
            continue
        if rule["modality"] not in {"mandatory","prohibited"}:
            lost.append({"rule":rid,"reason":"modality_weakened"})
            continue
        if rule["modality"] != prior["modality"]:
            lost.append({"rule":rid,"reason":"modality_changed"})
        before, after = prior["evaluation"], rule["evaluation"]
        if before["mode"] in {"deterministic", "human", "independent"} and after["mode"] != before["mode"]:
            lost.append({"rule":rid,"reason":"evaluation_mode_changed"})
        if before["stage"] != after["stage"]:
            lost.append({"rule":rid,"reason":"evaluation_stage_changed"})
        if not set(before["checks"]) <= set(after["checks"]):
            lost.append({"rule":rid,"reason":"required_check_removed"})
        for cid in sorted(set(before["checks"]) & set(after["checks"])):
            if prior_mapping.get("checks", {}).get(cid) != mapping["checks"].get(cid):
                lost.append({"rule":rid,"check":cid,"reason":"required_check_definition_changed"})
        prior_state,_=applicability(prior,task)
        current_state,_=applicability(rule,task)
        if prior_state!="not_applicable" and current_state=="not_applicable":
            lost.append({"rule":rid,"reason":"scope_narrowed_out"})
    return lost


def bind(inventory,mapping,task,map_digest,task_digest,prior_mapping=None):
    blocked=validate_map(inventory,mapping)
    validate_task(task)
    modifying = modifies_repository_rules(inventory,mapping,task,prior_mapping=prior_mapping)
    if modifying and task["facts"].get("modifies_repository_rules") is False:
        blocked.append({"reason":"repository_rules_fact_contradiction"})
    if modifying and prior_mapping is None:
        blocked.append({"reason":"prior_agreement_required"})
    # A supplied previous agreement is always checked, including when the task
    # declares ordinary code paths. The rewritten map cannot waive this check.
    if prior_mapping is not None and task["facts"].get("agreement_change_authorized") is not True:
        lost=agreement_weakening(prior_mapping,mapping,task)
        if lost:
            blocked.append({"reason":"agreement_weakening_without_authorization",
                            "rules":sorted({item["rule"] for item in lost}),"details":lost})
    rows=[]
    for rule in mapping["rules"]:
        state,reason=applicability(rule,task)
        rows.append({"rule":rule["id"],"applicability":state,"reason":reason})
        if state=="unknown" and rule["modality"] in {"mandatory","prohibited","ambiguous"}:
            blocked.append({"rule":rule["id"],"reason":reason})
        if state=="applicable" and (rule["modality"]=="ambiguous" or rule["evaluation"]["mode"]=="unsupported"):
            blocked.append({"rule":rule["id"],"reason":"unsupported_or_ambiguous_obligation"})
    active={row["rule"] for row in rows if row["applicability"]!="not_applicable"}
    for conflict in mapping["conflicts"]:
        if set(conflict["rules"])<=active:
            blocked.append({"reason":"unresolved_conflict","rules":conflict["rules"]})
    return {"schema":BINDING_SCHEMA,"inventory_digest":inventory["inventory_digest"],
            "worktree_id":inventory.get("worktree_id",""),
            "map_digest":map_digest,"task_digest":task_digest,"task_id":task["id"],"task_revision":task["revision"],
            "task_paths":list(task["paths"]),
            "rules":sorted(rows,key=lambda row:row["rule"]),"blockers":blocked,
            "status":"blocked" if blocked else "bound_needs_evaluation",
            "limits":["applicability_is_deterministic_over_guided_classification", "not_semantic_completeness",
                      "binding_is_not_protected_authorization","independent_review_and_host_activation_pending",
                      "prior_agreement_required_when_modifying_rules"]}


def validate_binding(inventory,mapping,task,binding,map_digest,task_digest,prior_mapping=None):
    expected=bind(inventory,mapping,task,map_digest,task_digest,prior_mapping=prior_mapping)
    require(binding==expected,"binding omitted/changed rules or belongs to stale map/task")
    return expected
