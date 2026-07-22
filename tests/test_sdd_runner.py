import json
import subprocess
import sys
from pathlib import Path


def test_runner_status_and_loop(tmp_path):
    root = Path(__file__).resolve().parents[1]
    status = subprocess.run(
        [sys.executable, "tools/sdd_runner.py", "--spec", "hello-transform", "--status"],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    )
    data = json.loads(status.stdout)
    assert data["total"] == 2


def test_normal_tests_pass():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_hello_transform.py", "-q"],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "4 passed" in result.stdout
