from fractions import Fraction
import math

PHASE_MULTIPLIERS = {
    "ідея": (Fraction(1, 4), Fraction(4, 1)),
    "визначення продукту": (Fraction(1, 2), Fraction(2, 1)),
    "вимоги": (Fraction(2, 3), Fraction(3, 2)),
    "інтерфейс": (Fraction(4, 5), Fraction(5, 4)),
    "проєктування": (Fraction(9, 10), Fraction(11, 10)),
}


def estimate_ranges(items: list[tuple[str, int, str]]) -> dict:
    if not isinstance(items, list) or len(items) == 0:
        raise ValueError("Порожній список")

    ranges = []
    total_low = 0
    total_high = 0
    widest_item = None
    max_diff = -1

    for item in items:
        name, estimate, phase_raw = item

        # Оцінка: ціле число > 0, bool не підходить
        if isinstance(estimate, bool) or not isinstance(estimate, int) or estimate <= 0:
            raise ValueError(f"Некоректна оцінка: {name}")

        normalized_phase = phase_raw.strip().lower()
        if normalized_phase not in PHASE_MULTIPLIERS:
            raise ValueError(f"Невідома фаза: {phase_raw}")

        low_mult, high_mult = PHASE_MULTIPLIERS[normalized_phase]

        low_bound = math.floor(estimate * low_mult)
        high_bound = math.ceil(estimate * high_mult)

        ranges.append((name, low_bound, high_bound))
        total_low += low_bound
        total_high += high_bound

        diff = high_bound - low_bound
        if diff > max_diff:
            max_diff = diff
            widest_item = name

    return {
        "ranges": ranges,
        "total": (total_low, total_high),
        "widest": widest_item,
    }