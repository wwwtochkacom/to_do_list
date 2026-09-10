def validate_patch(data: dict) -> str | None:
    mapping = ["title", "description", "status", "date"]
    for key, value in data.items():
        if key in mapping:
            if type(value) is str and type(key) is str:
                continue
            else:
                return None
        else:
            return None
    return "Успешно"


def validate_put(data: dict):
    mapping = ["title", "description", "status", "date"]
    if set(data.keys()) == set(mapping):
        for key, value in data.items():
            if isinstance(value, str):
                continue
            else:
                return None
        return "Успешно"
    else:
        return None
