
from typing import List, Union, Any, Dict
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import tensorflow as tf
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import torch
import os
import time
import uuid


# Set the model repository and file
GENERATIVE_AI_MODEL_REPO = "TheBloke/Llama-2-7B-GGUF"
GENERATIVE_AI_MODEL_FILE = "llama-2-7b.Q4_K_M.gguf"

# Download the model file
model_path = hf_hub_download(
    repo_id=GENERATIVE_AI_MODEL_REPO,
    filename=GENERATIVE_AI_MODEL_FILE
)

# Load the model
llama2_model = Llama(
    model_path=model_path,
    n_gpu_layers=64,
    n_ctx=2000
)

# Test an inference
# print(llama2_model(prompt="Hello ", max_tokens=10))


app = FastAPI()

@app.get("/")
def status_gpu_check():
    gpus = tf.config.list_physical_devices('GPU')
    gpu_msg = "Unavailable"
    gpu_details = {}

    if gpus:
        gpu_msg = "Available"
        for i, gpu in enumerate(gpus):
            gpu_details[f"GPU {i}"] = tf.config.experimental.get_device_details(gpu)
    
    return {
        "status": "System Status: Operational",
        "gpu": gpu_msg,
        "gpu_details": gpu_details
    }

