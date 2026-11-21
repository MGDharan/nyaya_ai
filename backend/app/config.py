from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    app_name: str = "NyayaAI"
    environment: str = "development"
    data_dir: str = "./data"
    chroma_dir: str = "./data/chroma"
    embedding_model: str = "intfloat/multilingual-e5-small"
    llm_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b"
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    admin_api_key: str = ""
    max_upload_mb: int = 25
    top_k: int = 7
    _ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
    model_config = SettingsConfigDict(
        env_file=(_ENV_PATH if _ENV_PATH.exists() else ".env", ".env"),
        extra="ignore"
    )

settings = Settings()
Path(settings.data_dir).mkdir(parents=True, exist_ok=True)
Path(settings.chroma_dir).mkdir(parents=True, exist_ok=True)
