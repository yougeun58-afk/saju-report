"""천간·지지·오행·신살 상수"""

STEMS    = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
BRANCHES = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

STEM_ELEMENT = {
    "甲":"wood","乙":"wood","丙":"fire","丁":"fire",
    "戊":"earth","己":"earth","庚":"metal","辛":"metal",
    "壬":"water","癸":"water",
}
STEM_YINYANG = {
    "甲":"yang","乙":"yin","丙":"yang","丁":"yin","戊":"yang",
    "己":"yin","庚":"yang","辛":"yin","壬":"yang","癸":"yin",
}
BRANCH_ELEMENT = {
    "子":"water","丑":"earth","寅":"wood","卯":"wood",
    "辰":"earth","巳":"fire","午":"fire","未":"earth",
    "申":"metal","酉":"metal","戌":"earth","亥":"water",
}
YANG_STEMS = {"甲","丙","戊","庚","壬"}

# 삼합국
SAMHAP = {
    "寅":"fire","午":"fire","戌":"fire",
    "申":"water","子":"water","辰":"water",
    "巳":"metal","酉":"metal","丑":"metal",
    "亥":"wood","卯":"wood","未":"wood",
}
SAMHAP_SINSAL = {
    "fire":  {"도화":"卯","역마":"申","화개":"戌"},
    "water": {"도화":"酉","역마":"寅","화개":"辰"},
    "metal": {"도화":"午","역마":"亥","화개":"丑"},
    "wood":  {"도화":"子","역마":"巳","화개":"未"},
}

# 천을귀인 (일간 기준)
CHEONEUL = {
    "甲":["丑","未"], "乙":["子","申"], "丙":["亥","酉"],
    "丁":["亥","酉"], "戊":["丑","未"], "己":["子","申"],
    "庚":["丑","未"], "辛":["寅","午"], "壬":["卯","巳"],
    "癸":["卯","巳"],
}

# 상생·상극
SAENG = {"wood":"fire","fire":"earth","earth":"metal",
         "metal":"water","water":"wood"}
GEUK  = {"wood":"earth","earth":"water","water":"fire",
         "fire":"metal","metal":"wood"}

KOR2EN = {"목":"wood","화":"fire","토":"earth","금":"metal","수":"water"}
EN2KOR = {v:k for k,v in KOR2EN.items()}
HANJA2KOR = {"木":"목","火":"화","土":"토","金":"금","水":"수"}


def ganzi_index(stem: str, branch: str) -> int:
    s, b = STEMS.index(stem), BRANCHES.index(branch)
    for i in range(60):
        if i % 10 == s and i % 12 == b:
            return i
    raise ValueError(f"유효하지 않은 간지: {stem}{branch}")