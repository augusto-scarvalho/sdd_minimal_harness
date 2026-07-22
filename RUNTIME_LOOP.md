# Native agent loop

The expected runtime is the session agent itself, with read, edit, and terminal access. There is no endpoint configuration and no API key.

## Getting started

```bash
python tools/runtime_iteration.py --spec hello-transform --prepare
```

The command runs the initial verification and creates `.sdd/runtime_runs/latest.json`. If it fails, the agent must read the output, edit `src/`, `tests/`, and — when justified — the spec, then run:

```bash
python tools/runtime_iteration.py --spec hello-transform --verify   --reason "Fix based on the previous iteration's diagnostics"
```

Repeat after each edit. The report contains status, commands, outputs, hashes, and the file delta.

## Controlled repair-capability test

Use a disposable copy of the repository:

```bash
python tools/inject_audit_fault.py --spec hello-transform --fault wrong-strip
python tools/runtime_iteration.py --spec hello-transform --prepare
```

This injects a known defect into `src/hello_transform.py`. The agent must diagnose, edit, and repeat the verification until `satisfied`. Do not run the injection on the main branch.

## Files the agent may change

- `src/**`;
- `tests/**`;
- `.sdd/specs/<spec>/**`, when there is ambiguity or a real need for refinement.

Tests may be changed, but the agent must record the justification with `--reason`.

## Completion synchronization

When a task passes the specific verification and the global regression, the agent must update the corresponding item in `.sdd/specs/<spec>/tasks.md` from `- [ ]` to `- [x]`. The checkbox must match the `verified` status in `backlog.yaml`.

Before finishing, the agent must check the consistency between checkbox, backlog, ledger, and evidence.

## Replacing the example

To remove `hello-transform` and add your own program, follow `REPLACE_EXAMPLE.md`. The guide distinguishes files to delete, adapt, keep, and regenerate.
