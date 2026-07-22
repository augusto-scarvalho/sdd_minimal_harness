# Requirements — hello-transform

## Objetivo

Normalizar texto de entrada de forma determinística.

## Escopo

- Receber uma string.
- Remover espaços no início e no fim.
- Rejeitar valores nulos, não texto ou vazios.

## Fora de escopo

- Persistência.
- Interface gráfica.
- Integrações externas.

## Histórias de usuário

### US01 — Normalizar entrada textual

Como consumidor da função, quero normalizar texto para obter um valor limpo.

#### Critérios de aceite

- CA01: QUANDO a entrada for texto válido, O SISTEMA DEVE retornar o texto normalizado.
- CA02: QUANDO a entrada tiver espaços no início ou no fim, O SISTEMA DEVE remover esses espaços.

### US02 — Rejeitar entrada inválida

Como consumidor da função, quero receber erro quando a entrada for inválida.

#### Critérios de aceite

- CA03: QUANDO a entrada for nula, O SISTEMA DEVE retornar erro de validação.
- CA04: QUANDO a entrada estiver vazia após normalização, O SISTEMA DEVE retornar erro de validação.
