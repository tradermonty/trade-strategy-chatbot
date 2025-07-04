# 🎓 RAG Starter Kit

**Learn RAG technology by building your own AI assistant in 10 minutes**

*A beginner-friendly, educational starter template for understanding and implementing Retrieval-Augmented Generation (RAG) systems*

🇺🇸 English | [🇯🇵 日本語](README_ja.md)

**🔗 Repository**: https://github.com/takusaotome/rag-starter-kit

## 📖 Overview

The RAG Starter Kit is designed to help developers learn and understand RAG technology through hands-on implementation. Perfect for students, educators, and developers new to AI who want to build their first intelligent assistant.

**🎯 What you'll learn:**
- How RAG (Retrieval-Augmented Generation) works
- Vector embeddings and semantic search
- LLM integration and prompt engineering
- Building production-ready APIs with FastAPI
- Authentication and security best practices

**🚀 What you'll build:**
A complete AI assistant that can answer questions about your custom knowledge base in under 10 minutes.

### 🎯 Why RAG Starter Kit?

- **📚 Educational First**: Clear, commented code with step-by-step explanations
- **🚀 Quick Start**: From zero to working AI assistant in 10 minutes
- **🔧 Hands-On Learning**: Build while you learn core RAG concepts
- **🌉 Bridge to Production**: Foundation for more complex systems
- **📖 Complete Tutorial**: Includes Japanese recipe knowledge base as example
- **🎨 Customizable**: Easy to adapt for your own use cases
- **🔐 Security Included**: JWT authentication and best practices
- **💡 Best Practices**: Modern Python, FastAPI, and AI development patterns

## 🎯 プロジェクトの特徴

### ✨ 独自の価値

- 🎓 **教育的優秀性**: TDD手法、包括的ドキュメント
- ⚡ **即座に利用可能**: 複雑な設定不要
- 🎨 **カスタマイズ性**: YAML設定、ドメイン非依存
- 🍜 **実例豊富**: 日本料理レシピによる実用デモ
- 🔄 **効率的更新**: インクリメンタル更新機能


## 🏗️ Learning Architecture

*Understanding how RAG systems work under the hood*

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

*Modern, industry-standard tools for learning*

- **Backend**: FastAPI + Uvicorn *(Learn API development)*
- **RAG Engine**: LangChain + RetrievalQA *(Understand RAG patterns)*
- **Vector DB**: FAISS *(Learn semantic search)*
- **Embeddings**: OpenAI text-embedding-3-small *(Understand vector representations)*
- **LLM**: OpenAI GPT-4 *(Experience with modern AI)*
- **Authentication**: JWT *(Learn security fundamentals)*
- **Testing**: pytest + TDD *(Best practices included)*

## 🚀 Quick Start - Your First AI Assistant

*Follow these steps to build your first RAG-powered AI assistant*

### 1. Environment Setup

```bash
# Clone the starter kit
git clone https://github.com/takusaotome/rag-starter-kit.git
cd rag-starter-kit

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
LLM_MODEL=gpt-4o
```

### 3. Explore the Sample Knowledge Base

**📚 Pre-loaded Example: Japanese Recipe Collection**

The starter kit comes with a complete Japanese recipe knowledge base to help you understand how RAG works:

```bash
# Explore the sample knowledge base
ls knowledge/
# You'll see: 01_basic_rice_dishes.md, 02_noodle_dishes.md, etc.

# View a sample document
cat knowledge/01_basic_rice_dishes.md
```

**🎯 Learning Opportunity**: See how structured knowledge is organized for optimal RAG retrieval.

**🔄 Customize Later**: Replace with your own documents once you understand the structure.

### 4. Build Vector Store *(Learn Embeddings)*

```bash
# Transform documents into searchable vectors
python3 run_etl.py

# 🎓 What happens here:
# 1. Documents are split into chunks
# 2. Each chunk becomes a vector embedding
# 3. FAISS index is created for fast similarity search
```

### 5. Start Your AI Assistant

```bash
# Launch your RAG-powered API
python3 server.py

# 🎉 Your AI assistant is now running!
# Visit: http://localhost:8000/docs for interactive API documentation
```

### 6. Ask Your First Question

```bash
# Health check
curl http://localhost:8000/health

# Try asking about Japanese cuisine
python3 query_cli.py "How do you make oyakodon?"

# Interactive mode for exploration
python3 query_cli.py --interactive

# 🎓 Try these learning questions:
# "What are the main types of Japanese rice dishes?"
# "How do you make perfect sushi rice?"
# "What's the difference between ramen and udon?"
```

## 🎨 Customization Guide - Make It Your Own

*Once you understand the basics, customize for your domain*

### 🔄 Adapting to Your Domain

*Step-by-step guide to creating your custom AI assistant*

1. **📚 Replace Knowledge Base**: 
   ```bash
   # Clear sample data
   rm knowledge/*.md
   
   # Add your documents
   cp /path/to/your/docs/*.md knowledge/
   ```

2. **🎨 Customize AI Behavior**:
   ```bash
   # Edit the prompt configuration
   vim prompt/prompt.yaml
   
   # 🎓 Learning tip: See how prompts shape AI responses
   ```

3. **⚙️ Optimize Performance**:
   ```bash
   # Adjust settings in .env
   LLM_MODEL=gpt-3.5-turbo  # For cost-effective learning
   CHUNK_SIZE=1000          # For longer documents
   ```

4. **🔄 Rebuild and Test**:
   ```bash
   python3 run_etl.py  # Rebuild vector store
   python3 server.py   # Test your custom assistant
   ```

### 🎯 Learning Project Ideas

*Practice RAG development with these domains*

- **📖 Personal Knowledge Base**: Your notes, research, documentation
- **🏢 Company FAQ**: Internal knowledge, policies, procedures
- **🎓 Study Assistant**: Course materials, textbooks, research papers
- **🍳 Recipe Collection**: Like our Japanese example, but your cuisine
- **💼 Technical Documentation**: API docs, troubleshooting guides
- **📚 Book Summary**: Create assistants for your favorite books

**🎓 Educational Value**: Each domain teaches different aspects of RAG optimization

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

## 🧪 Testing - Learn Through Validation

*Understanding how to test AI systems*

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test modules
python3 -m pytest tests/test_ingest.py -v
python3 -m pytest tests/test_server.py -v
```

## 🎯 Performance Optimization - Advanced Learning

*Master the art of RAG tuning*

### Vector Store Optimization

- **Chunk Size**: Adjust based on your content structure (default: 800 tokens)
- **Overlap**: Ensure context continuity (default: 100 tokens)
- **Retrieval Count**: Balance between context and performance (default: 6 chunks)

### LLM Configuration

- **Temperature**: Lower for factual responses (0.1-0.3), higher for creative (0.7-0.9)
- **Model Selection**: GPT-4 for complex reasoning, GPT-3.5-turbo for speed

## 🐳 Docker Deployment - Production Skills

*Learn containerization for AI applications*

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
docker build -t rag-starter-kit .
docker run -p 8000:8000 --env-file .env rag-starter-kit
```

## 🔒 Security Considerations - Essential Knowledge

*Learn to build secure AI applications*

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

## 📈 Monitoring and Logging - Production Skills

*Learn to monitor AI systems in production*

- **Request Logging**: Track API usage and performance
- **Error Monitoring**: Capture and alert on failures
- **Vector Store Metrics**: Monitor retrieval effectiveness
- **LLM Usage**: Track token consumption and costs

## 🚀 Scaling Strategies - Advanced Topics

*From starter kit to production system*

1. **Horizontal Scaling**: Deploy multiple API instances behind a load balancer
2. **Vector Store**: Consider migration to distributed solutions (Chroma, Pinecone)
3. **Caching**: Implement Redis for frequent queries
4. **Async Processing**: Use background jobs for heavy operations

## 🤝 Contributing - Join the Learning Community

*Help others learn RAG technology*

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests using TDD approach
4. Implement your feature
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛠️ Troubleshooting - Common Learning Issues

*Solutions to help you keep learning*

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

## 📖 Educational Resources - Learn More About RAG

*Deep dive into RAG technology with our comprehensive learning materials*

### 🍜 Featured Article: "AIおばあちゃんの作り方"

**📝 Beginner-Friendly RAG Tutorial**: We've created a comprehensive, story-driven article that teaches RAG fundamentals through an engaging narrative. Perfect for beginners who want to understand the technology while building a practical AI assistant.

**📍 Location**: [`article/rag-chatbot-story.md`](article/rag-chatbot-story.md)

**🎯 What you'll learn**:
- RAG concepts explained through storytelling
- Step-by-step implementation guide
- Real-world customization examples
- Best practices and troubleshooting
- Advanced features and optimization

**📋 Learning Tools**:
- **Progress Tracking**: [`article/learning-checklist.md`](article/learning-checklist.md)
- **Guide Overview**: [`article/README.md`](article/README.md)

**🌟 Why read it**:
- Story-driven approach makes complex concepts enjoyable
- Written specifically for beginners
- Includes practical exercises and challenges
- Covers both theory and hands-on implementation

```bash
# Start your learning journey
cd article
open rag-chatbot-story.md  # or use your preferred markdown viewer
```

---

## 🎓 Next Steps - Your Learning Journey

**🚀 You've built your first RAG system! What's next?**

### Immediate Next Steps:
1. **🔄 Customize**: Replace the Japanese recipes with your own knowledge base
2. **🎨 Experiment**: Try different prompt configurations
3. **📊 Optimize**: Adjust chunk sizes and retrieval parameters
4. **🔐 Secure**: Implement proper authentication for production use

### Advanced Learning:
- **🔧 Enterprise Features**: Study [danny-avila/rag_api](https://github.com/danny-avila/rag_api) for production-grade implementation
- **🧠 Custom Models**: Learn to fine-tune models for your domain
- **📈 Scaling**: Explore distributed vector stores and multi-model architectures
- **🔍 Hybrid Search**: Combine semantic and keyword search strategies

### Community Resources:
- **💬 Discussions**: Share your customizations and ask questions
- **📚 Examples**: See how others have adapted the starter kit
- **🎯 Challenges**: Weekly RAG implementation challenges

---

**🎉 Congratulations! You've learned RAG technology by building!**

*RAG Starter Kit - From Zero to AI Assistant in 10 minutes*

*Powered by LangChain, FastAPI, and OpenAI*