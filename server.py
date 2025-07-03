"""
🟢 Green フェーズ: テストを通すための最小限の実装
RAGサーバーでナレッジベースからの質問応答を提供
"""

import os
from pathlib import Path
from typing import Dict, List, Any
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from jose import JWTError, jwt
from config import Config


class QueryRequest(BaseModel):
    """クエリリクエストモデル"""
    query: str
    user_id: str = "default"


class QueryResponse(BaseModel):
    """クエリレスポンスモデル"""
    answer: str
    sources: List[str] = []
    timestamp: str


class RAGServer:
    """RAGサーバークラス"""
    
    def __init__(self):
        """イニシャライザー - テストを通すための最小限の実装"""
        self.vector_store_path = Config.VECTOR_STORE_PATH
        self.vector_store = None
        self.qa_chain = None
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
    def load_vector_store(self):
        """ベクトルストア読み込み - テストを通すための実装"""
        if not Path(self.vector_store_path).exists():
            raise FileNotFoundError(f"ベクトルストアが見つかりません: {self.vector_store_path}")
        
        self.vector_store = FAISS.load_local(
            self.vector_store_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        
    def setup_qa_chain(self):
        """RetrievalQAセットアップ - テストを通すための実装"""
        if self.vector_store is None:
            raise ValueError("ベクトルストアが読み込まれていません")
        
        llm = ChatOpenAI(
            model=Config.LLM_MODEL,
            temperature=Config.LLM_TEMPERATURE
        )
        
        # retrieverの設定
        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": Config.RETRIEVAL_K}
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """クエリ処理 - テストを通すための実装"""
        if self.qa_chain is None:
            raise ValueError("QAチェーンが設定されていません")
        
        try:
            result = self.qa_chain.invoke({"query": query})
            
            # ソースドキュメントの抽出
            sources = []
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    if "source" in doc.metadata:
                        sources.append(doc.metadata["source"])
            
            return {
                "answer": result["result"],
                "sources": list(set(sources)),  # 重複除去
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"クエリ処理エラー: {str(e)}"
            )
    
    def initialize(self):
        """サーバー初期化"""
        print("🔄 RAGサーバーを初期化中...")
        
        try:
            # ベクトルストア読み込み
            print("📚 ベクトルストアを読み込み中...")
            self.load_vector_store()
            print("✅ ベクトルストアの読み込みが完了しました。")
            
            # QAチェーンセットアップ
            print("🔗 QAチェーンをセットアップ中...")
            self.setup_qa_chain()
            print("✅ QAチェーンのセットアップが完了しました。")
            
            print("🚀 RAGサーバーの初期化が完了しました！")
            
        except Exception as e:
            print(f"❌ サーバー初期化エラー: {e}")
            raise


# RAGサーバーのインスタンス
rag_server = RAGServer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションライフサイクル管理"""
    # 起動時の処理
    try:
        rag_server.initialize()
        yield
    except Exception as e:
        print(f"❌ サーバー起動エラー: {e}")
        raise
    finally:
        # 終了時の処理（必要に応じて）
        print("🛑 サーバーを終了しています...")


# FastAPIアプリケーション
app = FastAPI(
    title="PM実務コンシェルジュ RAG API",
    description="PM実務に関する質問応答システム",
    version="1.0.0",
    lifespan=lifespan
)

security = HTTPBearer()


def create_access_token(data: dict) -> str:
    """アクセストークン作成"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """トークン検証"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無効なトークンです",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "PM実務コンシェルジュ RAG API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """ヘルスチェック - テストを通すための実装"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "vector_store_loaded": rag_server.vector_store is not None,
        "qa_chain_ready": rag_server.qa_chain is not None
    }


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(
    request: QueryRequest,
    token_payload: dict = Depends(verify_token)
):
    """クエリエンドポイント - 実際のRAG問い合わせ処理"""
    try:
        # クエリ処理
        result = rag_server.process_query(request.query)
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            timestamp=result["timestamp"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"クエリ処理エラー: {str(e)}"
        )


@app.post("/login")
async def login(username: str, password: str):
    """ログインエンドポイント（デモ用）"""
    # デモ用の簡単な認証（本番環境では適切な認証を実装）
    if username == "pm_user" and password == "demo_password":
        access_token = create_access_token(
            data={"sub": username, "user_id": "demo_user"}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="認証情報が正しくありません"
        )


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 PM実務コンシェルジュ RAGサーバーを起動中...")
    uvicorn.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        log_level="info"
    ) 