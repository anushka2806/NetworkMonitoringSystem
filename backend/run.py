import uvicorn
from backend.app import config

if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host=config.FASTAPI_HOST,
        port=config.FASTAPI_PORT,
        reload=False
    )
