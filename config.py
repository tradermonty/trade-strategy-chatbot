import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "vector_store")
    KNOWLEDGE_PATH = os.getenv("KNOWLEDGE_PATH", "knowledge")
    PROMPTS_PATH = os.getenv("PROMPTS_PATH", "prompt")
    
    # ETL設定
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
    
    # RAG設定
    RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "6"))
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")  # o3がまだ利用できない場合gpt-4使用
    
    # サーバー設定
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000")) 