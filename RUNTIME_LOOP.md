# Ciclo nativo do agente

O runtime esperado é o próprio agente da sessão, com acesso a leitura, edição e terminal. Não existe configuração de endpoint nem chave de API.

## Início

```bash
python tools/runtime_iteration.py --spec hello-transform --prepare
```

O comando executa a verificação inicial e cria `.sdd/runtime_runs/latest.json`. Se houver falha, o agente deve ler a saída, editar `src/`, `tests/` e, quando justificável, a especificação, e então executar:

```bash
python tools/runtime_iteration.py --spec hello-transform --verify   --reason "Correção baseada no diagnóstico da iteração anterior"
```

Repita após cada edição. O relatório contém status, comandos, saídas, hashes e o delta dos arquivos.

## Teste controlado da capacidade de reparo

Use uma cópia descartável do repositório:

```bash
python tools/inject_audit_fault.py --spec hello-transform --fault wrong-strip
python tools/runtime_iteration.py --spec hello-transform --prepare
```

Isso injeta um defeito conhecido em `src/hello_transform.py`. O agente deve diagnosticar, editar e repetir a verificação até `satisfied`. Não execute a injeção no branch principal.

## Arquivos que o agente pode alterar

- `src/**`;
- `tests/**`;
- `.sdd/specs/<especificação>/**`, quando houver ambiguidade ou necessidade real de refinamento.

Os testes podem ser alterados, mas o agente deve registrar a justificativa com `--reason`.

## Sincronização da conclusão

Quando uma tarefa passar pela verificação específica e pela regressão global, o agente deve atualizar o item correspondente em `.sdd/specs/<especificação>/tasks.md` de `- [ ]` para `- [x]`. A marcação deve corresponder ao status `verified` em `backlog.yaml`.

Antes de encerrar, o agente deve conferir a coerência entre checkbox, backlog, ledger e evidências.

## Substituição do exemplo

Para remover `hello-transform` e incluir um programa próprio, siga `SUBSTITUIR_EXEMPLO.md`. O guia distingue arquivos a excluir, adaptar, manter e regenerar.
