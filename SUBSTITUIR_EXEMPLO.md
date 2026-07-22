# Substituição do exemplo `hello-transform`

Este guia orienta a remoção do exemplo prático e a inclusão de um programa próprio sem danificar o núcleo do harness.

## Princípio de segurança

Faça a substituição em uma cópia, branch ou worktree. Antes de excluir qualquer arquivo, identifique se ele pertence exclusivamente ao exemplo ou se faz parte do mecanismo reutilizável.

## Árvore de decisão

```text
sdd_minimal_harness/
├── .sdd/
│   ├── runtime-loop.yaml                    ADAPTAR
│   ├── specs/
│   │   └── hello-transform/                 EXCLUIR TODO O DIRETÓRIO
│   │       ├── backlog.checked.yaml         EXCLUIR
│   │       ├── backlog.seed.yaml            EXCLUIR
│   │       ├── backlog.yaml                 EXCLUIR
│   │       ├── design.md                    EXCLUIR
│   │       ├── ledger.jsonl                 EXCLUIR
│   │       ├── requirements.md              EXCLUIR
│   │       ├── review.md                    EXCLUIR
│   │       └── tasks.md                     EXCLUIR
│   └── steering/                            MANTER
├── src/
│   └── hello_transform.py                   EXCLUIR
├── tests/
│   ├── test_hello_transform.py              EXCLUIR
│   ├── test_sdd_runner.py                   ADAPTAR
│   ├── test_runtime_iteration.py            ADAPTAR
│   └── test_task_documentation_sync.py      ADAPTAR
├── tools/
│   ├── inject_audit_fault.py                EXCLUIR OU REESCREVER
│   ├── reset_demo.py                        EXCLUIR OU REESCREVER
│   ├── runtime_iteration.py                 MANTER
│   ├── sdd_config.yaml                      MANTER E ADAPTAR
│   └── sdd_runner.py                        MANTER
├── AGENTS.md                                MANTER
├── RUNTIME_LOOP.md                          MANTER E ADAPTAR
├── README.md                                MANTER E ADAPTAR
├── SELF_CHECK.md                            REGENERAR
├── AGENT_LOOP_MANIFEST.json                 REGENERAR
├── pyproject.toml                           MANTER OU ADAPTAR
└── .gitignore                               MANTER
```

## Arquivos que podem ser excluídos

### Especificação do exemplo

Exclua todo o diretório:

```text
.sdd/specs/hello-transform/
```

Ele contém somente requisitos, design, tarefas, backlog, revisão e histórico do exemplo.

### Código e testes do exemplo

Exclua:

```text
src/hello_transform.py
tests/test_hello_transform.py
```

### Ferramentas específicas da demonstração

Exclua ou reescreva:

```text
tools/inject_audit_fault.py
tools/reset_demo.py
```

`inject_audit_fault.py` conhece uma falha específica de `hello_transform.py`. `reset_demo.py` restaura o backlog da demonstração. Nenhum deles deve permanecer inalterado em um programa diferente.

### Artefatos que devem ser regenerados

Remova durante a migração e gere novamente ao final:

```text
SELF_CHECK.md
AGENT_LOOP_MANIFEST.json
```

Esses arquivos descrevem uma execução e hashes do pacote anterior; portanto, ficam obsoletos após qualquer substituição.

## Arquivos que devem ser adaptados

Revise todas as referências a `hello-transform` ou `hello_transform` em:

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

Nem todos precisarão de mudança funcional, mas todos devem ser verificados.

## Arquivos que devem ser preservados

O núcleo reutilizável é:

```text
AGENTS.md
.sdd/steering/
tools/runtime_iteration.py
tools/sdd_runner.py
tools/sdd_config.yaml
.gitignore
```

Preserve também `.sdd/runtime-loop.yaml`, adaptando o nome da especificação, os comandos e as políticas quando necessário.

## Estrutura mínima a incluir para o novo programa

Supondo que o identificador seja `meu-programa`:

```text
.sdd/specs/meu-programa/
├── requirements.md
├── design.md
├── tasks.md
├── backlog.yaml
├── backlog.seed.yaml
├── review.md
└── ledger.jsonl

src/
└── meu_programa.py

tests/
└── test_meu_programa.py
```

### Regras para os novos artefatos

- `requirements.md`: objetivo, escopo, histórias e critérios de aceite identificáveis.
- `design.md`: decisões técnicas, componentes e estratégia de testes.
- `tasks.md`: tarefas com IDs estáveis e checkboxes inicialmente desmarcados.
- `backlog.yaml`: os mesmos IDs de `tasks.md`, critérios relacionados, entradas, saídas, evidências e prioridade.
- `backlog.seed.yaml`: estado inicial reproduzível da nova execução.
- `review.md`: revisão inicial e pontos de atenção.
- `ledger.jsonl`: arquivo inicialmente vazio.
- `src/`: implementação do programa.
- `tests/`: testes vinculados aos critérios de aceite.

## Sequência recomendada

1. Crie uma cópia ou branch de trabalho.
2. Exclua os arquivos exclusivos do exemplo.
3. Crie `.sdd/specs/<nova-especificação>/` e seus artefatos mínimos.
4. Atualize `spec:` em `.sdd/runtime-loop.yaml`.
5. Atualize os comandos em `tools/sdd_config.yaml` e `.sdd/runtime-loop.yaml`.
6. Adapte os testes do próprio harness que ainda usam o nome antigo.
7. Implemente o novo programa e seus testes.
8. Execute o ciclo nativo do agente até todas as tarefas ficarem `verified`.
9. Sincronize os checkboxes de `tasks.md`.
10. Regenere `SELF_CHECK.md` e `AGENT_LOOP_MANIFEST.json`.
11. Remova caches e arquivos temporários antes de criar o ZIP final.

## Verificação de referências residuais

Antes de concluir, execute:

```bash
grep -RIn --exclude-dir=.git --exclude='*.pyc'   -e 'hello-transform' -e 'hello_transform' .
```

O resultado deve conter somente referências intencionalmente preservadas em documentação histórica. Em um pacote totalmente convertido, o resultado esperado é vazio.

## Checklist

```markdown
- [ ] Trabalhar em cópia, branch ou worktree
- [ ] Excluir `.sdd/specs/hello-transform/`
- [ ] Excluir `src/hello_transform.py`
- [ ] Excluir `tests/test_hello_transform.py`
- [ ] Excluir ou adaptar `tools/inject_audit_fault.py`
- [ ] Excluir ou adaptar `tools/reset_demo.py`
- [ ] Criar `.sdd/specs/<nova-especificação>/`
- [ ] Criar requisitos, design, tarefas, backlog, revisão e ledger
- [ ] Criar o código e os testes do novo programa
- [ ] Atualizar `.sdd/runtime-loop.yaml`
- [ ] Atualizar os comandos de verificação
- [ ] Adaptar os testes internos do harness
- [ ] Atualizar README e guia do ciclo
- [ ] Verificar referências residuais ao exemplo
- [ ] Executar todos os testes
- [ ] Confirmar backlog sem itens abertos
- [ ] Confirmar `tasks.md` sincronizado
- [ ] Regenerar `SELF_CHECK.md`
- [ ] Regenerar `AGENT_LOOP_MANIFEST.json`
- [ ] Remover caches antes de empacotar
```
