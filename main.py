"""CLI: python main.py"""
import json, logging, sys
from pipeline.report import generate_report
from config.settings import settings

logging.basicConfig(level=settings.LOG_LEVEL,
                    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--example":
        raw = {
            "name":"홍길동","gender":"M","calendar":"solar",
            "birth_date":"1983-02-19","time":"14:30",
            "menu_code":"code-22",
        }
    else:
        print("사용법: python main.py --example")
        return

    result = generate_report(raw)
    if result["ok"]:
        print(result["report"])
        print("\n--- TRACE ---")
        print(json.dumps(result["trace"], ensure_ascii=False, indent=2))
    else:
        print(f"실패: {result['error']} — {result.get('detail','')}")

if __name__ == "__main__":
    main()