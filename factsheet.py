"""팩트시트 조립 — 모든 엔진 모듈 통합"""
from datetime import datetime
from engine.validator import validate_input
from engine.lunar_adapter import get_pillars, lunar_to_solar, get_jieqi_table
from engine.elements import calc_elements
from engine.daewoon import calc_daewoon
from engine.sinsal import detect_sinsal
from engine.yongsin import calc_yongsin
from engine.relations import detect_relations, calc_gongmang
from config.menus import load_menu_meta

class EngineError(Exception):
    pass

def compute_factsheet(v: dict) -> dict:
    try:
        # 1) 양력 정규화
        if v["calendar"] == "lunar":
            solar_dt = lunar_to_solar(v["birth_date"], v["is_leap_month"])
        else:
            y, m, d = map(int, v["birth_date"].split("-"))
            hh, mm = (map(int, v["time"].split(":")) if v["time_known"] else (12, 0))
            solar_dt = datetime(y, m, d, hh, mm)

        # 2) 사주 4주
        pillars = get_pillars(solar_dt, v["time_known"])

        # 3) 오행
        el = calc_elements(pillars)

        # 4) 용신
        yong = calc_yongsin(pillars, el["elements"])

        # 5) 대운
        jieqi = get_jieqi_table(solar_dt.year)
        dw = calc_daewoon(solar_dt, v["gender"], pillars["year"]["stem"],
                          pillars["month"], jieqi)

        # 6) 세운 (올해)
        this_year = datetime.now().year
        sewoon_pillars = get_pillars(datetime(this_year, 6, 1))
        sewoon = {"year": this_year,
                  "pillar": sewoon_pillars["year"]["stem"] + sewoon_pillars["year"]["branch"],
                  "stem": sewoon_pillars["year"]["stem"],
                  "branch": sewoon_pillars["year"]["branch"]}

        # 7) 신살·합충·공망
        sinsal = detect_sinsal(pillars)
        relations = detect_relations(pillars)
        gongmang = calc_gongmang(pillars["day"])

        # 8) 메뉴
        menu = load_menu_meta(v["menu_code"])

        age = (datetime.now() - solar_dt).days // 365
        total_chars = el["summary"]["total_chars"]

        return {
            "schema_version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "customer": {"name": v["name"], "gender": v["gender"], "age": age},
            "birth": {
                "calendar_input": v["calendar"],
                "is_leap_month": v["is_leap_month"],
                "solar_date": solar_dt.strftime("%Y-%m-%d"),
                "time_known": v["time_known"],
                "input_time": v["time"],
                "corrected_time": v["time"],  # 진태양시 보정은 이후 확장
                "birth_place": v["birth_place"],
            },
            "mode": {"pillar_count": 4 if v["time_known"] else 3,
                     "is_three_pillar": not v["time_known"]},
            "pillars": pillars,
            "day_master": {"stem": pillars["day"]["stem"]},
            "elements": el,
            "yongsin": yong,
            "daewoon": dw,
            "sewoon": sewoon,
            "sinsal": sinsal,
            "relations": relations,
            "gongmang": gongmang,
            "menu": menu,
        }
    except Exception as e:
        raise EngineError(f"팩트시트 계산 실패: {e}")