# 🚀 Universal RAG API System

**A production-ready Retrieval-Augmented Generation (RAG) API system that can be customized for any domain**

## 📖 Overview

The Universal RAG API System is a flexible, domain-agnostic question-answering system built with modern AI technologies. Simply replace the knowledge base and prompts to create a specialized AI assistant for any field - from technical documentation to customer support, legal documents to medical knowledge.

### 🎯 Key Features

- **🧠 Domain-Agnostic Design**: Easily adaptable to any knowledge domain
- **🔍 Advanced RAG Technology**: LangChain + FAISS + OpenAI Embeddings
- **🔐 JWT Authentication**: Secure API access out of the box
- **⚡ High Performance**: Optimized for fast response times
- **📚 Flexible Knowledge Base**: Support for Markdown documents
- **🎨 Customizable Prompts**: YAML-based prompt configuration
- **🏗️ Production-Ready**: Built with FastAPI for scalability

## 🏗️ Architecture

```
📱 Client Application
    ↓
🌐 FastAPI Server (server.py)
    ↓
🧠 LangChain RAG + OpenAI GPT-4
    ↓
📊 FAISS Vector Store
    ↓
📚 Knowledge Base (Markdown files)
```

### 🔧 Technology Stack

- **Backend**: FastAPI + Uvicorn
- **RAG Engine**: LangChain + RetrievalQA
- **Vector DB**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: OpenAI text-embedding-3-small
- **LLM**: OpenAI GPT-4 (configurable)
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: pytest + TDD methodology

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone repository
git clone <repository-url>
cd rag-api

# Create Python virtual environment (Python 3.11 recommended)
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file:

```env
OPENAI_API_KEY=your-openai-api-key-here
JWT_SECRET_KEY=your-jwt-secret-key

# Optional configurations
CHUNK_SIZE=800
CHUNK_OVERLAP=100
RETRIEVAL_K=6
LLM_TEMPERATURE=0.3
LLM_MODEL=gpt-4
```

### 3. Prepare Your Knowledge Base

1. Clear the existing knowledge base:
   ```bash
   rm knowledge/*.md
   ```

2. Add your domain-specific documents:
   ```bash
   cp /path/to/your/documents/*.md knowledge/
   ```

3. Customize the prompt configuration:
   ```bash
   vim prompt/prompt.yaml
   ```

### 4. Build Vector Store

```bash
python3 run_etl.py
```

### 5. Start the Server

```bash
python3 server.py
```

### 6. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Command-line query tool
python3 query_cli.py "Your question here"

# Interactive mode
python3 query_cli.py --interactive
```

## 🎨 Customization Guide

### Adapting to Your Domain

1. **Knowledge Base**: Place your Markdown documents in the `knowledge/` directory
2. **Prompt Engineering**: Edit `prompt/prompt.yaml` to define your AI assistant's behavior
3. **Model Selection**: Update `LLM_MODEL` in `.env` (e.g., gpt-4, gpt-3.5-turbo)
4. **Embedding Strategy**: Adjust `CHUNK_SIZE` and `CHUNK_OVERLAP` for your content type

### Example Domains

- **Technical Documentation**: Software manuals, API docs, troubleshooting guides
- **Customer Support**: FAQs, product information, support procedures
- **Legal Documents**: Contracts, policies, regulatory compliance
- **Medical Knowledge**: Clinical guidelines, drug information, protocols
- **Educational Content**: Course materials, textbooks, research papers

## 📊 API Specification

### Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /login` - JWT authentication
- `POST /query` - Submit questions and get answers

### Query API Example

```bash
# Login
curl -X POST "http://localhost:8000/login?username=demo_user&password=demo_password"

# Submit query
curl -X POST "http://localhost:8000/query" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"query": "Your question here", "user_id": "user123"}'
```

### Response Format

```json
{
  "answer": "The detailed answer to your question...",
  "sources": ["document1.md", "document2.md"],
  "timestamp": "2025-01-04T10:30:00"
}
```

## 🧪 Testing

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test modules
python3 -m pytest tests/test_ingest.py -v
python3 -m pytest tests/test_server.py -v
```

## 🎯 Performance Optimization

### Vector Store Optimization

- **Chunk Size**: Adjust based on your content structure (default: 800 tokens)
- **Overlap**: Ensure context continuity (default: 100 tokens)
- **Retrieval Count**: Balance between context and performance (default: 6 chunks)

### LLM Configuration

- **Temperature**: Lower for factual responses (0.1-0.3), higher for creative (0.7-0.9)
- **Model Selection**: GPT-4 for complex reasoning, GPT-3.5-turbo for speed

## 🐳 Docker Deployment

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

Build and run:
```bash
docker build -t universal-rag-api .
docker run -p 8000:8000 --env-file .env universal-rag-api
```

## 🔒 Security Considerations

### 🚨 **IMPORTANT: Before Deployment**

1. **⚠️ API Keys Security**:
   ```bash
   # ❌ NEVER commit real API keys to git
   # ✅ Use environment variables
   export OPENAI_API_KEY=your-real-api-key-here
   
   # ✅ Or use secret management systems
   # AWS Secrets Manager, Azure Key Vault, etc.
   ```

2. **🔐 Authentication Configuration**:
   ```bash
   # Generate secure JWT secret (32+ characters)
   python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
   
   # Set secure demo credentials
   export DEMO_USERNAME=your-admin-username
   export DEMO_PASSWORD=your-secure-password
   ```

3. **🛡️ Production Security Checklist**:
   - [ ] Use HTTPS (TLS/SSL) for all communications
   - [ ] Generate unique, cryptographically secure JWT secret keys
   - [ ] Configure authentication credentials via environment variables
   - [ ] Enable rate limiting for API endpoints
   - [ ] Implement comprehensive input validation
   - [ ] Set up proper error handling (avoid information leakage)
   - [ ] Use secure headers (CORS, CSP, etc.)
   - [ ] Regular security audits and dependency updates

### 🔧 **Security Configuration**

- **JWT Security**: Tokens expire in 24 hours by default
- **FAISS Security**: Uses `allow_dangerous_deserialization=True` - ensure trusted data sources
- **Environment Variables**: All sensitive data configurable via environment variables
- **Default Credentials**: Changed from hardcoded to environment-based authentication

## 📈 Monitoring and Logging

- **Request Logging**: Track API usage and performance
- **Error Monitoring**: Capture and alert on failures
- **Vector Store Metrics**: Monitor retrieval effectiveness
- **LLM Usage**: Track token consumption and costs

## 🚀 Scaling Strategies

1. **Horizontal Scaling**: Deploy multiple API instances behind a load balancer
2. **Vector Store**: Consider migration to distributed solutions (Chroma, Pinecone)
3. **Caching**: Implement Redis for frequent queries
4. **Async Processing**: Use background jobs for heavy operations

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests using TDD approach
4. Implement your feature
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**: Ensure virtual environment is activated
2. **API Key Issues**: Verify OPENAI_API_KEY is set correctly
3. **Memory Errors**: Reduce chunk size or implement batch processing
4. **Slow Responses**: Consider using GPT-3.5-turbo or implementing caching

### Getting Help

- **Documentation**: This README and inline code comments
- **Issues**: GitHub Issues for bug reports and feature requests
- **Demos**: Run `python3 demo_runner.py` for interactive examples

---

**🚀 Build your own domain-specific AI assistant in minutes!**

*Powered by LangChain, FastAPI, and OpenAI*