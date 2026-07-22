# Minimal SDD Harness

A lightweight harness for Spec-Driven Development (SDD) with agents, a dynamic backlog, an append-only ledger, and Python-based verification.

It is designed to run:

- locally;
- inside a container or pod;
- in an agent environment with read, edit, and terminal tools (for example, the temporary code runtime of ChatGPT or Microsoft 365 Copilot in agent mode);
- in CI/CD;
- with any implementation language, as long as the verification commands are configured in YAML.

## Overview

```text
Spec + backlog + ledger
               ↓
Runner selects the highest-priority `ready` task
               ↓
Agent inspects, edits, and runs verifications
               ↓
Verifier runs task-specific tests and the global regression
               ↓
Task moves to `verified` or `blocked`
               ↓
Ledger and `tasks.md` are synchronized
               ↓
Cycle continues until the backlog is empty or a blocker is found
```

The runner does not implement code by itself. The session agent uses the runner and `tools/runtime_iteration.py` as auditable rails to work on one task at a time.

## Quick start

Requirements: Python 3.10+.

```bash
cd sdd_minimal_harness
pip install -r requirements.txt
python -m pytest -q
python tools/sdd_runner.py --spec hello-transform --status
python tools/runtime_iteration.py --spec hello-transform --prepare
```

## Core documentation

- `AGENTS.md`: mandatory instructions for the agent.
- `RUNTIME_LOOP.md`: running the native edit-and-verify cycle.
- `REPLACE_EXAMPLE.md`: files to delete, adapt, keep, and create when replacing `hello-transform` with your own program.
- `SELF_CHECK.md`: self-verification criteria for the current package.

## Structure

```text
.sdd/
├── runtime-loop.yaml
├── steering/
│   ├── agent-protocol.md
│   ├── critic-policy.md
│   ├── backlog-policy.md
│   └── spec-quality.md
└── specs/
    └── hello-transform/
        ├── requirements.md
        ├── design.md
        ├── tasks.md
        ├── backlog.yaml
        ├── backlog.seed.yaml
        ├── ledger.jsonl
        └── review.md
src/
└── hello_transform.py
tests/
├── test_hello_transform.py
├── test_sdd_runner.py
├── test_runtime_iteration.py
└── test_task_documentation_sync.py
tools/
├── sdd_runner.py
├── runtime_iteration.py
├── sdd_config.yaml
├── reset_demo.py
└── inject_audit_fault.py
.github/workflows/ci.yml
LICENSE
requirements.txt
```

## Main commands

### Show status

```bash
python tools/sdd_runner.py --spec hello-transform --status
```

### Validate the spec and backlog

```bash
python tools/sdd_runner.py --spec hello-transform --check
```

### Run one runner iteration

```bash
python tools/sdd_runner.py --spec hello-transform --once
```

### Run the runner until the backlog is empty

```bash
python tools/sdd_runner.py --spec hello-transform --loop
```

### Prepare or verify an agent iteration

```bash
python tools/runtime_iteration.py --spec hello-transform --prepare
python tools/runtime_iteration.py --spec hello-transform --verify --reason "Description of the change"
```

### Generate the next-task context

```bash
python tools/sdd_runner.py --spec hello-transform --next-prompt
```

## Adapting to another language

Edit `tools/sdd_config.yaml`:

```yaml
commands:
  verify:
    - "python -m pytest -q"
    # - "npm test"
    # - "go test ./..."
    # - "mvn test"
    # - "dotnet test"
    # - "make test"
```

The runner is language-agnostic and simply executes the declared commands.

## Possible states

```text
candidate
refine_required
ready
in_progress
implemented
critic_review
verified
blocked
rejected
stale
pruned
needs_human_decision
```

## Essential rules

- a `ready` task must have the minimum fields;
- every task must be linked to acceptance criteria;
- every task must declare consumers and evidence;
- references like `file.py::test_name` must exist;
- the configured commands must pass;
- each iteration records events in `ledger.jsonl`;
- a `verified` task must be checked `[x]` in `tasks.md`;
- the cycle stops when there are no open tasks or a blocker exists.

## Replacing the demo

The repository ships `hello-transform` as a completed example. To build your own program, do not delete the whole repository. Follow `REPLACE_EXAMPLE.md`, which contains the file tree, the deletion list, the files to adapt, and the minimum structure to create.
