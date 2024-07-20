from typing import List, Union
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import os
import numpy as np
import base64
import logging
import tensorflow as tf


# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Get Hugging Face token set as an environment variable
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

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
        logging.debug(f"Loading tokenizer and model for {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=HUGGING_FACE_TOKEN)
        model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=HUGGING_FACE_TOKEN)
        if torch.cuda.is_available():
            model.to('cuda')
        model_cache[model_name] = (tokenizer, model)
    return model_cache[model_name]

def generate_embeddings(inputs: List[str], model_name: str):
    logging.debug(f"Generating embeddings for model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=HUGGING_FACE_TOKEN)
    model = AutoModel.from_pretrained(model_name, trust_remote_code=True, use_auth_token=HUGGING_FACE_TOKEN)
    if torch.cuda.is_available():
        model.to('cuda')

    embeddings = []
    for i, text in enumerate(inputs):
        if not isinstance(text, str):
            logging.warning(f"Invalid input type at index {i}: {text} (type: {type(text)}). Converting to string.")
            text = str(text)
        logging.debug(f"Processing input {i}: {text}")
        tokenized_inputs = tokenizer(text, return_tensors="pt")
        if torch.cuda.is_available():
            tokenized_inputs = {key: val.to('cuda') for key, val in tokenized_inputs.items()}

        with torch.no_grad():
            outputs = model(**tokenized_inputs)
            pooled_output = outputs.last_hidden_state[:, 0, :]

        if pooled_output.shape[0] == 0:  
            logging.warning(f"No valid embeddings for input {i}")
            continue

        embedding = pooled_output.squeeze().cpu().numpy()
        try:
            embedding_list = embedding.tolist()
        except TypeError:  
            base64_encoded = base64.b64encode(embedding).decode('utf-8')
            embedding_list = base64.b64decode(base64_encoded)
            embedding_list = np.frombuffer(embedding_list, dtype=np.float32).tolist()

        embeddings.append({"embedding": embedding_list, "index": i})

    return embeddings

@app.post("/v1/embeddings")
async def create_embeddings(data: dict):
    try:
        inputs = data["input"]
        model_name = data["model"]
        
        # Convert all inputs to strings
        if isinstance(inputs, list):
            inputs = [str(input) for input in inputs]
        else:
            inputs = [str(inputs)]

        logging.debug(f"Received embedding request for model: {model_name} with inputs: {inputs}")

        embeddings = generate_embeddings(inputs, model_name)
        usage = {"total_tokens": sum([len(input_text.split()) for input_text in inputs])}

        logging.debug(f"Embeddings generated successfully: {embeddings}")

        return {
            "object": "list",
            "data": embeddings,
            "model": model_name,
            "usage": usage
        }
    except Exception as e:
        logging.error(f"Error generating embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

class ChatCompletionInput(BaseModel):
    model: str
    messages: List[dict]
    max_tokens: int = 150
    temperature: float = 1.0
    top_p: float = 1.0
    n: int = 1
    stop: Union[str, List[str], None] = None

@app.post("/v1/chat/completions")
async def create_chat_completion(data: ChatCompletionInput):
    try:
        logging.debug(f"Received chat completion request for model: {data.model}")

        tokenizer, model = get_model_and_tokenizer(data.model)
        conversation = ""
        for message in data.messages:
            role = message['role']
            content = message['content']
            prefix = "User: " if role == "user" else "Assistant: "
            conversation += prefix + content + "\n"

        input_ids = tokenizer.encode(conversation, return_tensors="pt")
        if torch.cuda.is_available():
            input_ids = input_ids.to('cuda')
        outputs = model.generate(
            input_ids,
            max_length=data.max_tokens + input_ids.shape[1],
            temperature=data.temperature,
            top_p=data.top_p,
            num_return_sequences=data.n,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            do_sample=True
        )

        responses = []
        for i in range(data.n):
            response_text = tokenizer.decode(outputs[i], skip_special_tokens=True)
            response_text = response_text[len(conversation):] 
            responses.append({"index": i, "text": response_text})

        logging.debug(f"Chat completion generated successfully: {responses}")

        return {"choices": responses}
    except Exception as e:
        logging.error(f"Error generating chat completion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
