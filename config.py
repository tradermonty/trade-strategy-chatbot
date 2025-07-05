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
    PROMPT_FILE = os.getenv("PROMPT_FILE", "prompt.yaml")
    
    # ETL設定 - 投資文書用に最適化
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1200"))  # 複雑な投資戦略により大きなチャンク
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))  # より多くのオーバーラップで文脈保持
    
    # RAG設定 - 包括的な投資アドバイス用
    RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "8"))  # より多くの関連文書を取得
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))  # より保守的な金融アドバイス
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")  # 最新の推奨モデル (2025年1月時点)
    
    # 投資特化設定
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", "8000"))
    FINANCIAL_ADVICE_TEMPERATURE = float(os.getenv("FINANCIAL_ADVICE_TEMPERATURE", "0.1"))
    INCLUDE_RISK_WARNINGS = os.getenv("INCLUDE_RISK_WARNINGS", "true").lower() == "true"
    REQUIRE_DISCLAIMERS = os.getenv("REQUIRE_DISCLAIMERS", "true").lower() == "true"
    
    # サーバー設定
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")
    
    # クライアント設定
    CLIENT_URL = os.getenv("CLIENT_URL", "http://localhost:8000")  # CLIやテスト用のデフォルトURL 