"""lunar-python 연동 어댑터 (조자시 방식 적용)"""
from datetime import datetime, timedelta
from lunar_python import Solar, Lunar

def get_pillars(solar_dt: datetime, time_known: bool = True) -> dict:
    if not time_known:
        # 시간 모름 → 정오 기준으로 일주만 정확히 (시주는 None)
        solar = Solar.fromYmdHms(
            solar_dt.year, solar_dt.month, solar_dt.day, 12, 0, 0
        )
        lunar = solar.getLunar()
        ec = lunar.getEightChar()
        return {
            "year":  {"stem": ec.getYearGan(),  "branch": ec.getYearZhi()},
            "month": {"stem": ec.getMonthGan(), "branch": ec.getMonthZhi()},
            "day":   {"stem": ec.getDayGan(),   "branch": ec.getDayZhi()},
            "hour":  None,
        }

    # ★ 조자시(早子時) 적용: 23시 이후는 다음날로 계산
    effective_dt = solar_dt
    is_jojasi = solar_dt.hour >= 23
    if is_jojasi:
        effective_dt = solar_dt + timedelta(days=1)

    solar = Solar.fromYmdHms(
        effective_dt.year, effective_dt.month, effective_dt.day,
        effective_dt.hour, effective_dt.minute, 0
    )
    lunar = solar.getLunar()
    ec = lunar.getEightChar()

    pillars = {
        "year":  {"stem": ec.getYearGan(),  "branch": ec.getYearZhi()},
        "month": {"stem": ec.getMonthGan(), "branch": ec.getMonthZhi()},
        "day":   {"stem": ec.getDayGan(),   "branch": ec.getDayZhi()},
        "hour":  {"stem": ec.getTimeGan(),  "branch": ec.getTimeZhi()},
    }
    return pillars


def lunar_to_solar(date_str: str, is_leap: bool = False) -> datetime:
    """음력 → 양력 변환 (date_str: YYYY-MM-DD)"""
    y, m, d = map(int, date_str.split("-"))
    lunar = Lunar.fromYmd(y, -m if is_leap else m, d)  # 음수 월 = 윤달
    solar = lunar.getSolar()
    return datetime(solar.getYear(), solar.getMonth(), solar.getDay())


def get_jieqi_table(year: int) -> list:
    """해당 연도 24절기 절입 시각 [(datetime, name), ...] 오름차순"""
    lunar = Lunar.fromYmd(year, 6, 1)
    table = lunar.getJieQiTable()
    result = []
    for name, solar in table.items():
        dt = datetime(
            solar.getYear(), solar.getMonth(), solar.getDay(),
            solar.getHour(), solar.getMinute(), solar.getSecond()
        )
        result.append((dt, name))
    return sorted(result, key=lambda x: x[0])