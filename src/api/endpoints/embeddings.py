from fastapi import APIRouter, HTTPException
from src.models.ml_models import generate_embeddings
from src.core.logging import logger

router = APIRouter()

@router.post("/")
async def create_embeddings(data: dict):
    try:
        inputs = data["input"]
        model_name = data["model"]
        
        if isinstance(inputs, list):
            inputs = [str(input) for input in inputs]
        else:
            inputs = [str(inputs)]

        logger.debug(f"Received embedding request for model: {model_name} with inputs: {inputs}")

        embeddings = generate_embeddings(inputs, model_name)
        usage = {"total_tokens": sum([len(input_text.split()) for input_text in inputs])}

        logger.debug(f"Embeddings generated successfully: {embeddings}")

        return {
            "object": "list",
            "data": embeddings,
            "model": model_name,
            "usage": usage
        }
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))