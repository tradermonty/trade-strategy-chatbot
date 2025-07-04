# RAG Starter Kit Design Document

**Version 2.0 — 2025-07-04**

An educational, beginner-friendly Retrieval-Augmented Generation (RAG) starter template designed for learning and understanding RAG technology through hands-on implementation.

---

## 1. System Overview

The RAG Starter Kit is designed to help developers learn RAG technology by building their own AI assistant. By providing a complete, working example with Japanese recipe knowledge base, it serves as an educational foundation for understanding RAG concepts and implementation patterns.

### Core Principles

- **Educational First**: Clear, commented code with step-by-step explanations
- **Hands-On Learning**: Learn RAG concepts by building a working system
- **Quick Start**: From zero to working AI assistant in 10 minutes
- **Customizable**: Easy to adapt for your own knowledge domains
- **Best Practices**: Modern Python, FastAPI, and AI development patterns
- **Bridge to Production**: Foundation for more complex systems

## 2. Learning Architecture

### 2.1 System Architecture

*Understanding how RAG systems work under the hood*

```text
┌─────────────┐      HTTPS (JSON)      ┌───────────────────────┐
│   Client    │ ─────────────────────▶ │  RAG API (FastAPI)    │
│ Application │                        │  • Auth (JWT)          │
└─────────────┘                        │  • Retriever (FAISS)   │
                                       │  • LLM (OpenAI)        │
                                       └────────┬──────────────┘
                                                │
                      VectorStore.load()        │
                                                ▼
                                        FAISS index (local)
                                                ▲
                                        ingest.py (ETL)
                                                ▲
                                        knowledge/*.md
```

---

## 3. Directory Structure

```
rag-starter-kit/
│
├── knowledge/               # Learning knowledge base (Japanese recipes included)
│   ├── 01_basic_rice_dishes.md
│   ├── 02_noodle_dishes.md
│   └── ... (replace with your own documents)
│
├── prompt/                  # Prompt configuration for learning
│   └── prompt.yaml         # Customizable system prompts
│
├── vector_store/           # Generated vector embeddings (auto-created)
│   ├── index.faiss
│   └── index.pkl
│
├── src/                    # Source code (well-commented for learning)
│   ├── run_etl.py         # Document processing pipeline
│   ├── server.py          # FastAPI application
│   ├── config.py          # Configuration management
│   ├── query_cli.py       # Command-line interface
│   └── demo_runner.py     # Demo and testing tool
│
├── tests/                  # Test suite (TDD examples)
│   ├── test_ingest.py
│   └── test_server.py
│
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variable template
├── README.md              # Getting started guide
├── README_ja.md           # Japanese version
├── design.md              # This design document
├── Dockerfile             # Container configuration
└── docker-compose.yml     # Multi-container setup
```

---

## 4. Component Architecture

### 4.1 Document Processing Pipeline

| Component | Technology | Configuration | Purpose |
|-----------|-----------|---------------|---------|
| **Document Loader** | Python + Markdown | Supports .md, .txt | Ingests knowledge documents |
| **Text Splitter** | LangChain MarkdownTextSplitter | chunk_size=800, overlap=100 | Creates semantic chunks |
| **Embeddings** | OpenAI text-embedding-3-small | Dimension: 1536 | Generates vector representations |
| **Vector Store** | FAISS | Flat index, L2 distance | Enables similarity search |

### 4.2 Query Processing Pipeline

| Component | Technology | Configuration | Purpose |
|-----------|-----------|---------------|---------|
| **API Gateway** | FastAPI | Async, auto-docs | REST API interface |
| **Authentication** | JWT + python-jose | HS256, 24h expiry | Secure access control |
| **Retriever** | FAISS VectorStore | k=6 neighbors | Finds relevant chunks |
| **LLM Integration** | OpenAI GPT-4 | temperature=0.3 | Generates responses |
| **Prompt Manager** | YAML + Jinja2 | Customizable templates | Domain-specific behavior |

### 4.3 Configuration System

```python
# Environment Variables (.env)
OPENAI_API_KEY=sk-...          # Required: OpenAI API access
JWT_SECRET_KEY=...             # Required: JWT signing key

# Optional Configurations
CHUNK_SIZE=800                 # Document chunk size
CHUNK_OVERLAP=100             # Overlap between chunks
RETRIEVAL_K=6                 # Number of chunks to retrieve
LLM_MODEL=gpt-4              # LLM model selection
LLM_TEMPERATURE=0.3          # Response creativity (0-1)
VECTOR_STORE_PATH=vector_store # Vector store location
KNOWLEDGE_PATH=knowledge      # Knowledge base location
```

---

## 5. API Specification

### 5.1 Authentication Flow

```mermaid
sequenceDiagram
    Client->>API: POST /login {username, password}
    API->>Client: {access_token, token_type}
    Client->>API: POST /query {Authorization: Bearer token}
    API->>Client: {answer, sources, timestamp}
```

### 5.2 Endpoints

#### Health Check
```http
GET /health
Response: {
  "status": "ok",
  "timestamp": "2025-01-04T10:00:00Z",
  "vector_store_loaded": true,
  "qa_chain_ready": true
}
```

#### Login
```http
POST /login?username={username}&password={password}
Response: {
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### Query
```http
POST /query
Headers: 
  Authorization: Bearer {token}
  Content-Type: application/json
Body: {
  "query": "Your question here",
  "user_id": "optional_user_id"
}
Response: {
  "answer": "The detailed response...",
  "sources": ["document1.md", "document2.md"],
  "timestamp": "2025-01-04T10:00:00Z"
}
```

---

## 6. Learning Customization Guide

*Once you understand the basics, customize for your domain*

### 6.1 Knowledge Base Setup

1. **Document Format**: Use Markdown for rich formatting
   ```markdown
   # Topic Title
   
   ## Section 1
   Content with **emphasis** and `code`.
   
   ## Section 2
   - Bullet points
   - Lists
   ```

2. **Document Organization**: Group related content
   ```
   knowledge/
   ├── category1/
   │   ├── topic1.md
   │   └── topic2.md
   └── category2/
       └── topic3.md
   ```

3. **Metadata**: Use frontmatter for document metadata
   ```markdown
   ---
   title: Document Title
   category: Category Name
   tags: [tag1, tag2]
   ---
   # Content starts here
   ```

### 6.2 Prompt Engineering

Edit `prompt/prompt.yaml`:

```yaml
name: Your Assistant Name
version: "1.0"
description: >
  Detailed description of your AI assistant's purpose and capabilities

# Behavior Configuration
language: "en"              # Primary language
tone: "professional"        # professional, friendly, casual
temperature: 0.3           # 0.1-0.9 (factual to creative)
format_preference: "markdown"

# System Instructions
system_prompt: |
  You are a knowledgeable assistant specializing in {domain}.
  Your responses should be:
  - Accurate and fact-based
  - Well-structured and easy to understand
  - Referenced to source documents when possible

# Response Guidelines
response_guidelines:
  - Always cite sources when available
  - Use bullet points for lists
  - Include code examples when relevant
  - Acknowledge uncertainty when appropriate

# Example Interactions
examples:
  - query: "What is X?"
    response: "X is... [Source: document.md]"
```

### 6.3 Advanced Learning Configurations

#### Vector Store Optimization
```python
# For large knowledge bases (>100MB)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
)

# For technical documentation
text_splitter = MarkdownTextSplitter(
    chunk_size=1500,
    chunk_overlap=300
)
```

#### Multi-Model Support
```python
# config.py
LLM_MODELS = {
    "fast": "gpt-3.5-turbo",
    "accurate": "gpt-4",
    "creative": "gpt-4-turbo"
}

# Select based on query type
model = LLM_MODELS.get(query_type, "gpt-4")
```

---

## 7. Deployment Strategies for Learning

*From local development to production deployment*

### 7.1 Local Development
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 run_etl.py
python3 server.py
```

### 7.2 Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python3 run_etl.py
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 7.3 Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-api
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: rag-api
        image: rag-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: rag-secrets
              key: openai-api-key
```

### 7.4 Cloud Deployment Options

| Platform | Service | Configuration |
|----------|---------|---------------|
| **AWS** | ECS Fargate | Auto-scaling, ALB |
| **GCP** | Cloud Run | Serverless, auto-scale |
| **Azure** | Container Instances | Managed containers |
| **Heroku** | Container Registry | Simple deployment |

---

## 8. Performance Optimization for Learning

*Understanding how to tune RAG systems*

### 8.1 Caching Strategy
```python
from functools import lru_cache
import redis

# In-memory caching for embeddings
@lru_cache(maxsize=1000)
def get_embedding(text: str):
    return embeddings.embed_query(text)

# Redis for distributed caching
cache = redis.Redis(host='localhost', port=6379)
```

### 8.2 Batch Processing
```python
# Process multiple queries concurrently
async def batch_query(queries: List[str]):
    tasks = [process_query(q) for q in queries]
    return await asyncio.gather(*tasks)
```

### 8.3 Vector Store Scaling

| Knowledge Size | Recommended Solution | Configuration |
|----------------|---------------------|---------------|
| < 1GB | FAISS (local) | Default |
| 1-10GB | FAISS (GPU) | faiss-gpu |
| 10-100GB | Chroma | Persistent, distributed |
| > 100GB | Pinecone/Weaviate | Cloud-native |

---

## 9. Security Best Practices for Learning

*Essential security knowledge for AI applications*

### 9.1 Authentication & Authorization
- Implement OAuth2 for production
- Use short-lived tokens (15-30 minutes)
- Implement refresh token rotation
- Add role-based access control (RBAC)

### 9.2 API Security
- Rate limiting per user/IP
- Request size limits
- Input sanitization
- SQL injection prevention
- XSS protection

### 9.3 Data Security
- Encrypt sensitive documents
- Implement data retention policies
- Audit logging for compliance
- GDPR/CCPA compliance features

---

## 10. Monitoring & Observability for Learning

*Understanding how to monitor AI systems in production*

### 10.1 Metrics to Track
```python
# Application metrics
- Request rate and latency
- Token usage and costs
- Cache hit/miss ratios
- Error rates by endpoint

# Business metrics
- Query topics and frequency
- User engagement patterns
- Knowledge base coverage
- Response quality scores
```

### 10.2 Logging Strategy
```python
import structlog

logger = structlog.get_logger()

# Structured logging
logger.info("query_processed", 
    user_id=user_id,
    query_length=len(query),
    response_time=elapsed,
    chunks_retrieved=len(chunks),
    model_used=model_name
)
```

### 10.3 Alerting Rules
- High error rate (> 1%)
- Slow response time (> 5s)
- Low vector store matches
- API quota warnings

---

## 11. Educational Roadmap

*Your learning journey from starter kit to production system*

### Beginner Phase: Master the Basics
- [ ] Complete the 10-minute setup tutorial
- [ ] Understand vector embeddings and similarity search
- [ ] Experiment with different prompt configurations
- [ ] Replace sample knowledge base with your own content
- [ ] Learn about chunk sizes and overlap optimization

### Intermediate Phase: Advanced RAG Concepts
- [ ] Implement hybrid search (keyword + semantic)
- [ ] Add streaming responses for better UX
- [ ] Integrate user feedback mechanisms
- [ ] Experiment with different LLM models
- [ ] Build conversation memory features

### Advanced Phase: Production-Ready Systems
- [ ] Multi-language support implementation
- [ ] Document version control and updates
- [ ] A/B testing framework for prompts
- [ ] Custom model fine-tuning
- [ ] Advanced analytics and monitoring

### Expert Phase: Enterprise Features
- [ ] Multi-tenancy support
- [ ] Advanced analytics dashboard
- [ ] Custom model deployment
- [ ] Compliance and audit features

---

## 12. Troubleshooting Guide for Learners

*Common learning challenges and solutions*

### Common Issues and Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Slow responses | >5s latency | Reduce chunk size, use GPT-3.5 |
| Poor answers | Irrelevant responses | Improve prompt, increase retrieval_k |
| High costs | Large API bills | Implement caching, use smaller models |
| Memory errors | OOM crashes | Batch processing, reduce vector dimensions |

### Debug Mode
```python
# Enable verbose logging
LANGCHAIN_VERBOSE=true
LOG_LEVEL=DEBUG

# Test individual components
python3 -c "from ingest import KnowledgeIngester; KnowledgeIngester().test()"
```

---

## 13. Contributing Guidelines

*Help others learn RAG technology*

### Development Workflow
1. Fork the repository
2. Create feature branch
3. Write tests first (TDD)
4. Implement features
5. Update documentation
6. Submit pull request

### Code Standards
- Python 3.11+
- Type hints required
- 100% test coverage for new code
- Follow PEP 8
- Document all functions

### Testing Requirements
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# End-to-end tests
python3 demo_runner.py --test-all
```

---

**Learn RAG technology by building your own AI assistant with the RAG Starter Kit!**