"""용신·희신 (억부 근사)"""
from engine.constants import STEM_ELEMENT, BRANCH_ELEMENT, SAENG, GEUK

def calc_strength(pillars: dict, elements: dict) -> dict:
    dm_el = STEM_ELEMENT[pillars["day"]["stem"]]
    saeng_me = next(k for k,v in SAENG.items() if v == dm_el)

    support = elements[dm_el]["count"] + elements[saeng_me]["count"]
    total = sum(e["count"] for e in elements.values())

    month_el = BRANCH_ELEMENT[pillars["month"]["branch"]]
    deukryeong = (month_el == dm_el or month_el == saeng_me)
    if deukryeong:
        support += 1.5

    ratio = support / total
    strength = "신강" if ratio >= 0.6 else ("신약" if ratio <= 0.4 else "중화")
    return {"strength": strength, "support_ratio": round(ratio,2),
            "deukryeong": deukryeong}

def calc_yongsin(pillars: dict, elements: dict) -> dict:
    info = calc_strength(pillars, elements)
    dm_el = STEM_ELEMENT[pillars["day"]["stem"]]
    saeng_me = next(k for k,v in SAENG.items() if v == dm_el)

    if info["strength"] == "신강":
        yongsin, heesin, gisin = SAENG[dm_el], GEUK[dm_el], saeng_me
    elif info["strength"] == "신약":
        yongsin, heesin, gisin = saeng_me, dm_el, GEUK[dm_el]
    else:
        yongsin, heesin, gisin = dm_el, SAENG[dm_el], GEUK[dm_el]

    return {**info, "yongsin": yongsin, "heesin": heesin, "gisin": gisin}