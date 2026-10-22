"""신살 판정 (삼합 기반 + 천을귀인)"""
from engine.constants import SAMHAP, SAMHAP_SINSAL, CHEONEUL

def detect_samhap_sinsal(pillars: dict) -> list:
    results = []
    base_branches = {"year": pillars["year"]["branch"], "day": pillars["day"]["branch"]}
    targets = {k: v["branch"] for k,v in pillars.items() if v}

    for base_name, base_br in base_branches.items():
        group = SAMHAP.get(base_br)
        if not group:
            continue
        for sal_name, sal_br in SAMHAP_SINSAL[group].items():
            for pos, br in targets.items():
                if br == sal_br:
                    results.append({"name": sal_name, "present": True,
                                    "base": base_name, "location": pos})
    return results

def detect_cheoneul(pillars: dict) -> list:
    day_stem = pillars["day"]["stem"]
    targets = [v["branch"] for v in pillars.values() if v]
    hits = [b for b in CHEONEUL.get(day_stem, []) if b in targets]
    return [{"name":"천을귀인","present":True,"branch":b} for b in hits] or \
           [{"name":"천을귀인","present":False}]

def detect_sinsal(pillars: dict) -> list:
    all_s = detect_samhap_sinsal(pillars) + detect_cheoneul(pillars)
    seen, uniq = set(), []
    for s in all_s:
        key = (s["name"], s.get("location"))
        if key not in seen:
            seen.add(key)
            uniq.append(s)
    return uniq