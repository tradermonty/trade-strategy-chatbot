"""
🟢 Green Phase: Minimal implementation to pass tests
RAG server providing question-answering from knowledge base
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
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.prompt_template = None
        
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
        """Load prompt template"""
        prompt_file_path = Path(Config.PROMPTS_PATH) / Config.PROMPT_FILE
        
        if not prompt_file_path.exists():
            print(f"⚠️  Prompt file not found: {prompt_file_path}")
            # Use default prompt
            self.prompt_template = PromptTemplate(
                template="Please answer the question based on the following information.\n\n{context}\n\nQuestion: {question}\n\nAnswer:",
                input_variables=["context", "question"]
            )
            print(f"🔍 Using default prompt: True")
            print(f"🔍 Default prompt variables: {self.prompt_template.input_variables}")
            return
        
        try:
            with open(prompt_file_path, 'r', encoding='utf-8') as f:
                prompt_config = yaml.safe_load(f)
            
            # Extract response rules from prompt configuration
            response_guidelines = prompt_config.get('response_guidelines', [])
            compliance_notes = prompt_config.get('compliance_notes', [])
            
            # Create custom prompt template
            system_prompt = f"""
あなたは「{prompt_config.get('name', 'Universal Knowledge Assistant')}」です。
{prompt_config.get('description', '')}

## Operating Policy
- Language: {prompt_config.get('language', 'ja')}
- Tone: {prompt_config.get('tone', 'friendly-professional')}
- Temperature: {prompt_config.get('temperature', 0.3)}

## Response Rules
"""
            
            # Add response rules
            for rule in response_guidelines:
                system_prompt += f"- {rule}\n"
            
            system_prompt += "\n## Compliance & Ethics\n"
            for note in compliance_notes:
                system_prompt += f"- {note}\n"
            
            system_prompt += """
## Response format
Please answer the question based on the following information, following the rules above。

【Reference Information】
{context}

【Question】
{question}

【Answer】
"""
            
            self.prompt_template = PromptTemplate(
                template=system_prompt,
                input_variables=["context", "question"]
            )
            
            print("✅ Loaded prompt template")
            print(f"🔍 Prompt template variables: {self.prompt_template.input_variables}")
            print(f"🔍 Using default prompt: False")
            
        except Exception as e:
            print(f"❌ プロンプトFile loadingエラー: {e}")
            # Use default prompt
            self.prompt_template = PromptTemplate(
                template="Please answer the question based on the following information.\n\n{context}\n\nQuestion: {question}\n\nAnswer:",
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
        
        if self.prompt_template is None:
            raise ValueError("Prompt template not loaded")
        
        llm = ChatOpenAI(
            model=Config.LLM_MODEL,
            temperature=Config.LLM_TEMPERATURE
        )
        
        # Configure retriever
        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": Config.RETRIEVAL_K}
        )
        
        # Create QA chain using custom prompt
        # Use basic functionality to avoid prompt issues in latest LangChain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            verbose=True
        )
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """Query processing - implementation to pass tests"""
        if self.qa_chain is None:
            raise ValueError("QA chain not configured")
        
        try:
            # Prepend system prompt to question
            system_prompt = self.get_system_prompt()
            enhanced_query = f"{system_prompt}\n\nQuestion: {query}"
            
            # Execute RetrievalQA chain
            result = self.qa_chain.invoke({"query": enhanced_query})
            
            # Extract source documents
            sources = []
            if "source_documents" in result:
                for doc in result["source_documents"]:
                    if "source" in doc.metadata:
                        sources.append(doc.metadata["source"])
            
            return {
                "answer": result["result"],
                "sources": list(set(sources)),  # Remove duplicates
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Process queryエラー: {str(e)}"
            )
    
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
    title="Universal RAG API",
    description="A flexible knowledge-based question answering system",
    version="1.0.0",
    lifespan=lifespan
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
        "message": "Universal RAG API",
        "version": "1.0.0",
        "status": "running"
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


@app.post("/login")
async def login(username: str, password: str):
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


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Universal RAG Server starting...")
    uvicorn.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        log_level="info"
    ) 