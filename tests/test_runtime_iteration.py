import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_runtime_iteration_cli_is_available():
    p=subprocess.run([sys.executable,'tools/runtime_iteration.py','--help'],cwd=ROOT,text=True,capture_output=True)
    assert p.returncode==0
    assert '--prepare' in p.stdout and '--verify' in p.stdout

def test_runtime_config_is_agent_native():
    text=(ROOT/'.sdd/runtime-loop.yaml').read_text(encoding='utf-8')
    assert 'mode: agent_native' in text
    assert 'endpoint' not in text.lower()
    assert 'api_key' not in text.lower()
