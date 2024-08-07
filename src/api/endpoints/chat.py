from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Union
from src.models.ml_models import get_model_and_tokenizer
from src.core.logging import logger
import torch

router = APIRouter()

class ChatCompletionInput(BaseModel):
    model: str
    messages: List[dict]
    max_tokens: int = 150
    temperature: float = 1.0
    top_p: float = 1.0
    n: int = 1
    stop: Union[str, List[str], None] = None

@router.post("/completions")
async def create_chat_completion(data: ChatCompletionInput):
    try:
        logger.debug(f"Received chat completion request for model: {data.model}")

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

        logger.debug(f"Chat completion generated successfully: {responses}")

        return {"choices": responses}
    except Exception as e:
        logger.error(f"Error generating chat completion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))