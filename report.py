"""엔드투엔드 파이프라인"""
import logging
from datetime import datetime

from engine.validator import validate_input, InputError
from engine.factsheet import compute_factsheet, EngineError
from prompt.builder import build_prompt, build_retry_prompt
from postprocess.verify import verify_numbers, verify_structure
from postprocess.filter import filter_banned
from postprocess.disclaimer import append_disclaimers
from postprocess.logger import log_attempt, log_escalation
from llm.client import call_llm_with_continuation
from config.settings import settings

logger = logging.getLogger("saju.pipeline")

def generate_report(raw_input: dict) -> dict:
    trace = {"started_at": datetime.now().isoformat(), "attempts": []}

    try:
        validated = validate_input(raw_input)
    except InputError as e:
        return {"ok": False, "error": "INPUT_INVALID", "detail": str(e), "trace": trace}

    try:
        fs = compute_factsheet(validated)
    except EngineError as e:
        return {"ok": False, "error": "ENGINE_FAILED", "detail": str(e), "trace": trace}

    trace["factsheet"] = {
        "pillars": {k:(v["stem"]+v["branch"] if v else None) for k,v in fs["pillars"].items()},
        "daewoon_start": fs["daewoon"]["start_age"],
        "direction": fs["daewoon"]["direction"],
        "missing": fs["elements"]["summary"]["missing"],
    }

    prompt = build_prompt(fs)
    last_output = ""

    for attempt in range(settings.MAX_REGEN + 1):
        raw = call_llm_with_continuation(prompt)
        last_output = raw

        nv = verify_numbers(raw, fs)
        filtered, banned = filter_banned(raw)
        st = verify_structure(filtered, fs)

        trace["attempts"].append({
            "attempt": attempt,
            "critical_numbers": sum(1 for i in nv.issues if i.level=="critical"),
            "banned": len(banned), "structure": len(st),
        })
        log_attempt(fs, attempt, nv, banned, st, "")

        all_issues = nv.issues + banned
        criticals = [i for i in all_issues if i.level == "critical"]

        if not criticals:
            trace["result"] = "PASS"
            trace["finished_at"] = datetime.now().isoformat()
            return {"ok": True, "report": append_disclaimers(filtered, fs), "trace": trace}

        if attempt >= settings.MAX_REGEN:
            log_escalation(fs, raw, criticals)
            trace["result"] = "ESCALATED"
            trace["finished_at"] = datetime.now().isoformat()
            return {"ok": True, "report": append_disclaimers(filter_banned(raw)[0], fs),
                    "escalated": True, "trace": trace}

        reason = "; ".join(i.message for i in criticals[:3])
        prompt = build_retry_prompt(fs, reason, last_output)

    return {"ok": False, "error": "UNREACHABLE", "trace": trace}