# Design — hello-transform

## Overview

The feature is implemented as a pure function in `src/hello_transform.py`.

## Components

- `src/hello_transform.py`: `normalize_text` function.
- `tests/test_hello_transform.py`: behavior tests.

## Technical decisions

- Use a pure function to keep the behavior deterministic.
- Raise `ValueError` for invalid inputs.
- Use `strip()` for normalization.

## Test strategy

- Test valid text.
- Test space stripping.
- Test null input.
- Test empty input.
