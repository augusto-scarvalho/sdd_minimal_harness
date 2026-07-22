# Self-check result

This file records the condition of the demo package. It must be regenerated when `hello-transform` is replaced.

## Commands executed

```bash
python -m pytest -q
python tools/sdd_runner.py --spec hello-transform --check
python tools/sdd_runner.py --spec hello-transform --status
python tools/runtime_iteration.py --spec hello-transform --prepare
```

## Expected criteria

- all tests pass;
- the spec and backlog validation passes;
- both tasks are `verified`;
- there are no open or blocked tasks;
- `tasks.md` is synchronized with `backlog.yaml`;
- the native loop report shows `satisfied`.
