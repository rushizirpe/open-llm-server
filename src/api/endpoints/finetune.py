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

def get_job_id():
    return f"job_{len(os.listdir(settings.JOB_DIR)) + 1}"