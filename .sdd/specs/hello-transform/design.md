# Design — hello-transform

## Visão geral

A feature será implementada como uma função pura em `src/hello_transform.py`.

## Componentes

- `src/hello_transform.py`: função `normalize_text`.
- `tests/test_hello_transform.py`: testes de comportamento.

## Decisões técnicas

- Usar função pura para manter comportamento determinístico.
- Lançar `ValueError` para entradas inválidas.
- Usar `strip()` para normalização.

## Estratégia de testes

- Testar texto válido.
- Testar remoção de espaços.
- Testar entrada nula.
- Testar entrada vazia.
