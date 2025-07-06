"""
🟢 Green Phase: Minimal implementation to pass tests
RAG server providing question-answering from knowledge base
"""

import os
import yaml
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, status, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from jose import JWTError, jwt
from langdetect import detect
from config import Config

# .envファイルを読み込み
load_dotenv()


class QueryRequest(BaseModel):
    """Query request model"""
    query: str
    user_id: str = "default"


class QueryResponse(BaseModel):
    """Query response model"""
    answer: str
    sources: List[str] = []
    timestamp: str


class RAGServer:
    """RAG Server class"""
    
    def __init__(self):
        """Initializer - minimal implementation to pass tests"""
        self.vector_store_path = Config.VECTOR_STORE_PATH
        self.vector_store = None
        self.qa_chain = None
        self.streaming_qa_chain = None
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.prompt_template = None
        self.prompt_config = None
        
    def detect_language(self, text: str) -> str:
        """Detect language of the input text"""
        try:
            detected_lang = detect(text)
            # Map detected language to our supported languages
            if detected_lang == 'ja':
                return 'japanese'
            elif detected_lang == 'en':
                return 'english'
            else:
                return 'english'  # Default to English for other languages
        except Exception as e:
            print(f"⚠️ Language detection error: {e}")
            return 'english'  # Default to English on error
    
    def get_system_prompt(self) -> str:
        """Get system prompt"""
        prompt_file_path = Path(Config.PROMPTS_PATH) / Config.PROMPT_FILE
        
        if not prompt_file_path.exists():
            return """You are the "Universal Knowledge Assistant".
A knowledgeable assistant that provides helpful and contextual answers based on your knowledge base.

## Response Rules
- Display concrete measures and checklists in bullet points
- Reference sources and documents when available
- Mark speculations and best practices with ※Reference
- Respond in a friendly yet professional tone
"""
        
        try:
            with open(prompt_file_path, 'r', encoding='utf-8') as f:
                prompt_config = yaml.safe_load(f)
            
            # システムプロンプトの構築
            system_prompt = f"""あなたは「{prompt_config.get('name', 'Universal Knowledge Assistant')}」です。
{prompt_config.get('description', '')}

## Operating Policy
- Language: {prompt_config.get('language', 'ja')}
- Tone: {prompt_config.get('tone', 'friendly-professional')}
- Temperature: {prompt_config.get('temperature', 0.3)}

## Response Rules"""
            
            response_guidelines = prompt_config.get('response_guidelines', [])
            for rule in response_guidelines:
                system_prompt += f"\n- {rule}"
            
            system_prompt += "\n\n## Compliance & Ethics"
            compliance_notes = prompt_config.get('compliance_notes', {})
            for note in compliance_notes:
                system_prompt += f"\n- {note}"
            
            return system_prompt
            
        except Exception as e:
            print(f"❌ System prompt acquisition error: {e}")
            return """You are the "Universal Knowledge Assistant".
A knowledgeable assistant that provides helpful and contextual answers based on your knowledge base.
"""
    
    def load_prompt_template(self):
        """Load prompt template configuration"""
        prompt_file_path = Path(Config.PROMPTS_PATH) / Config.PROMPT_FILE
        
        if not prompt_file_path.exists():
            print(f"⚠️  Prompt file not found: {prompt_file_path}")
            # Use default prompt config
            self.prompt_config = {
                'name': 'Universal Knowledge Assistant',
                'description': 'A knowledgeable assistant that provides helpful and contextual answers.',
                'language': 'auto-detect',
                'tone': 'friendly',
                'temperature': 0.3,
                'system_prompt': 'You are a specialized AI assistant for Japanese cuisine with deep knowledge of authentic Japanese recipes, cooking techniques, and cultural background.',
                'response_guidelines': []
            }
            print(f"🔍 Using default prompt: True")
            return
        
        try:
            with open(prompt_file_path, 'r', encoding='utf-8') as f:
                self.prompt_config = yaml.safe_load(f)
            
            print("✅ Loaded prompt configuration")
            print(f"🔍 Using default prompt: False")
            
        except Exception as e:
            print(f"❌ プロンプトFile loadingエラー: {e}")
            # Use default prompt config
            self.prompt_config = {
                'name': 'Universal Knowledge Assistant',
                'description': 'A knowledgeable assistant that provides helpful and contextual answers.',
                'language': 'auto-detect',
                'tone': 'friendly',
                'temperature': 0.3,
                'system_prompt': 'You are a specialized AI assistant for Japanese cuisine with deep knowledge of authentic Japanese recipes, cooking techniques, and cultural background.',
                'response_guidelines': []
            }
    
    def get_dynamic_prompt_template(self, question: str) -> PromptTemplate:
        """Generate dynamic prompt template based on question language"""
        if self.prompt_config is None:
            # Fallback to default template
            return PromptTemplate(
                template="Please answer the question based on the following information.\n\n{context}\n\nQuestion: {question}\n\nAnswer:",
                input_variables=["context", "question"]
            )
        
        # Detect language of the question
        detected_lang = self.detect_language(question)
        
        # Get system prompt from config
        system_prompt = self.prompt_config.get('system_prompt', '')
        
        # Create language-specific prompt
        if detected_lang == 'japanese':
            template = f"""{system_prompt}

以下の情報を基に、質問に日本語で答えてください。

【参考情報】
{{context}}

【質問】
{{question}}

【回答】
"""
        else:  # English or other languages
            template = f"""{system_prompt}

Please answer the question in English based on the following information.

**Reference Information**
{{context}}

**Question**
{{question}}

**Answer**
"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
    def load_vector_store(self):
        """Load vector store - implementation to pass tests"""
        if not Path(self.vector_store_path).exists():
            raise FileNotFoundError(f"Vector store not found: {self.vector_store_path}")
        
        self.vector_store = FAISS.load_local(
            self.vector_store_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        
    def setup_qa_chain(self):
        """RetrievalQA setup - implementation to pass tests"""
        if self.vector_store is None:
            raise ValueError("Vector store not loaded")
        
        if self.prompt_config is None:
            raise ValueError("Prompt configuration not loaded")
        
        # QA chain is no longer needed as we use dynamic prompt templates
        # All processing is done directly in process_query methods
        # Set qa_chain to True to indicate system is ready
        self.qa_chain = "dynamic_prompt_system"
        print("✅ Dynamic prompt template setup completed.")
        print("✅ QA chain setup completed.")
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """Query processing - implementation to pass tests"""
        if self.vector_store is None:
            raise ValueError("Vector store not loaded")
        
        try:
            # Get dynamic prompt template based on question language
            prompt_template = self.get_dynamic_prompt_template(query)
            
            # Get relevant documents
            retriever = self.vector_store.as_retriever(
                search_kwargs={"k": Config.RETRIEVAL_K}
            )
            relevant_docs = retriever.get_relevant_documents(query)
            
            # Extract source information
            sources = []
            for doc in relevant_docs:
                if "source" in doc.metadata:
                    sources.append(doc.metadata["source"])
            
            # Build context
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # Generate final query using prompt template
            final_query = prompt_template.format(
                context=context,
                question=query
            )
            
            # Execute LLM
            llm = ChatOpenAI(
                model=Config.LLM_MODEL,
                temperature=Config.LLM_TEMPERATURE
            )
            
            result = llm.invoke(final_query)
            
            return {
                "answer": result.content,
                "sources": list(set(sources)),  # Remove duplicates
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Process queryエラー: {str(e)}"
            )
    
    async def process_query_streaming(self, query: str) -> AsyncGenerator[str, None]:
        """ストリーミング用クエリ処理"""
        if self.vector_store is None:
            raise ValueError("Vector store not loaded")
        
        try:
            # Get dynamic prompt template based on question language
            prompt_template = self.get_dynamic_prompt_template(query)
            
            # ストリーミング処理を開始
            sources = []
            
            # 先に関連ドキュメントを取得
            retriever = self.vector_store.as_retriever(
                search_kwargs={"k": Config.RETRIEVAL_K}
            )
            relevant_docs = retriever.get_relevant_documents(query)
            
            # ソース情報を抽出
            for doc in relevant_docs:
                if "source" in doc.metadata:
                    sources.append(doc.metadata["source"])
            
            # コンテキストを構築
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # プロンプトテンプレートでクエリを構築
            final_query = prompt_template.format(
                context=context,
                question=query
            )
            
            # ストリーミングLLMを直接使用
            streaming_llm = ChatOpenAI(
                model=Config.LLM_MODEL,
                temperature=Config.LLM_TEMPERATURE,
                streaming=True
            )
            
            # ストリーミング開始通知
            start_data = {
                "type": "start",
                "sources": list(set(sources)),
                "timestamp": datetime.now().isoformat()
            }
            yield f"data: {json.dumps(start_data, ensure_ascii=False)}\n\n"
            
            # ストリーミング実行
            async for chunk in streaming_llm.astream(final_query):
                if chunk.content:
                    token_data = {
                        "type": "token",
                        "content": chunk.content,
                        "timestamp": datetime.now().isoformat()
                    }
                    yield f"data: {json.dumps(token_data, ensure_ascii=False)}\n\n"
            
            # 完了通知
            complete_data = {
                "type": "complete",
                "timestamp": datetime.now().isoformat()
            }
            yield f"data: {json.dumps(complete_data, ensure_ascii=False)}\n\n"
            
        except Exception as e:
            error_data = {
                "type": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
            yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
    
    def initialize(self):
        """Server initialization"""
        print("🔄 Initializing RAG server...")
        
        try:
            # プロンプトテンプレート読み込み
            print("📝 Loading prompt template...")
            self.load_prompt_template()
            print("✅ Load prompt templateが完了しました。")
            
            # ベクトルストア読み込み
            print("📚 Loading vector store...")
            self.load_vector_store()
            print("✅ Vector store loading completed.")
            
            # QAチェーンセットアップ
            print("🔗 Setting up QA chain...")
            self.setup_qa_chain()
            print("✅ QA chain setup completed.")
            
            print("🚀 RAG server initialization completed!")
            
        except Exception as e:
            print(f"❌ Server initializationエラー: {e}")
            raise


# RAG server instance
rag_server = RAGServer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Startup processing
    try:
        rag_server.initialize()
        yield
    except Exception as e:
        print(f"❌ Server startup error: {e}")
        raise
    finally:
        # Shutdown processing (if needed)
        print("🛑 Shutting down server...")


# FastAPIアプリケーション
app = FastAPI(
    title="RAG Starter Kit",
    description="Educational RAG system for learning AI development",
    version="1.0.0",
    lifespan=lifespan
)

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


def create_access_token(data: dict) -> str:
    """Create access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Token verification"""
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
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RAG Starter Kit",
        "version": "1.0.0",
        "status": "running",
        "description": "Educational RAG system for learning AI development"
    }


@app.get("/health")
async def health_check():
    """Health check - implementation to pass tests"""
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
    """Query endpoint - actual RAG inquiry processing"""
    try:
        # Process query
        result = rag_server.process_query(request.query)
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            timestamp=result["timestamp"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Process queryエラー: {str(e)}"
        )


@app.post("/query/stream")
async def query_stream_endpoint(
    request: QueryRequest,
    token_payload: dict = Depends(verify_token)
):
    """ストリーミング用クエリエンドポイント"""
    try:
        # ストリーミング処理を開始
        return StreamingResponse(
            rag_server.process_query_streaming(request.query),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"  # nginx用のバッファリング無効化
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Streaming query error: {str(e)}"
        )


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """Login endpoint (authentication via environment variables)"""
    # Get authentication information from environment variables
    valid_username = os.getenv("DEMO_USERNAME", "admin")
    valid_password = os.getenv("DEMO_PASSWORD", "change-this-password")
    
    if username == valid_username and password == valid_password:
        access_token = create_access_token(
            data={"sub": username, "user_id": username}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )


@app.get("/RAG_demo.html")
async def demo_html():
    """Serve demo HTML file"""
    return FileResponse("RAG_demo.html", media_type="text/html")


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 RAG Starter Kit Server starting...")
    uvicorn.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        log_level="info"
    ) 