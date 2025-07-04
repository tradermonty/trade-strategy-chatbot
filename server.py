"""
🟢 Green フェーズ: テストを通すための最小限の実装
RAGサーバーでナレッジベースからの質問応答を提供
"""

import os
import yaml
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
from langchain.prompts import PromptTemplate
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
        self.prompt_template = None
        
    def get_system_prompt(self) -> str:
        """システムプロンプトを取得"""
        prompt_file_path = Path(Config.PROMPTS_PATH) / "prompt.yaml"
        
        if not prompt_file_path.exists():
            return """あなたは「PM実務コンシェルジュGPT」です。
現役プロジェクトマネージャーの日常課題をPMBOK®をはじめとする世界標準・実践知識で伴走支援する相談相手です。

## 応答ルール
- 具体策・チェックリストは箇条書きで表示
- PMBOK参照箇所は版＋章節を明示
- 推測やベストプラクティスは ※参考 と明示
- 日本語で親しみやすく、しかし軽すぎないトーンで回答
"""
        
        try:
            with open(prompt_file_path, 'r', encoding='utf-8') as f:
                prompt_config = yaml.safe_load(f)
            
            # システムプロンプトの構築
            system_prompt = f"""あなたは「{prompt_config.get('name', 'PM実務コンシェルジュGPT')}」です。
{prompt_config.get('description', '')}

## 動作ポリシー
- 言語: {prompt_config.get('language', 'ja')}
- トーン: {prompt_config.get('tone', 'friendly-professional')}
- 温度設定: {prompt_config.get('temperature', 0.3)}

## 応答ルール"""
            
            response_guidelines = prompt_config.get('response_guidelines', [])
            for rule in response_guidelines:
                system_prompt += f"\n- {rule}"
            
            system_prompt += "\n\n## コンプライアンス・倫理"
            compliance_notes = prompt_config.get('compliance_notes', {})
            for note in compliance_notes:
                system_prompt += f"\n- {note}"
            
            return system_prompt
            
        except Exception as e:
            print(f"❌ システムプロンプト取得エラー: {e}")
            return """あなたは「PM実務コンシェルジュGPT」です。
現役プロジェクトマネージャーの日常課題をPMBOK®をはじめとする世界標準・実践知識で伴走支援する相談相手です。

## 応答ルール
- 具体策・チェックリストは箇条書きで表示
- PMBOK参照箇所は版＋章節を明示
- 推測やベストプラクティスは ※参考 と明示
- 日本語で親しみやすく、しかし軽すぎないトーンで回答
"""
    
    def load_prompt_template(self):
        """プロンプトテンプレートの読み込み"""
        prompt_file_path = Path(Config.PROMPTS_PATH) / "prompt.yaml"
        
        if not prompt_file_path.exists():
            print(f"⚠️  プロンプトファイルが見つかりません: {prompt_file_path}")
            # デフォルトのプロンプトを使用
            self.prompt_template = PromptTemplate(
                template="以下の情報を参考に、質問に日本語で回答してください。\n\n{context}\n\n質問: {question}\n\n回答:",
                input_variables=["context", "question"]
            )
            print(f"🔍 デフォルトプロンプト使用: True")
            print(f"🔍 デフォルトプロンプトの変数: {self.prompt_template.input_variables}")
            return
        
        try:
            with open(prompt_file_path, 'r', encoding='utf-8') as f:
                prompt_config = yaml.safe_load(f)
            
            # プロンプト設定から応答ルールを抽出
            response_guidelines = prompt_config.get('response_guidelines', [])
            compliance_notes = prompt_config.get('compliance_notes', [])
            
            # カスタムプロンプトテンプレートの作成
            system_prompt = f"""
あなたは「{prompt_config.get('name', 'PM実務コンシェルジュGPT')}」です。
{prompt_config.get('description', '')}

## 動作ポリシー
- 言語: {prompt_config.get('language', 'ja')}
- トーン: {prompt_config.get('tone', 'friendly-professional')}
- 温度設定: {prompt_config.get('temperature', 0.3)}

## 応答ルール
"""
            
            # 応答ルールを追加
            for rule in response_guidelines:
                system_prompt += f"- {rule}\n"
            
            system_prompt += "\n## コンプライアンス・倫理\n"
            for note in compliance_notes:
                system_prompt += f"- {note}\n"
            
            system_prompt += """
## 回答フォーマット
以下の情報を参考に、上記のルールに従って質問に回答してください。

【参考情報】
{context}

【質問】
{question}

【回答】
"""
            
            self.prompt_template = PromptTemplate(
                template=system_prompt,
                input_variables=["context", "question"]
            )
            
            print("✅ プロンプトテンプレートを読み込みました")
            print(f"🔍 プロンプトテンプレートの変数: {self.prompt_template.input_variables}")
            print(f"🔍 デフォルトプロンプト使用: False")
            
        except Exception as e:
            print(f"❌ プロンプトファイル読み込みエラー: {e}")
            # デフォルトのプロンプトを使用
            self.prompt_template = PromptTemplate(
                template="以下の情報を参考に、質問に日本語で回答してください。\n\n{context}\n\n質問: {question}\n\n回答:",
                input_variables=["context", "question"]
            )
        
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
        
        if self.prompt_template is None:
            raise ValueError("プロンプトテンプレートが読み込まれていません")
        
        llm = ChatOpenAI(
            model=Config.LLM_MODEL,
            temperature=Config.LLM_TEMPERATURE
        )
        
        # retrieverの設定
        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": Config.RETRIEVAL_K}
        )
        
        # カスタムプロンプトを使用してQAチェーンを作成
        # 最新のLangChainでは、プロンプトの問題を回避するため基本機能を使用
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            verbose=True
        )
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """クエリ処理 - テストを通すための実装"""
        if self.qa_chain is None:
            raise ValueError("QAチェーンが設定されていません")
        
        try:
            # システムプロンプトを質問に前置
            system_prompt = self.get_system_prompt()
            enhanced_query = f"{system_prompt}\n\n質問: {query}"
            
            # RetrievalQAチェーンを実行
            result = self.qa_chain.invoke({"query": enhanced_query})
            
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
            # プロンプトテンプレート読み込み
            print("📝 プロンプトテンプレートを読み込み中...")
            self.load_prompt_template()
            print("✅ プロンプトテンプレートの読み込みが完了しました。")
            
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