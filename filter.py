"""금칙어·단정 필터"""
import re
from postprocess.verify import Issue

BANNED_RULES = [
    (r'반드시\s*(합격|당첨|성공|결혼|이혼|사망)', "critical","단정"),
    (r'100\s*%\s*(보장|확실|성공|당첨)', "critical","보장"),
    (r'(암|당뇨|심장병|뇌졸중|치매)\s*(이다|확정|진단|발병)', "critical","질병단정"),
    (r'수익\s*(률|금)?\s*\d+\s*%', "critical","수익보장"),
    (r'죽을\s*(수|것|운)', "critical","공포"),
    (r'무조건\s*(이직|잔류|결혼|이혼)', "warning","단정"),
]

def filter_banned(output: str) -> tuple[str, list]:
    issues = []
    for pattern, level, desc in BANNED_RULES:
        for m in re.finditer(pattern, output):
            issues.append(Issue(level, "banned", f"{desc}: '{m.group(0)}'", m.group(0)))
        output = re.sub(pattern, "[표현 완화]", output)
    return output, issues