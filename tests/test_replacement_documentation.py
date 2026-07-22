from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_replacement_guide_lists_delete_adapt_keep_and_create_actions():
    text = (ROOT / "REPLACE_EXAMPLE.md").read_text(encoding="utf-8")
    for expected in [
        ".sdd/specs/hello-transform/",
        "src/hello_transform.py",
        "tests/test_hello_transform.py",
        "tools/inject_audit_fault.py",
        "tools/reset_demo.py",
        "Example specification",
        "Files to adapt",
        "Files to preserve",
        "Minimum structure to include",
    ]:
        assert expected in text


def test_agent_instructions_reference_replacement_guide():
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "REPLACE_EXAMPLE.md" in text
    assert "regenerate `SELF_CHECK.md`" in text
    assert "regenerate `AGENT_LOOP_MANIFEST.json`" in text


def test_main_documentation_uses_english_headings():
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    runtime = (ROOT / "RUNTIME_LOOP.md").read_text(encoding="utf-8")
    assert "Instructions" in agents
    assert "synchronization" in agents
    assert "Native agent loop" in runtime
    assert "verification" in runtime
