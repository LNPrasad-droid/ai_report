from typing import List
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    APP_NAME: str = "Agentic AI Remote Sensing Platform"
    ENV: str = "development"

    MONGODB_URI: str = Field(..., env="MONGODB_URI")
    MONGODB_DB: str = Field("agentic_ai", env="MONGODB_DB")
    MONGODB_MIN_POOL_SIZE: int = Field(0, env="MONGODB_MIN_POOL_SIZE")
    MONGODB_MAX_POOL_SIZE: int = Field(100, env="MONGODB_MAX_POOL_SIZE")

    # Comma-separated list supported in env; Pydantic will parse into a list if provided as a Python list
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["http://localhost:5173"], env="CORS_ORIGINS")

    # Retrieval / embeddings / vector store
    EMBEDDING_MODEL: str = Field("BAAI/bge-small-en-v1.5", env="EMBEDDING_MODEL")
    CHROMA_PERSIST_DIR: str = Field(".chromadb", env="CHROMA_PERSIST_DIR")
    # Google Earth Engine project id
    GEE_PROJECT: str = Field("ee-leo913173", env="GEE_PROJECT")

    FIREBASE_PROJECT_ID: str = Field(..., env="FIREBASE_PROJECT_ID")
    FIREBASE_SERVICE_ACCOUNT: str = Field(..., env="FIREBASE_SERVICE_ACCOUNT")
    AUTH_DEFAULT_ROLE: str = Field("Viewer", env="AUTH_DEFAULT_ROLE")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

