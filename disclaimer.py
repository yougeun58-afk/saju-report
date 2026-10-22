DISCLAIMERS = {
    "base": "본 리포트는 전통 명리학에 기반한 참고·오락용 해석이며, 의료·법률·투자 등 전문적 판단을 대체하지 않습니다.",
    "health": "건강 관련 내용은 진단이 아니며, 증상 시 의료기관 상담을 권합니다.",
    "invest": "재물 관련 내용은 투자 권유가 아니며, 수익을 보장하지 않습니다.",
}

def append_disclaimers(output: str, fs: dict) -> str:
    if DISCLAIMERS["base"][:10] in output:
        return output
    lines = [output, "", "─"*30, DISCLAIMERS["base"]]
    flags = fs["menu"]["flags"]
    if flags.get("health_disclaimer"): lines.append(DISCLAIMERS["health"])
    if flags.get("investment_disclaimer"): lines.append(DISCLAIMERS["invest"])
    return "\n".join(lines)