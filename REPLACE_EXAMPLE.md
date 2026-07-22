# Replacing the `hello-transform` example

This guide walks through removing the practical example and adding your own program without damaging the core of the harness.

## Safety principle

Do the replacement in a copy, branch, or worktree. Before deleting any file, identify whether it belongs exclusively to the example or is part of the reusable mechanism.

## Decision tree

```text
sdd_minimal_harness/
├── .sdd/
│   ├── runtime-loop.yaml                    ADAPT
│   ├── specs/
│   │   └── hello-transform/                 DELETE THE WHOLE DIRECTORY
│   │       ├── backlog.checked.yaml         DELETE
│   │       ├── backlog.seed.yaml            DELETE
│   │       ├── backlog.yaml                 DELETE
│   │       ├── design.md                    DELETE
│   │       ├── ledger.jsonl                 DELETE
│   │       ├── requirements.md              DELETE
│   │       ├── review.md                    DELETE
│   │       └── tasks.md                     DELETE
│   └── steering/                            KEEP
├── src/
│   └── hello_transform.py                   DELETE
├── tests/
│   ├── test_hello_transform.py              DELETE
│   ├── test_sdd_runner.py                   ADAPT
│   ├── test_runtime_iteration.py            ADAPT
│   └── test_task_documentation_sync.py      ADAPT
├── tools/
│   ├── inject_audit_fault.py                DELETE OR REWRITE
│   ├── reset_demo.py                        DELETE OR REWRITE
│   ├── runtime_iteration.py                 KEEP
│   ├── sdd_config.yaml                      KEEP AND ADAPT
│   └── sdd_runner.py                        KEEP
├── AGENTS.md                                KEEP
├── RUNTIME_LOOP.md                          KEEP AND ADAPT
├── README.md                                KEEP AND ADAPT
├── SELF_CHECK.md                            REGENERATE
├── AGENT_LOOP_MANIFEST.json                 REGENERATE
├── pyproject.toml                           KEEP OR ADAPT
└── .gitignore                               KEEP
```

## Files that can be deleted

### Example specification

Delete the whole directory:

```text
.sdd/specs/hello-transform/
```

It contains only the requirements, design, tasks, backlog, review, and history of the example.

### Example code and tests

Delete:

```text
src/hello_transform.py
tests/test_hello_transform.py
```

### Demo-specific tools

Delete or rewrite:

```text
tools/inject_audit_fault.py
tools/reset_demo.py
```

`inject_audit_fault.py` knows a specific fault of `hello_transform.py`. `reset_demo.py` restores the demo backlog. Neither should remain unchanged in a different program.

### Artifacts that must be regenerated

Remove during the migration and generate again at the end:

```text
SELF_CHECK.md
AGENT_LOOP_MANIFEST.json
```

These files describe a run and hashes of the previous package; they become stale after any replacement.

## Files to adapt

Review every reference to `hello-transform` or `hello_transform` in:

```text
.sdd/runtime-loop.yaml
tests/test_sdd_runner.py
tests/test_runtime_iteration.py
tests/test_task_documentation_sync.py
README.md
RUNTIME_LOOP.md
pyproject.toml
tools/sdd_config.yaml
```

Not all of them will need a functional change, but all of them must be checked.

## Files to preserve

The reusable core is:

```text
AGENTS.md
.sdd/steering/
tools/runtime_iteration.py
tools/sdd_runner.py
tools/sdd_config.yaml
.gitignore
```

Also preserve `.sdd/runtime-loop.yaml`, adapting the spec name, the commands, and the policies when needed.

## Minimum structure to include for the new program

Assuming the identifier is `my-program`:

```text
.sdd/specs/my-program/
├── requirements.md
├── design.md
├── tasks.md
├── backlog.yaml
├── backlog.seed.yaml
├── review.md
└── ledger.jsonl

src/
└── my_program.py

tests/
└── test_my_program.py
```

### Rules for the new artifacts

- `requirements.md`: goal, scope, stories, and identifiable acceptance criteria.
- `design.md`: technical decisions, components, and test strategy.
- `tasks.md`: tasks with stable IDs and initially unchecked checkboxes.
- `backlog.yaml`: the same IDs as `tasks.md`, related criteria, inputs, outputs, evidence, and priority.
- `backlog.seed.yaml`: reproducible initial state of the new run.
- `review.md`: initial review and points of attention.
- `ledger.jsonl`: initially empty file.
- `src/`: the program implementation.
- `tests/`: tests linked to the acceptance criteria.

## Recommended sequence

1. Create a working copy or branch.
2. Delete the files exclusive to the example.
3. Create `.sdd/specs/<new-spec>/` and its minimum artifacts.
4. Update `spec:` in `.sdd/runtime-loop.yaml`.
5. Update the commands in `tools/sdd_config.yaml` and `.sdd/runtime-loop.yaml`.
6. Adapt the harness's own tests that still use the old name.
7. Implement the new program and its tests.
8. Run the native agent loop until every task is `verified`.
9. Synchronize the `tasks.md` checkboxes.
10. Regenerate `SELF_CHECK.md` and `AGENT_LOOP_MANIFEST.json`.
11. Remove caches and temporary files before creating the final package.

## Residual-reference check

Before finishing, run:

```bash
grep -RIn --exclude-dir=.git --exclude='*.pyc'   -e 'hello-transform' -e 'hello_transform' .
```

The result must contain only references intentionally preserved in historical documentation. In a fully converted package, the expected result is empty.

## Checklist

```markdown
- [ ] Work in a copy, branch, or worktree
- [ ] Delete `.sdd/specs/hello-transform/`
- [ ] Delete `src/hello_transform.py`
- [ ] Delete `tests/test_hello_transform.py`
- [ ] Delete or adapt `tools/inject_audit_fault.py`
- [ ] Delete or adapt `tools/reset_demo.py`
- [ ] Create `.sdd/specs/<new-spec>/`
- [ ] Create requirements, design, tasks, backlog, review, and ledger
- [ ] Create the new program's code and tests
- [ ] Update `.sdd/runtime-loop.yaml`
- [ ] Update the verification commands
- [ ] Adapt the harness's internal tests
- [ ] Update the README and the loop guide
- [ ] Check residual references to the example
- [ ] Run all tests
- [ ] Confirm the backlog has no open items
- [ ] Confirm `tasks.md` is synchronized
- [ ] Regenerate `SELF_CHECK.md`
- [ ] Regenerate `AGENT_LOOP_MANIFEST.json`
- [ ] Remove caches before packaging
```
