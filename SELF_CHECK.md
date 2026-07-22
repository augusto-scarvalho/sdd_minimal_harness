# Resultado da autoverificação

Este arquivo registra a condição do pacote de demonstração. Ele deve ser regenerado quando `hello-transform` for substituído.

## Comandos executados

```bash
python -m pytest -q
python tools/sdd_runner.py --spec hello-transform --check
python tools/sdd_runner.py --spec hello-transform --status
python tools/runtime_iteration.py --spec hello-transform --prepare
```

## Critérios esperados

- todos os testes passam;
- a validação da especificação e do backlog passa;
- as duas tarefas estão em `verified`;
- não há tarefas abertas ou bloqueadas;
- `tasks.md` está sincronizado com `backlog.yaml`;
- o relatório do ciclo nativo apresenta `satisfied`.
