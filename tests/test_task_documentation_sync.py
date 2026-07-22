from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_agent_is_instructed_to_sync_tasks_markdown():
    instructions = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "Mandatory `tasks.md` synchronization" in instructions
    assert "- [x]" in instructions
    assert "backlog.yaml" in instructions
    assert "specific verification" in instructions
    assert "global regression" in instructions


def test_finished_demo_tasks_are_checked_and_match_backlog():
    spec = ROOT / ".sdd/specs/hello-transform"
    backlog = yaml.safe_load((spec / "backlog.yaml").read_text(encoding="utf-8"))["backlog"]
    tasks_md = (spec / "tasks.md").read_text(encoding="utf-8")
    for task in backlog:
        marker = "[x]" if task["status"] == "verified" else "[ ]"
        assert f"- {marker} {task['id']}:" in tasks_md
