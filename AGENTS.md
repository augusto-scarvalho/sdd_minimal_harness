# Instructions for the runtime agent

This repository is meant to be worked on directly by the agent that has read, edit, and execution tools.

## Goal of the cycle

Repeat `inspect → edit → verify → critique` until the specification criteria are satisfied or a real blocker exists.

## Mandatory procedure

1. Read `.sdd/runtime-loop.yaml`, the selected spec, and the highest-priority item with status `ready`.
2. Run `python tools/runtime_iteration.py --spec <spec> --prepare`.
3. Inspect the report at `.sdd/runtime_runs/latest.json`.
4. Edit the allowed files directly.
5. Tests may be edited when needed to reflect the specification, but must never be weakened just to get a green result.
6. Run the specific verification and then the global regression.
7. Run `python tools/runtime_iteration.py --spec <spec> --verify`.
8. On failure, use the diagnostics to make another edit and repeat the cycle.
9. Stop only in the `satisfied`, `blocked`, or `needs_human_decision` states.

## Integrity rules

- The specification is the functional source of truth.
- Do not remove assertions, do not turn tests into trivial checks, and do not use `skip` or `xfail` to mask failures.
- Do not change `.sdd/runtime-loop.yaml`, `tools/sdd_config.yaml`, or the oracles during an iteration.
- Do not declare success without executed commands and recorded evidence.
- Do not include credentials, endpoints, or any Chat Completions dependency.

## Mandatory `tasks.md` synchronization

When a task is completed and verified, the agent MUST also update `.sdd/specs/<spec>/tasks.md` in the same iteration:

- mark as `- [x]` only the task whose corresponding status in `backlog.yaml` is `verified`;
- keep as `- [ ]` tasks that are open, blocked, rejected, or awaiting a human decision;
- never mark `[x]` just because code was edited: the specific verification and the global regression must have passed;
- keep the same task identifier (`TSKxx`) to allow auditing and correlation;
- before ending the iteration, check that `tasks.md`, `backlog.yaml`, the ledger, and the evidence show the same state;
- if they diverge, treat `backlog.yaml` and the executable evidence as the operational sources, fix `tasks.md`, and record the synchronization in the iteration report.

A completed task is only considered documentally closed when code, tests, `backlog.yaml`, the ledger, and the `tasks.md` checkbox are consistent.

## Replacing the `hello-transform` example

When the user starts their own program, read `REPLACE_EXAMPLE.md` before editing the repository. The agent must:

1. identify and remove only the files exclusive to the example;
2. preserve the reusable core of the harness;
3. create the new spec, code, and tests;
4. update every reference to the name `hello-transform`;
5. regenerate `SELF_CHECK.md` and regenerate `AGENT_LOOP_MANIFEST.json` at the end;
6. run the residual-reference check described in the replacement guide.

Do not delete core files just because they reference the example: some must be adapted, not removed.
