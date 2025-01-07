import logging
from contextlib import asynccontextmanager
from config import get_settings
from db import sessionmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


settings = get_settings()

logging.basicConfig(level=settings.APP_LOG_LEVEL)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with sessionmanager.connect() as connection:  # Test DB connection
            logger.info("Database connection is successful.")
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection failed")

    yield
    if sessionmanager.engine is not None:
        await sessionmanager.close()

app = FastAPI(
    lifespan=lifespan,
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url="/",
)

# TODO: specify CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
    )
