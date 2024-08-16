# File: .\open-llm-server_master\src\api\endpoints\metrics.py
from fastapi import APIRouter
import psutil

router = APIRouter()

@router.get("/metrics")
async def get_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    
    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage
    }
