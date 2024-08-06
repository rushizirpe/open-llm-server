from fastapi import FastAPI
from src.api.router import router
from src.core.config import settings
from src.core.logging import setup_logging

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

setup_logging()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)