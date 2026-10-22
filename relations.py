"""합충형파해·공망 (기본 구현)"""
from engine.constants import BRANCHES

# 육합
YUKHAP = {("子","丑"),("寅","亥"),("卯","戌"),("辰","酉"),("巳","申"),("午","未")}
# 충
CHUNG = {("子","午"),("丑","未"),("寅","申"),("卯","酉"),("辰","戌"),("巳","亥")}

def detect_relations(pillars: dict) -> dict:
    branches = {k: v["branch"] for k,v in pillars.items() if v}
    positions = list(branches.items())
    hap, chung = [], []

    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            p1, b1 = positions[i]
            p2, b2 = positions[j]
            pair = tuple(sorted([b1, b2]))
            if any(set(pair) == set(h) for h in YUKHAP):
                hap.append(f"{p1}-{p2}")
            if any(set(pair) == set(c) for c in CHUNG):
                chung.append(f"{p1}-{p2}")

    return {"hap": hap, "chung": chung, "hyeong": [], "pa": [], "hae": []}

def calc_gongmang(day_pillar: dict) -> list:
    """일주 기준 공망 (60갑자 순환)"""
    from engine.constants import STEMS, BRANCHES
    s_idx = STEMS.index(day_pillar["stem"])
    b_idx = BRANCHES.index(day_pillar["branch"])
    # 공망: 일주 순(旬)에서 빠진 2지
    xun_start = (b_idx - s_idx) % 12
    return [BRANCHES[(xun_start + 10) % 12], BRANCHES[(xun_start + 11) % 12]]