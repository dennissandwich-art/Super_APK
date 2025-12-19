# validators.py
# BRANCH: main
# ROLE: Pure validators (NO SIDE EFFECTS)

def is_non_empty_string(value) -> bool:
    return isinstance(value, str) and len(value.strip()) > 0

def is_positive_int(value) -> bool:
    return isinstance(value, int) and value > 0
