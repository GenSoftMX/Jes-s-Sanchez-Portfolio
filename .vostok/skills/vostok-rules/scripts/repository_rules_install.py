"""Non-overwriting incorporation of the repository-rules skill and tools.

No hooks/configuration are installed. Existing identical files are preserved
without claiming ownership; different contents always conflict in this version.
"""
import hashlib
import json
import os
from pathlib import Path

PREFIX = ".vostok/skills/vostok-rules"


def sha(content):
    return hashlib.sha256(content).hexdigest()


def payload(package_root):
    package_root=Path(package_root).resolve()
    skill=package_root/f"{PREFIX}/SKILL.md"
    scripts=package_root/"tools"
    if not skill.exists() and (package_root/"SKILL.md").is_file():
        skill=package_root/"SKILL.md";scripts=package_root/"scripts"
    return {f"{PREFIX}/SKILL.md":skill.read_bytes(),
            **{f"{PREFIX}/scripts/{name}":(scripts/name).read_bytes() for name in
               ("repository_rules.py","repository_rule_contracts.py","repository_rules_install.py",
                "repository_rule_evaluator.py","repository_rule_protection.py","cursor_g2_gate.py",
                "check_scope_evidence.py", "repository_rule_cache.py")}}


def plan(root, files, read):
    root=Path(root).resolve(strict=True)
    rows=[]
    for name,content in sorted(files.items()):
        target=root/name
        try:
            current=read(root,name)
            state="identical_preexisting" if current==content else "conflict"
        except FileNotFoundError:
            # A missing leaf is creatable only when every existing ancestor is
            # a real directory. Never traverse a customized symlink directory.
            state="create"
            for parent in list(target.parents):
                if parent==root:break
                if parent.is_symlink() or (parent.exists() and not parent.is_dir()):state="conflict"
        except (OSError,ValueError):
            state="conflict"
        rows.append({"path":name,"sha256":sha(content),"state":state,"ownership_claimed":False})
    result={"schema":"vostok.rules-install-plan.v1","root":str(root),"files":rows,
            "status":"blocked" if any(row["state"]=="conflict" for row in rows) else "preview",
            "limits":["skill_and_contract_tools_only","no_hooks_or_host_config","no_protection_activation",
                      "existing_files_never_overwritten","identical_does_not_establish_ownership"]}
    result["plan_digest"]=sha(json.dumps(result,sort_keys=True,separators=(",",":")).encode())
    return result


def create(root,name,content,created_dirs,created_files):
    parts=Path(name).parts
    directory=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    current=Path(root)
    try:
        for part in parts[:-1]:
            current=current/part
            try:
                os.mkdir(part,dir_fd=directory)
                created_dirs.append(current)
            except FileExistsError:
                pass
            child=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=directory)
            os.close(directory);directory=child
        descriptor=os.open(parts[-1],os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644,dir_fd=directory)
        created_files.append(name)
        try:
            with os.fdopen(descriptor,"wb",closefd=False) as handle:
                handle.write(content);handle.flush();os.fsync(handle.fileno())
        finally:os.close(descriptor)
    finally:os.close(directory)


def apply(root,files,expected_digest,read):
    root=Path(root).resolve(strict=True)
    preview=plan(root,files,read)
    if preview["plan_digest"]!=expected_digest or preview["status"]=="blocked":
        return {**preview,"status":"blocked","reason":"plan_changed_or_conflicting"}
    created,dirs=[],[]
    try:
        for row in preview["files"]:
            name=row["path"]
            if row["state"]=="identical_preexisting":
                if read(root,name)!=files[name]:raise ValueError("existing artifact changed during incorporation")
                continue
            # Register before writing, so partial writes are visible as residue
            # rather than claimed as a clean rollback.
            create(root,name,files[name],dirs,created)
        return {**preview,"status":"installed_catalog_tools_only","created":created,
                "preserved":[row["path"] for row in preview["files"] if row["state"]=="identical_preexisting"]}
    except (OSError,ValueError):
        removed,preserved=[],[]
        for name in reversed(created):
            try:
                if read(root,name)==files[name]:
                    (root/name).unlink();removed.append(name)
                else:preserved.append(name)
            except (OSError,ValueError):preserved.append(name)
        for directory in reversed(dirs):
            try:directory.rmdir()
            except OSError:pass
        return {**preview,"status":"blocked","reason":"partial_incorporation_failed",
                "removed_unchanged_created_files":removed,"preserved_concurrent_changes":preserved,
                "limits":preview["limits"]+["inspect_partial_transaction_residue"]}
