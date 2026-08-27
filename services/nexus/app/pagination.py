import base64
import json
from dataclasses import dataclass


class InvalidCursorError(ValueError):
    pass


@dataclass(frozen=True)
class Cursor:
    value: str
    resource_id: str


def encode_cursor(value: str, resource_id: str) -> str:
    payload = json.dumps({"value": value, "id": resource_id}, separators=(",", ":"))
    return base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")


def decode_cursor(token: str) -> Cursor:
    try:
        padded = token + "=" * (-len(token) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded).decode())
        value = payload["value"]
        resource_id = payload["id"]
        if not isinstance(value, str) or not isinstance(resource_id, str):
            raise TypeError
        return Cursor(value=value, resource_id=resource_id)
    except (ValueError, TypeError, KeyError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InvalidCursorError("The cursor is invalid.") from exc
