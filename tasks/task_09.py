def decide_change(cr: dict, state: dict) -> dict:
    # 1. Перевірка cr
    if not isinstance(cr, dict):
        raise ValueError("Некоректний запит: ?")

    cr_id = cr.get("id")
    allowed_types = {"problem", "extension", "external", "standards", "management"}
    cr_type = cr.get("type")
    impact_days = cr.get("impact_days")
    value = cr.get("value")

    is_valid_impact = (
        not isinstance(impact_days, bool)
        and isinstance(impact_days, int)
        and impact_days >= 0
    )
    is_valid_value = (
        not isinstance(value, bool)
        and isinstance(value, int)
        and 1 <= value <= 10
    )

    if (
        not cr_id
        or cr_type not in allowed_types
        or not is_valid_impact
        or not is_valid_value
    ):
        raise ValueError(f"Некоректний запит: {cr_id}")

    # 2. Перевірка state
    if not isinstance(state, dict):
        raise ValueError("Некоректний стан")

    reserve_days = state.get("reserve_days")
    if (
        isinstance(reserve_days, bool)
        or not isinstance(reserve_days, int)
        or reserve_days < 0
    ):
        raise ValueError("Некоректний стан")

    goal_at_risk = bool(state.get("goal_at_risk", False))
    emergency = bool(cr.get("emergency", False))
    mandatory_flag = bool(cr.get("mandatory", False))

    is_mandatory = mandatory_flag or (cr_type in {"standards", "management"})
    exceeds_reserve = impact_days > reserve_days
    left = max(0, reserve_days - impact_days)

    # 3. Правила ухвалення рішень
    # (1) Екстрений запит
    if emergency:
        return {
            "id": cr_id,
            "decision": "Затвердити",
            "reserve_after": left,
            "rebaseline": exceeds_reserve,
            "next_step": "Ретроспективний розгляд радою",
        }

    # (2) Обов'язковий запит
    if is_mandatory:
        next_step = (
            "Оновити базову лінію" if exceeds_reserve else "Виконати в межах резерву"
        )
        return {
            "id": cr_id,
            "decision": "Затвердити",
            "reserve_after": left,
            "rebaseline": exceeds_reserve,
            "next_step": next_step,
        }

    # (3) Мета під загрозою
    if goal_at_risk:
        return {
            "id": cr_id,
            "decision": "Відкласти",
            "reserve_after": reserve_days,
            "rebaseline": False,
            "next_step": "Розглянути на наступному плануванні",
        }

    # (4) Не виходить за резерв
    if not exceeds_reserve:
        if value >= 5:
            return {
                "id": cr_id,
                "decision": "Затвердити",
                "reserve_after": left,
                "rebaseline": False,
                "next_step": "Виконати в межах резерву",
            }
        else:
            return {
                "id": cr_id,
                "decision": "Відкласти",
                "reserve_after": reserve_days,
                "rebaseline": False,
                "next_step": "Повернути в беклог",
            }

    # (5) Виходить за резерв
    if value >= 8:
        return {
            "id": cr_id,
            "decision": "Відкласти",
            "reserve_after": reserve_days,
            "rebaseline": False,
            "next_step": "Узгодити з замовником нову базову лінію",
        }
    else:
        return {
            "id": cr_id,
            "decision": "Відхилити",
            "reserve_after": reserve_days,
            "rebaseline": False,
            "next_step": "Повідомити замовника",
        }