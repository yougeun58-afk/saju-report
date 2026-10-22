"""수치·구조 검증"""
import re
from dataclasses import dataclass, field
from engine.constants import KOR2EN, HANJA2KOR

@dataclass
class Issue:
    level: str; category: str; message: str
    matched: str = ""; expected: str = ""

@dataclass
class VerifyResult:
    issues: list = field(default_factory=list)
    is_critical: bool = False

ELEMENT_PCT_PATTERN = re.compile(
    r'(목|화|토|금|수|木|火|土|金|水)\s*[\(（]?\s*(?:목|화|토|금|수|木|火|土|金|水)?\s*[\)）]?\s*(\d{1,3}(?:\.\d)?)\s*%'
)

def verify_element_pct(output, fs):
    issues = []
    elements = fs["elements"]["elements"]
    for m in ELEMENT_PCT_PATTERN.finditer(output):
        name = HANJA2KOR.get(m.group(1), m.group(1))
        val = float(m.group(2))
        expected = elements[KOR2EN[name]]["pct"]
        if abs(val - expected) > 0.1:
            issues.append(Issue("critical","number",f"오행 {name} 퍼센트 불일치",
                                m.group(0), f"{expected}%"))
    return issues

DAEWOON_AGE_PATTERN = re.compile(r'대운수?\s*(?:는|가|:)?\s*(\d{1,2}(?:\.\d{1,2})?)\s*(?:세|년|살)')

def verify_daewoon(output, fs):
    issues = []
    expected = fs["daewoon"]["start_age"]
    for m in DAEWOON_AGE_PATTERN.finditer(output):
        if abs(float(m.group(1)) - expected) > 0.1:
            issues.append(Issue("critical","number","대운수 불일치", m.group(0), f"{expected}세"))
    return issues

def verify_numbers(output, fs) -> VerifyResult:
    issues = verify_element_pct(output, fs) + verify_daewoon(output