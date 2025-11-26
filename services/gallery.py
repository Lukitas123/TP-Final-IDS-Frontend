import json


def safe_parse_gallery(value):
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except ValueError:
            return []
    return []
