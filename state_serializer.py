# state_serializer.py
# BRANCH: main
# ROLE: State serialization (NO DISK)

import json


def serialize(state: dict) -> str:
    return json.dumps(state)


def deserialize(blob: str) -> dict:
    return json.loads(blob)
