
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


model_cache = {}

def get_model_and_tokenizer(model_name: str):
    if model_name not in model_cache:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        model_cache[model_name] = (tokenizer, model)
    return model_cache[model_name]

def generate_embeddings(inputs: List[str], model_name: str):
    # Load the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name, trust_remote_code=True)

    embeddings = []
    for i, text in enumerate(inputs):
        # Tokenize the input text
        tokenized_inputs = tokenizer(text, return_tensors="pt")

        # Generate embeddings
        with torch.no_grad():
            outputs = model(**tokenized_inputs)
            pooled_output = outputs.last_hidden_state[:, 0, :]  

        # Convert embeddings to list format
        embedding = pooled_output.squeeze().tolist()
        embeddings.append({"embedding": embedding, "index": i})

    return embeddings

@app.post("/v1/embeddings")
async def create_embeddings(data: dict):
    try:
        inputs = data["input"] if isinstance(data["input"], list) else [data["input"]]
        model_name = data["model"]

        # Generate embeddings
        embeddings = generate_embeddings(inputs, model_name)

        # Calculate usage metrics
        usage = {"total_tokens": sum([len(input_text.split()) for input_text in inputs])}

        return {
            "object": "list",
            "data": embeddings,
            "model": model_name,
            "usage": usage
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
