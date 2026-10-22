"""오행 개수·퍼센트·막대 계산"""
from engine.constants import STEM_ELEMENT, BRANCH_ELEMENT

def make_bar(pct: float) -> str:
    filled = round(pct / 10)
    return "█" * filled + "░" * (10 - filled)

def calc_elements(pillars: dict) -> dict:
    chars = []
    for pos in ("year","month","day","hour"):
        p = pillars.get(pos)
        if p:
            chars.append(p["stem"])
            chars.append(p["branch"])

    total = len(chars)
    counts = {"wood":0,"fire":0,"earth":0,"metal":0,"water":0}
    for c in chars:
        el = STEM_ELEMENT.get(c) or BRANCH_ELEMENT.get(c)
        counts[el] += 1

    result = {}
    for el, cnt in counts.items():
        pct = round(cnt / total * 100, 1)
        result[el] = {"count": cnt, "pct": pct, "bar": make_bar(pct)}

    max_c = max(counts.values())
    min_c = min(counts.values())
    summary = {
        "total_chars": total,
        "strongest": [el for el,c in counts.items() if c == max_c],
        "weakest":   [el for el,c in counts.items() if c == min_c],
        "missing":   [el for el,c in counts.items() if c == 0],
        "excess":    [el for el,c in counts.items() if c >= total*0.375],
    }
    return {"elements": result, "summary": summary}