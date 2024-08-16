# File: .\open-llm-server_master\src\api\endpoints\metrics.py
from fastapi import APIRouter
import psutil

router = APIRouter()

@router.get("/metrics")
async def get_metrics():
    pass
