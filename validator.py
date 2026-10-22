"""입력 검증 레이어"""
from datetime import datetime

class InputError(Exception):
    pass

DEFAULT_KOREA = {"longitude": 126.98, "timezone_offset": 9}

def validate_input(raw: dict) -> dict:
    errors = []

    if not raw.get("name"):
        errors.append("성명 누락")
    if not raw.get("birth_date"):
        errors.append("생년월일 누락")
    if raw.get("calendar") not in ("solar", "lunar"):
        errors.append("양력/음력 구분 필수")
    if raw.get("gender") not in ("M", "F"):
        errors.append("성별 필수 (대운 순행/역행)")

    time_known = bool(raw.get("time"))
    if raw.get("calendar") == "lunar" and "is_leap_month" not in raw:
        errors.append("음력은 윤달 여부 필수")
    if not raw.get("menu_code"):
        errors.append("메뉴 코드 누락")

    if errors:
        raise InputError("; ".join(errors))

    return {
        "name": raw["name"],
        "gender": raw["gender"],
        "calendar": raw["calendar"],
        "is_leap_month": raw.get("is_leap_month", False),
        "birth_date": raw["birth_date"],
        "time": raw.get("time"),
        "time_known": time_known,
        "birth_place": raw.get("birth_place", DEFAULT_KOREA),
        "menu_code": raw["menu_code"],
    }