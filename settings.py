import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # DeepSeek 설정
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    LLM_BASE_URL = "https://api.deepseek.com"
    LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-flash")

    # 생성 파라미터
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "8000"))
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))

    # 검증/재생성
    MAX_REGEN = int(os.getenv("MAX_REGEN", "2"))

    # 운영 환경
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENV = os.getenv("ENV", "development")

settings = Settings()