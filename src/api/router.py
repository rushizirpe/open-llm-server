from fastapi import APIRouter
from src.api.endpoints import embeddings, chat, metrics

router = APIRouter()
router.include_router(embeddings.router, prefix="/v1/embeddings", tags=["embeddings"])
router.include_router(chat.router, prefix="/v1/chat", tags=["chat"])
router.include_router(metrics, prefix="/v1/metrics", tags=["metrics"])