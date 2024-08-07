from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel
import torch
import numpy as np
import base64
from src.core.config import settings
from src.core.logging import logger
from typing import List

model_cache = {}

def get_model_and_tokenizer(model_name: str):
    if model_name not in model_cache:
        logger.debug(f"Loading tokenizer and model for {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=settings.HUGGING_FACE_TOKEN)
        model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=settings.HUGGING_FACE_TOKEN)
        if torch.cuda.is_available():
            model.to('cuda')
        model_cache[model_name] = (tokenizer, model)
    return model_cache[model_name]

def generate_embeddings(inputs: List[str], model_name: str):
    logger.debug(f"Generating embeddings for model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=settings.HUGGING_FACE_TOKEN)
    model = AutoModel.from_pretrained(model_name, trust_remote_code=True, use_auth_token=settings.HUGGING_FACE_TOKEN)
    if torch.cuda.is_available():
        model.to('cuda')

    embeddings = []
    for i, text in enumerate(inputs):
        if not isinstance(text, str):
            logger.warning(f"Invalid input type at index {i}: {text} (type: {type(text)}). Converting to string.")
            text = str(text)
        logger.debug(f"Processing input {i}: {text}")
        tokenized_inputs = tokenizer(text, return_tensors="pt")
        if torch.cuda.is_available():
            tokenized_inputs = {key: val.to('cuda') for key, val in tokenized_inputs.items()}

        with torch.no_grad():
            outputs = model(**tokenized_inputs)
            pooled_output = outputs.last_hidden_state[:, 0, :]

        if pooled_output.shape[0] == 0:  
            logger.warning(f"No valid embeddings for input {i}")
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