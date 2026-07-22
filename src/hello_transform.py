def normalize_text(value: str) -> str:
    """Normalize a text value according to the example sdd spec.

    Covered criteria:
    - CA01: valid text is returned normalized
    - CA02: leading/trailing spaces are removed
    """
    if value is None:
        raise ValueError("value cannot be None")
    if not isinstance(value, str):
        raise ValueError("value must be a string")
    result = value.strip()
    if not result:
        raise ValueError("value cannot be empty")
    return result
