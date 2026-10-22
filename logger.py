import json, logging
from datetime import datetime

logger = logging.getLogger("saju.validation")

def log_attempt(fs, attempt, num_verify, banned_issues, struct_issues, reason):
    record = {
        "ts": datetime.now().isoformat(),
        "menu": fs["menu"]["code"],
        "attempt": attempt,
        "number_issues": len(num_verify.issues),
        "critical_numbers": sum(1 for i in num_verify.issues if i.level=="critical"),
        "banned_issues": len(banned_issues),
        "structure_issues": len(struct_issues),
        "regen_reason": reason,
    }
    logger.info(json.dumps(record, ensure_ascii=False))

def log_escalation(fs, output, criticals):
    logger.warning(json.dumps({
        "ts": datetime.now().isoformat(),
        "menu": fs["menu"]["code"],
        "escalation": True,
        "criticals": [i.message for i in criticals],
    }, ensure_ascii=False))