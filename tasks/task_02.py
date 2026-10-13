import re

FIBONACCI_SCALE = {1, 2, 3, 5, 8, 13, 21}


def check_ready(story: dict) -> dict:
    if not isinstance(story, dict):
        raise ValueError("Некоректна історія")

    problems = []

    # (1) Шаблон
    text = story.get("text")
    template_pattern = r"^Як\s+\S.*,\s*я хочу\s+\S.*,\s*щоб\s+\S.*$"
    if not isinstance(text, str) or not re.match(
        template_pattern, text.strip(), re.DOTALL
    ):
        problems.append("немає шаблону «Як..., я хочу..., щоб...»")

    # (2) Критерії прийняття
    criteria = story.get("criteria")
    count_criteria = 0
    if isinstance(criteria, list):
        for c in criteria:
            if isinstance(c, str) and c.strip():
                count_criteria += 1

    if count_criteria < 3:
        problems.append(f"критеріїв прийняття менше трьох: {count_criteria}")

    # (3) Оцінка
    points = story.get("points")
    if points is None:
        problems.append("немає оцінки")
    elif isinstance(points, bool) or not isinstance(points, int):
        problems.append(f"оцінка {points} не зі шкали Фібоначчі")
    elif points not in FIBONACCI_SCALE:
        problems.append(f"оцінка {points} не зі шкали Фібоначчі")
    elif points in (13, 21):
        problems.append(f"історія завелика ({points}): розбийте її")

    # (4) Залежності
    dependencies = story.get("dependencies")
    if dependencies is not None and isinstance(dependencies, list):
        for dep in dependencies:
            if isinstance(dep, dict) and dep.get("resolved") is not True:
                name = dep.get("name", "")
                problems.append(f"залежність {name} не вирішена")

    ready = len(problems) == 0
    verdict = (
        "Готова до планування" if ready else "Повернути власнику продукту"
    )

    return {"ready": ready, "problems": problems, "verdict": verdict}