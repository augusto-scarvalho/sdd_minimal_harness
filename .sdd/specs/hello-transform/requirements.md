# Requirements — hello-transform

## Goal

Normalize input text deterministically.

## Scope

- Receive a string.
- Strip leading and trailing spaces.
- Reject null, non-text, or empty values.

## Out of scope

- Persistence.
- Graphical interface.
- External integrations.

## User stories

### US01 — Normalize text input

As a consumer of the function, I want to normalize text to get a clean value.

#### Acceptance criteria

- CA01: WHEN the input is valid text, THE SYSTEM SHALL return the normalized text.
- CA02: WHEN the input has leading or trailing spaces, THE SYSTEM SHALL remove those spaces.

### US02 — Reject invalid input

As a consumer of the function, I want to receive an error when the input is invalid.

#### Acceptance criteria

- CA03: WHEN the input is null, THE SYSTEM SHALL return a validation error.
- CA04: WHEN the input is empty after normalization, THE SYSTEM SHALL return a validation error.
