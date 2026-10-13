def choose_techniques(situation: dict) -> list[str]:
    if not isinstance(situation, dict):
        raise ValueError("Невідома мета: None")

    allowed_goals = {"order", "sprint", "release_date", "schedule", "agreement"}
    goal = situation.get("goal")
    if goal not in allowed_goals:
        raise ValueError(f"Невідома мета: {goal}")

    items = situation.get("items")
    if isinstance(items, bool) or not isinstance(items, int) or items < 1:
        raise ValueError("Некоректна кількість пунктів")

    history_sprints = situation.get("history_sprints", 0)
    has_dependencies = situation.get("has_dependencies", False)
    wants_probability = situation.get("wants_probability", False)
    disputed = situation.get("disputed", False)
    largest = situation.get("largest", None)

    if goal == "agreement":
        res = ["Дорожня карта"]
        if history_sprints >= 3:
            res.append("Швидкість із діапазоном")
        return res

    elif goal == "schedule":
        res = ["Три оцінки (PERT)"]
        if has_dependencies:
            res.append("Критичний шлях")
        return res

    elif goal == "release_date":
        if history_sprints < 3:
            return ["Спершу накопичити швидкість (щонайменше 3 спринти)"]
        res = ["Швидкість із діапазоном"]
        if wants_probability:
            res.append("Метод Монте-Карло")
        return res

    elif goal == "order":
        if items > 20:
            res = ["Розміри «футболок» (S, M, L)"]
            if disputed:
                res.append("Planning Poker для спірних пунктів")
            return res
        return ["Planning Poker"]

    elif goal == "sprint":
        res = ["Planning Poker"]
        if (
            largest is not None
            and not isinstance(largest, bool)
            and largest >= 13
        ):
            res.append("Розбити історії завбільвши 13 і більше")
        return res

    return []