# Harness SDD mínimo

Um harness leve para Desenvolvimento Orientado por Especificações (Spec-Driven Development — SDD), com agentes, backlog dinâmico, ledger somente para acréscimos e verificação por Python.

Ele foi projetado para executar:

- localmente;
- dentro de contêiner ou pod;
- em um ambiente de agente com ferramentas de leitura, edição e terminal (por exemplo, o runtime temporário de código do ChatGPT ou do Microsoft 365 Copilot em modo agente);
- em CI/CD;
- com qualquer linguagem de implementação, desde que os comandos de verificação sejam configurados em YAML.

## Visão geral

```text
Especificação + backlog + ledger
               ↓
Runner seleciona a tarefa `ready` de maior prioridade
               ↓
Agente inspeciona, edita e executa verificações
               ↓
Verificador executa testes específicos e regressão
               ↓
Tarefa passa para `verified` ou `blocked`
               ↓
Ledger e `tasks.md` são sincronizados
               ↓
Ciclo continua até zerar o backlog ou encontrar bloqueio
```

O runner não implementa código sozinho. O agente da sessão usa o runner e `tools/runtime_iteration.py` como trilhos auditáveis para trabalhar em uma tarefa por vez.

## Início rápido

Requisitos: Python 3.10+.

```bash
cd sdd_minimal_harness
pip install -r requirements.txt
python -m pytest -q
python tools/sdd_runner.py --spec hello-transform --status
python tools/runtime_iteration.py --spec hello-transform --prepare
```

## Documentação principal

- `AGENTS.md`: instruções obrigatórias para o agente.
- `RUNTIME_LOOP.md`: execução do ciclo nativo de edição e verificação.
- `SUBSTITUIR_EXEMPLO.md`: arquivos a excluir, adaptar, manter e criar ao trocar `hello-transform` por um programa próprio.
- `SELF_CHECK.md`: critérios de autoverificação do pacote atual.

## Estrutura

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

## Comandos principais

### Ver o status

```bash
python tools/sdd_runner.py --spec hello-transform --status
```

### Validar a especificação e o backlog

```bash
python tools/sdd_runner.py --spec hello-transform --check
```

### Executar uma iteração do runner

```bash
python tools/sdd_runner.py --spec hello-transform --once
```

### Executar o runner até zerar o backlog

```bash
python tools/sdd_runner.py --spec hello-transform --loop
```

### Preparar ou verificar uma iteração do agente

```bash
python tools/runtime_iteration.py --spec hello-transform --prepare
python tools/runtime_iteration.py --spec hello-transform --verify --reason "Descrição da alteração"
```

### Gerar o contexto da próxima tarefa

```bash
python tools/sdd_runner.py --spec hello-transform --next-prompt
```

## Adaptação para outra linguagem

Edite `tools/sdd_config.yaml`:

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

O runner é agnóstico em relação à linguagem e apenas executa os comandos declarados.

## Estados possíveis

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

## Regras essenciais

- uma tarefa `ready` precisa ter os campos mínimos;
- toda tarefa precisa estar vinculada a critérios de aceite;
- toda tarefa precisa declarar consumidores e evidências;
- referências do tipo `arquivo.py::test_nome` precisam existir;
- os comandos configurados precisam passar;
- cada iteração registra eventos em `ledger.jsonl`;
- uma tarefa `verified` deve estar marcada com `[x]` em `tasks.md`;
- o ciclo para quando não há tarefas abertas ou quando existe bloqueio.

## Substituição da demonstração

O repositório inclui `hello-transform` como exemplo concluído. Para criar um programa próprio, não remova o repositório inteiro. Siga `SUBSTITUIR_EXEMPLO.md`, que contém a árvore de arquivos, a lista de exclusões, os arquivos a adaptar e a estrutura mínima a criar.
