#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
OPEN_STATUSES = {"candidate", "refine_required", "ready", "in_progress", "implemented", "critic_review", "blocked", "rejected", "stale", "needs_human_decision"}
TERMINAL_STATUSES = {"verified", "pruned"}
REQUIRED_TASK_FIELDS = ["id", "title", "status", "type", "related_criteria", "consumes", "produces", "evidence_expected", "priority"]
READY_ALLOWED_TYPES = {"code", "test", "spec", "decision", "prune", "ops", "code_and_test", "shell"}


def load_yaml(path: Path) -> dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML missing. Install with: pip install pyyaml")
    if not path.exists():
        raise FileNotFoundError(path)
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    if yaml is None:
        raise RuntimeError("PyYAML missing. Install with: pip install pyyaml")
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def now_id(prefix: str) -> str:
    return f"{prefix}-{int(time.time() * 1000)}"


def append_ledger(spec_dir: Path, event: dict[str, Any]) -> None:
    ledger = spec_dir / "ledger.jsonl"
    event.setdefault("id", now_id("LEDGER"))
    event.setdefault("ts", int(time.time()))
    with ledger.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def spec_dir_for(spec_name: str) -> Path:
    return ROOT / ".sdd" / "specs" / spec_name


def load_backlog(spec_dir: Path) -> dict[str, Any]:
    return load_yaml(spec_dir / "backlog.yaml")


def save_backlog(spec_dir: Path, data: dict[str, Any]) -> None:
    dump_yaml(spec_dir / "backlog.yaml", data)


def task_score(task: dict[str, Any]) -> int:
    return int(task.get("priority", {}).get("score", 0))


def select_top_ready(backlog: list[dict[str, Any]]) -> dict[str, Any] | None:
    ready = [task for task in backlog if task.get("status") == "ready"]
    ready.sort(key=task_score, reverse=True)
    return ready[0] if ready else None


def validate_ready_task(task: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_TASK_FIELDS:
        if field not in task or task[field] in (None, "", []):
            errors.append(f"missing or empty required field: {field}")
    if task.get("status") != "ready":
        errors.append("task is not in ready status")
    if task.get("type") not in READY_ALLOWED_TYPES:
        errors.append(f"invalid type: {task.get('type')}")
    if not task.get("related_criteria"):
        errors.append("task has no related acceptance criteria")
    if not task.get("evidence_expected"):
        errors.append("task has no expected evidence")
    if not task.get("consumes"):
        errors.append("task has no consumed artifacts")
    if not task.get("produces"):
        errors.append("task has no produced evidence/artifacts")
    return errors


def evidence_exists(ref: str) -> bool:
    """Check evidence references.

    Supports:
    - path/to/file
    - path/to/test_file.py::test_function
    - arbitrary text evidence, which is ignored and considered non-file evidence
    """
    if "::" in ref:
        file_part, symbol = ref.split("::", 1)
        path = ROOT / file_part
        if not path.exists():
            return False
        text = path.read_text(encoding="utf-8", errors="ignore")
        return re.search(rf"def\s+{re.escape(symbol)}\s*\(", text) is not None
    if any(ref.endswith(ext) for ext in [".py", ".js", ".ts", ".java", ".go", ".cs", ".md", ".yaml", ".yml", ".json"]):
        return (ROOT / ref).exists()
    if ref.startswith("src/") or ref.startswith("tests/") or ref.startswith(".sdd/"):
        return (ROOT / ref).exists()
    return True


def validate_evidence(task: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for ref in task.get("produces", []):
        if not evidence_exists(str(ref)):
            missing.append(str(ref))
    return missing


def run_commands(commands: list[str]) -> tuple[int, list[dict[str, Any]]]:
    results: list[dict[str, Any]] = []
    final = 0
    for cmd in commands:
        if cmd == "python" or cmd.startswith("python "):
            # ponytail: 'python' may not exist on PATH (Windows/py launcher)
            cmd = f'"{sys.executable}"' + cmd[len("python"):]
        print(f"[sdd-runner] $ {cmd}")
        proc = subprocess.run(cmd, shell=True, cwd=ROOT, text=True, capture_output=True)
        result = {
            "cmd": cmd,
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-2000:],
            "stderr_tail": proc.stderr[-2000:],
        }
        results.append(result)
        if proc.stdout:
            print(proc.stdout)
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
        if proc.returncode != 0:
            final = proc.returncode
            break
    return final, results


def configured_commands() -> list[str]:
    cfg_path = ROOT / "tools" / "sdd_config.yaml"
    if not cfg_path.exists():
        return []
    data = load_yaml(cfg_path)
    return list(data.get("commands", {}).get("verify", []))


def status_summary(backlog: list[dict[str, Any]]) -> dict[str, int]:
    summary: dict[str, int] = {"total": len(backlog), "open": 0, "verified": 0, "pruned": 0, "blocked": 0, "ready": 0}
    for task in backlog:
        status = task.get("status", "")
        if status in TERMINAL_STATUSES:
            summary[status] = summary.get(status, 0) + 1
        else:
            summary["open"] += 1
            summary[status] = summary.get(status, 0) + 1
    return summary


def print_status(spec_dir: Path, backlog_data: dict[str, Any]) -> None:
    summary = status_summary(backlog_data.get("backlog", []))
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def check_all(spec_dir: Path, backlog_data: dict[str, Any]) -> int:
    errors: list[str] = []
    for name in ["requirements.md", "design.md", "tasks.md", "backlog.yaml", "ledger.jsonl"]:
        if not (spec_dir / name).exists():
            errors.append(f"missing file: {name}")
    for task in backlog_data.get("backlog", []):
        if task.get("status") == "ready":
            errors.extend([f"{task.get('id')}: {e}" for e in validate_ready_task(task)])
            errors.extend([f"{task.get('id')}: missing evidence: {e}" for e in validate_evidence(task)])
    if errors:
        for error in errors:
            print(f"[CHECK-FAIL] {error}")
        append_ledger(spec_dir, {"event": "check_failed", "errors": errors})
        return 1
    print("[CHECK-PASS] spec/backlog/minimum evidence OK")
    append_ledger(spec_dir, {"event": "check_passed"})
    return 0


def run_once(spec_dir: Path, backlog_data: dict[str, Any]) -> int:
    backlog = backlog_data.get("backlog", [])
    task = select_top_ready(backlog)
    if not task:
        print("[sdd-runner] no ready task.")
        append_ledger(spec_dir, {"event": "no_ready_task"})
        return 0

    task_id = task.get("id")
    print(f"[sdd-runner] selected task: {task_id} - {task.get('title')}")
    ready_errors = validate_ready_task(task)
    evidence_errors = validate_evidence(task)
    if ready_errors or evidence_errors:
        task["status"] = "blocked"
        task["block_reason"] = {"ready_errors": ready_errors, "evidence_errors": evidence_errors}
        save_backlog(spec_dir, backlog_data)
        append_ledger(spec_dir, {"event": "task_blocked", "task_id": task_id, "ready_errors": ready_errors, "evidence_errors": evidence_errors})
        return 1

    append_ledger(spec_dir, {"event": "task_started", "task_id": task_id, "criteria": task.get("related_criteria")})
    commands = configured_commands()
    rc, command_results = run_commands(commands)
    if rc != 0:
        task["status"] = "blocked"
        task["block_reason"] = {"verify_returncode": rc}
        save_backlog(spec_dir, backlog_data)
        append_ledger(spec_dir, {"event": "task_blocked", "task_id": task_id, "command_results": command_results})
        return rc

    task["status"] = "verified"
    task["verified_at"] = int(time.time())
    task["evidence_produced"] = task.get("produces", [])
    save_backlog(spec_dir, backlog_data)
    append_ledger(spec_dir, {"event": "task_verified", "task_id": task_id, "evidence": task.get("produces", []), "command_results": command_results})
    print(f"[sdd-runner] task verified: {task_id}")
    return 0


def run_loop(spec_dir: Path) -> int:
    iterations = 0
    while True:
        backlog_data = load_backlog(spec_dir)
        summary = status_summary(backlog_data.get("backlog", []))
        if summary["open"] == 0:
            print("[sdd-runner] backlog cleared.")
            append_ledger(spec_dir, {"event": "backlog_zero", "iterations": iterations})
            return 0
        ready = select_top_ready(backlog_data.get("backlog", []))
        if not ready:
            print("[sdd-runner] open items remain, but none ready. Stopping for intervention/refinement.")
            append_ledger(spec_dir, {"event": "loop_stopped_no_ready", "summary": summary})
            return 1
        rc = run_once(spec_dir, backlog_data)
        iterations += 1
        if rc != 0:
            return rc
        if iterations > 100:
            append_ledger(spec_dir, {"event": "loop_safety_stop"})
            return 2


def next_prompt(spec_dir: Path, backlog_data: dict[str, Any]) -> int:
    task = select_top_ready(backlog_data.get("backlog", []))
    if not task:
        print("No ready task.")
        return 1
    req = (spec_dir / "requirements.md").read_text(encoding="utf-8")
    design = (spec_dir / "design.md").read_text(encoding="utf-8")
    print("# Iteration Context")
    print("\n## Top backlog item\n")
    print(json.dumps(task, indent=2, ensure_ascii=False))
    print("\n## Requirements\n")
    print(req[:4000])
    print("\n## Design\n")
    print(design[:3000])
    print("\n## Mandatory instruction\n")
    print("Work only on this task. Do not create a new artifact without a consumer. Produce evidence and run the verifier.")
    append_ledger(spec_dir, {"event": "next_prompt_generated", "task_id": task.get("id")})
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="sdd Minimal Harness")
    parser.add_argument("--spec", required=True)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--loop", action="store_true")
    parser.add_argument("--next-prompt", action="store_true")
    args = parser.parse_args()

    spec_dir = spec_dir_for(args.spec)
    if not spec_dir.exists():
        print(f"Spec not found: {spec_dir}", file=sys.stderr)
        return 2
    backlog_data = load_backlog(spec_dir)

    if args.status:
        print_status(spec_dir, backlog_data)
        return 0
    if args.check:
        return check_all(spec_dir, backlog_data)
    if args.once:
        return run_once(spec_dir, backlog_data)
    if args.loop:
        return run_loop(spec_dir)
    if args.next_prompt:
        return next_prompt(spec_dir, backlog_data)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
