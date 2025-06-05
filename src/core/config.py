# filepath: c:\Users\anhld\Work\Learn\mcp_test\src\core\config.py
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):
    """Application configuration using pydantic settings to read from environment variables."""
    
    # Server settings
    HOST: str = "127.0.0.1"
    PORT: int = 17324
    LOG_LEVEL: str = "info"
    
    # API Keys
    NEWS_API_KEY: Optional[str] = None
    JINA_API_KEY: Optional[str] = None
    
    # Qdrant settings
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "documents"
    QDRANT_API_KEY: Optional[str] = None  # Optional for cloud-hosted Qdrant
    
    # Embedding service settings
    JINA_API_URL: str = "https://api.jina.ai/v1/embeddings"
    JINA_EMBEDDING_MODEL: str = "jina-embeddings-v2-base-en"
    
    # Dotenv file settings
    model_config = SettingsConfigDict(
        case_sensitive=True
    )


# Create a global instance of Config that can be imported throughout the application
config = Config()