"""프롬프트 조립기: 블록 A + B + C"""
import json, os
from prompt.system_prompt import SYSTEM_PROMPT

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

def load_template(code: str) -> str:
    path = os.path.join(TEMPLATE_DIR, f"{code}.txt")
    if not os.path.exists(path):
        raise FileNotFoundError(f"템플릿 없음: {code}")
    with open(path, encoding="utf-8") as f:
        return f.read()

def build_prompt(fs: dict) -> list:
    factsheet_text = json.dumps(fs, ensure_ascii=False, indent=2)
    template = load_template(fs["menu"]["code"])

    user = f"""[블록 B: 팩트시트]
{factsheet_text}

[블록 C: 메뉴 지시문]
{template}

위 팩트시트의 수치와 간지를 절대 재계산하지 말고,
블록 C의 주제에만 집중하여 해석하라."""

    return [
        {"role": "system", "content": SYSTEM_PROMPT.strip()},
        {"role": "user", "content": user},
    ]

def build_retry_prompt(fs: dict, reason: str, prev_output: str) -> list:
    base = build_prompt(fs)
    base.append({"role": "assistant", "content": prev_output[:3000]})
    base.append({"role": "user", "content":
        f"위 출력에 다음 문제가 있었다: {reason}\n"
        "팩트시트의 수치와 간지만 사용하여 다시 작성하라. "
        "특히 오행 퍼센트·개수·대운수는 팩트시트 값을 그대로 인용하라."})
    return base