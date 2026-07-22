# Instruções para o agente de runtime

Este repositório deve ser trabalhado diretamente pelo agente que possui ferramentas de leitura, edição e execução.

## Objetivo do ciclo

Repetir `inspecionar → alterar → verificar → criticar` até que os critérios da especificação sejam satisfeitos ou exista um bloqueio real.

## Procedimento obrigatório

1. Leia `.sdd/runtime-loop.yaml`, a especificação selecionada e o item de maior prioridade com status `ready`.
2. Execute `python tools/runtime_iteration.py --spec <especificação> --prepare`.
3. Inspecione o relatório em `.sdd/runtime_runs/latest.json`.
4. Edite diretamente os arquivos permitidos.
5. Os testes podem ser editados quando necessário para refletir a especificação, mas nunca devem ser enfraquecidos apenas para obter resultado verde.
6. Execute a verificação específica e, depois, a regressão global.
7. Execute `python tools/runtime_iteration.py --spec <especificação> --verify`.
8. Se houver falha, use o diagnóstico para fazer nova edição e repita o ciclo.
9. Pare somente nos estados `satisfied`, `blocked` ou `needs_human_decision`.

## Regras de integridade

- A especificação é a fonte de verdade funcional.
- Não remova asserções, não transforme testes em verificações triviais e não use `skip` ou `xfail` para mascarar falhas.
- Não altere `.sdd/runtime-loop.yaml`, `tools/sdd_config.yaml` nem os oráculos durante uma iteração.
- Não declare sucesso sem comandos executados e evidências registradas.
- Não inclua credenciais, endpoints nem dependência de Chat Completions.

## Sincronização obrigatória de `tasks.md`

Ao concluir e verificar uma tarefa, o agente DEVE atualizar também o arquivo `.sdd/specs/<especificação>/tasks.md` na mesma iteração:

- marque como `- [x]` somente a tarefa cujo status correspondente em `backlog.yaml` seja `verified`;
- mantenha como `- [ ]` as tarefas abertas, bloqueadas, rejeitadas ou que aguardem decisão humana;
- nunca marque `[x]` apenas porque o código foi editado: a verificação específica e a regressão global devem ter passado;
- preserve o mesmo identificador da tarefa (`TSKxx`) para permitir auditoria e correlação;
- antes de encerrar a iteração, confira se `tasks.md`, `backlog.yaml`, o ledger e as evidências apresentam o mesmo estado;
- se houver divergência, trate `backlog.yaml` e as evidências executáveis como fontes operacionais, corrija `tasks.md` e registre a sincronização no relatório da iteração.

Uma tarefa realizada somente é considerada documentalmente encerrada quando código, testes, `backlog.yaml`, ledger e checkbox de `tasks.md` estiverem coerentes.

## Substituição do exemplo `hello-transform`

Quando o usuário iniciar um programa próprio, leia `SUBSTITUIR_EXEMPLO.md` antes de editar o repositório. O agente deve:

1. identificar e remover apenas os arquivos exclusivos do exemplo;
2. preservar o núcleo reutilizável do harness;
3. criar a nova especificação, o código e os testes;
4. atualizar todas as referências ao nome `hello-transform`;
5. regenerar `SELF_CHECK.md` e regenerar `AGENT_LOOP_MANIFEST.json` ao final;
6. executar a verificação de referências residuais descrita no guia de substituição.

Não exclua arquivos do núcleo apenas porque fazem referência ao exemplo: alguns devem ser adaptados, e não removidos.
