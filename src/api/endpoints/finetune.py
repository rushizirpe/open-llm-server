# src/api/endpoints/fine_tune.py

import os
import json
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from src.models.ml_models import fine_tune_model
from src.core.logging import logger
from src.core.config import settings

router = APIRouter()

class FineTuneInput(BaseModel):
    model: str
    train_file: str
    validation_file: Optional[str] = None
    num_train_epochs: int = 3
    learning_rate: float = 2e-5
    batch_size: int = 8
    output_dir: str = "fine_tuned_model"

def get_job_id():
    return f"job_{len(os.listdir(settings.JOB_DIR)) + 1}"

def save_job_status(job_id: str, status: str):
    with open(os.path.join(settings.JOB_DIR, f"{job_id}.json"), "w") as f:
        json.dump({"status": status}, f)
        
@router.get("/status/{job_id}")
async def get_fine_tune_status(job_id: str):
    try:
        with open(os.path.join(settings.JOB_DIR, f"{job_id}.json"), "r") as f:
            status = json.load(f)
        return {"status": status["status"], "job_id": job_id}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Error reading status for job {job_id}")