import re


def screen_request(text: str) -> dict:
    if not isinstance(text, str):
        raise ValueError("Запит має бути рядком")
    if not text.strip():
        raise ValueError("Порожній запит")
    if len(text) > 4000:
        raise ValueError("Запит задовгий")

    secret_rules = [
        ("ключ API", re.compile(r"\b(?:sk|pk)_(?:live|test)_[A-Za-z0-9]{16,}\b")),
        ("токен GitHub", re.compile(r"\bghp_[A-Za-z0-9]{36}\b")),
        ("приватний ключ", re.compile(r"BEGIN [A-Z ]*PRIVATE")),
        (
            "пароль",
            re.compile(
                r"\b(?:password|passwd|пароль)\s*[:=]\s*\S+", re.IGNORECASE
            ),
        ),
    ]

    found_secrets = []
    for name, pattern in secret_rules:
        if pattern.search(text):
            found_secrets.append(name)

    if found_secrets:
        return {
            "action": "block",
            "found": found_secrets,
            "text": None,
            "replaced": 0,
        }

    redact_rules = [
        ("картка", "[КАРТКА]", re.compile(r"(?<!\d)(?:\d{4}[ -]){3}\d{4}(?!\d)")),
        ("телефон", "[ТЕЛЕФОН]", re.compile(r"(?<![\d+])(?:\+38)?0\d{9}(?!\d)")),
        ("email", "[EMAIL]", re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")),
        (
            "внутрішній ідентифікатор",
            "[ВНУТР_ID]",
            re.compile(r"\bPRJ-\d{3,}\b"),
        ),
    ]

    current_text = text
    total_replaced = 0
    found_redacts = []

    for name, placeholder, pattern in redact_rules:
        matches = pattern.findall(current_text)
        count = len(matches)
        if count > 0:
            found_redacts.append(name)
            total_replaced += count
            current_text = pattern.sub(placeholder, current_text)

    return {
        "action": "redact" if total_replaced > 0 else "allow",
        "found": found_redacts,
        "text": current_text,
        "replaced": total_replaced,
    }