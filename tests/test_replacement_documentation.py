from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_replacement_guide_lists_delete_adapt_keep_and_create_actions():
    text = (ROOT / "SUBSTITUIR_EXEMPLO.md").read_text(encoding="utf-8")
    for expected in [
        ".sdd/specs/hello-transform/",
        "src/hello_transform.py",
        "tests/test_hello_transform.py",
        "tools/inject_audit_fault.py",
        "tools/reset_demo.py",
        "Especificação do exemplo",
        "Arquivos que devem ser adaptados",
        "Arquivos que devem ser preservados",
        "Estrutura mínima a incluir",
    ]:
        assert expected in text


def test_agent_instructions_reference_replacement_guide():
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "SUBSTITUIR_EXEMPLO.md" in text
    assert "regenerar `SELF_CHECK.md`" in text
    assert "regenerar `AGENT_LOOP_MANIFEST.json`" in text


def test_main_documentation_uses_accented_portuguese_headings():
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    runtime = (ROOT / "RUNTIME_LOOP.md").read_text(encoding="utf-8")
    assert "Instruções" in agents
    assert "Sincronização" in agents
    assert "Ciclo nativo" in runtime
    assert "verificação" in runtime
