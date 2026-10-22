"""FastAPI 웹 서버 (Vercel 배포 최적화)"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os

from pipeline.report import generate_report
from config.menus import MENU_DB

app = FastAPI(title="사주 리포트 API")

# Vercel 환경에 맞춰 현재 작업 디렉토리(cwd) 기준으로 static 폴더 지정
STATIC_DIR = os.path.join(os.getcwd(), "static")

class ReportRequest(BaseModel):
    name: str
    gender: str          # "M" or "F"
    calendar: str        # "solar" or "lunar"
    birth_date: str      # "YYYY-MM-DD"
    time: Optional[str] = None   # "HH:MM" or None
    is_leap_month: bool = False
    menu_code: str


# ── 정적 페이지 라우트 ────────────────────────────
@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/terms.html")
def terms():
    return FileResponse(os.path.join(STATIC_DIR, "terms.html"))

@app.get("/privacy.html")
def privacy():
    return FileResponse(os.path.join(STATIC_DIR, "privacy.html"))

@app.get("/refund.html")
def refund():
    return FileResponse(os.path.join(STATIC_DIR, "refund.html"))


# ── API 라우트 ───────────────────────────────────
@app.get("/api/menus")
def get_menus():
    """메뉴 목록 반환 (프론트엔드 드롭다운용)"""
    return [
        {"code": code, "title": info["title"]}
        for code, info in MENU_DB.items()
    ]


@app.post("/api/report")
def create_report(req: ReportRequest):
    raw = {
        "name": req.name,
        "gender": req.gender,
        "calendar": req.calendar,
        "birth_date": req.birth_date,
        "time": req.time,
        "is_leap_month": req.is_leap_month,
        "menu_code": req.menu_code,
    }
    result = generate_report(raw)
    if not result["ok"]:
        raise HTTPException(status_code=400, detail=result.get("detail", result["error"]))
    return {"report": result["report"], "trace": result["trace"]}