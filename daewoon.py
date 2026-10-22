"""대운 계산 (3일=1년 규칙)"""
from datetime import datetime
from engine.constants import STEMS, BRANCHES, YANG_STEMS, ganzi_index


def determine_direction(year_stem: str, gender: str) -> str:
    is_yang = year_stem in YANG_STEMS
    if is_yang and gender == "M":
        return "forward"
    if is_yang and gender == "F":
        return "reverse"
    if not is_yang and gender == "M":
        return "reverse"
    return "forward"


def days_to_jieqi(birth_dt: datetime, direction: str, jieqi_table: list) -> float:
    if direction == "forward":
        for dt, _ in jieqi_table:
            if dt > birth_dt:
                return (dt - birth_dt).total_seconds() / 86400
    else:
        for dt, _ in reversed(jieqi_table):
            if dt < birth_dt:
                return (birth_dt - dt).total_seconds() / 86400
    raise ValueError("절입일 탐색 실패")


def calc_daewoon(birth_dt, gender, year_stem, month_pillar, jieqi_table, count=10) -> dict:
    direction = determine_direction(year_stem, gender)
    days = days_to_jieqi(birth_dt, direction, jieqi_table)

    # 대운수: 3일=1년, 소수 첫째 자리 반올림, 최소 1세
    raw_age = days / 3.0
    start_age = max(1.0, round(raw_age, 1))

    base_idx = ganzi_index(month_pillar["stem"], month_pillar["branch"])
    step = 1 if direction == "forward" else -1

    lst = []
    for i in range(1, count + 1):
        idx = (base_idx + step * i) % 60
        start = int(start_age) + (i - 1) * 10
        lst.append({
            "index": i,
            "start_age": start,
            "end_age": start + 9,
            "pillar": STEMS[idx % 10] + BRANCHES[idx % 12],
        })

    current_age = (datetime.now() - birth_dt).days // 365
    current_idx = next(
        (d["index"] for d in lst if d["start_age"] <= current_age <= d["end_age"]),
        None
    )

    return {
        "start_age": start_age,
        "direction": direction,
        "list": lst,
        "current_index": current_idx,
    }