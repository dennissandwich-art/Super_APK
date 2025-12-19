# state_diff.py
# BRANCH: main
# ROLE: Compute diffs between state snapshots (PURE)

def diff_states(old: dict, new: dict) -> dict:
    added = {k: v for k, v in new.items() if k not in old}
    removed = {k: v for k, v in old.items() if k not in new}
    changed = {
        k: {"from": old[k], "to": new[k]}
        for k in old
        if k in new and old[k] != new[k]
    }
    return {"added": added, "removed": removed, "changed": changed}
