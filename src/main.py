import torch
from fastapi import FastAPI
from src.api.router import router
from src.core.config import settings
from src.core.logging import setup_logging

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

setup_logging()

app.include_router(router)

@app.get("/")
async def root():
    # Check if CUDA is available
    gpu_available = torch.cuda.is_available()
    
    gpu_info = {}
    if gpu_available:
        for i in range(torch.cuda.device_count()):
            gpu_info[f"GPU {i}"] = {
                "compute_capability": str(torch.cuda.get_device_capability(i)),
                "device_name": torch.cuda.get_device_name(i)
            }
    else:
        gpu_info["GPU"] = "Not Available"

    # Construct the response
    response = {
        "status": "System Status: Operational",
        "gpu": "Available" if gpu_available else "Not Available",
        "gpu_details": gpu_info
    }
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)