"""LLM 호출 레이어 — OpenAI SDK로 DeepSeek API 연동"""
from openai import OpenAI
from config.settings import settings

# DeepSeek는 OpenAI SDK와 호환되므로 base_url과 model만 교체
client = OpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url=settings.LLM_BASE_URL,   # https://api.deepseek.com
)

def call_llm(messages: list) -> tuple[str, str]:
    """단일 호출, (내용, finish_reason) 반환"""
    resp = client.chat.completions.create(
        model=settings.LLM_MODEL,      # deepseek-flash
        messages=messages,
        max_tokens=settings.LLM_MAX_TOKENS,
        temperature=settings.LLM_TEMPERATURE,
    )
    choice = resp.choices[0]
    return choice.message.content, choice.finish_reason

def call_llm_with_continuation(prompt: list, max_rounds: int = 3) -> str:
    """max_tokens로 잘렸을 때 이어쓰기 지원"""
    parts = []
    messages = prompt

    for _ in range(max_rounds):
        content, finish = call_llm(messages)
        parts.append(content)

        if finish != "length":
            break

        # 잘렸으면 마지막 문장부터 이어서 쓰게 함
        messages = prompt + [
            {"role": "assistant", "content": "".join(parts)},
            {
                "role": "user",
                "content": "직전 문장의 마지막 단어부터 정확히 이어서 집필하라. 인사·요약 반복 금지.",
            },
        ]

    return "".join(parts)