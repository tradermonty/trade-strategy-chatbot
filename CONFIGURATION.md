# RAG Starter Kit - Configuration Guide

This guide explains how to configure the RAG Starter Kit for different domains and use cases.

## 📁 Configuration Files Overview

The system includes several pre-configured environment files for different domains:

- **`.env.example`** - Template with all available settings and examples
- **`.env.medical`** - Medical knowledge assistant configuration
- **`.env.legal`** - Legal document assistant configuration  
- **`.env.support`** - Customer support assistant configuration
- **`.env.tech`** - Technical documentation assistant configuration

## 🚀 Quick Start

### 1. Choose Your Domain

Select the appropriate configuration file for your use case:

```bash
# For medical knowledge base
cp .env.medical .env

# For legal documents
cp .env.legal .env

# For customer support
cp .env.support .env

# For technical documentation
cp .env.tech .env

# For custom configuration
cp .env.example .env
```

### 2. Update Required Settings

Edit your `.env` file and update the required values:

```bash
# Add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-api-key-here

# Generate a secure JWT secret for production
JWT_SECRET_KEY=your-secure-random-string-here
```

### 3. Prepare Your Content

Create the appropriate directory structure based on your configuration:

```bash
# Example for medical configuration
mkdir -p knowledge/medical
mkdir -p prompts/medical
mkdir -p vector_store/medical

# Add your markdown files to knowledge/medical/
# Add your prompt configuration to prompts/medical/medical_assistant.yaml
```

## ⚙️ Configuration Parameters

### Core Paths

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `KNOWLEDGE_PATH` | Directory containing your .md files | `knowledge` | `knowledge/medical` |
| `PROMPTS_PATH` | Directory containing prompt configs | `prompt` | `prompts/medical` |
| `PROMPT_FILE` | Name of the prompt configuration file | `prompt.yaml` | `medical_assistant.yaml` |
| `VECTOR_STORE_PATH` | Directory for processed embeddings | `vector_store` | `vector_store/medical` |

### Server Configuration

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `HOST` | Server host address | `0.0.0.0` | `localhost` |
| `PORT` | Server port number | `8000` | `8080` |
| `SERVER_URL` | Public server URL | `http://0.0.0.0:8000` | `https://api.example.com` |
| `CLIENT_URL` | Client connection URL | `http://localhost:8000` | `https://api.example.com` |

### Processing Settings

| Parameter | Description | Default | Recommended Range |
|-----------|-------------|---------|-------------------|
| `CHUNK_SIZE` | Size of text chunks (tokens) | `800` | 400-1500 |
| `CHUNK_OVERLAP` | Overlap between chunks (tokens) | `100` | 50-300 |
| `RETRIEVAL_K` | Number of chunks to retrieve | `6` | 3-10 |

### LLM Settings

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `LLM_MODEL` | OpenAI model to use | `gpt-4o` | `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `o1-preview`, `o1-mini` |
| `LLM_TEMPERATURE` | Response creativity (0.0-1.0) | `0.3` | 0.1 (factual) - 0.9 (creative) |

## 🎯 Domain-Specific Recommendations

### Medical/Healthcare
```bash
CHUNK_SIZE=1000          # Larger context for medical information
CHUNK_OVERLAP=150        # High overlap for terminology
RETRIEVAL_K=4            # Focused, accurate results
LLM_TEMPERATURE=0.1      # Very factual responses
LLM_MODEL=gpt-4o         # Latest high-accuracy model
```

### Legal Documents
```bash
CHUNK_SIZE=1200          # Large chunks for legal context
CHUNK_OVERLAP=200        # High overlap for citations
RETRIEVAL_K=6            # Comprehensive research
LLM_TEMPERATURE=0.2      # Precise legal language
LLM_MODEL=gpt-4o         # Latest model for complex legal text
```

### Customer Support
```bash
CHUNK_SIZE=600           # Quick, focused answers
CHUNK_OVERLAP=80         # Moderate overlap
RETRIEVAL_K=4            # Most relevant solutions
LLM_TEMPERATURE=0.5      # Helpful, friendly responses
LLM_MODEL=gpt-4o-mini    # Cost-effective latest model
```

### Technical Documentation
```bash
CHUNK_SIZE=800           # Good for code examples
CHUNK_OVERLAP=120        # Overlap for code context
RETRIEVAL_K=8            # Comprehensive technical info
LLM_TEMPERATURE=0.4      # Balanced for examples
LLM_MODEL=gpt-4o         # Latest model with code understanding
```

### Production Deployment
```bash
# Production server configuration
HOST=0.0.0.0
PORT=8000
SERVER_URL=https://your-domain.com
CLIENT_URL=https://your-domain.com

# For local development
HOST=localhost
PORT=8000
SERVER_URL=http://localhost:8000
CLIENT_URL=http://localhost:8000
```

## 🔄 Switching Between Configurations

You can easily switch between different configurations:

```bash
# Switch to medical configuration
cp .env.medical .env
python3 run_etl.py  # Rebuild vector store if needed
python3 server.py

# Switch to legal configuration
cp .env.legal .env
python3 run_etl.py  # Rebuild vector store if needed
python3 server.py
```

## 🐳 Docker Configuration

For Docker deployments, you can specify environment files:

```bash
# Build with medical configuration
docker build -t rag-medical .
docker run --env-file .env.medical -p 8000:8000 rag-medical

# Build with legal configuration  
docker build -t rag-legal .
docker run --env-file .env.legal -p 8000:8000 rag-legal
```

## 🔒 Security Considerations

### Production Settings

For production deployments:

1. **Generate a secure JWT secret:**
   ```bash
   # Linux/Mac
   openssl rand -hex 32
   
   # Or use Python
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Configure authentication credentials:**
   ```bash
   # Set secure authentication (replacing default demo credentials)
   export DEMO_USERNAME=your-admin-username
   export DEMO_PASSWORD=your-secure-password
   export JWT_SECRET_KEY=your-secure-32-character-secret-here
   ```

3. **Consider using secret management:**
   - AWS Secrets Manager
   - Azure Key Vault
   - Google Secret Manager
   - Kubernetes Secrets

### Environment Variables

You can also set these as system environment variables instead of using `.env` files:

```bash
export OPENAI_API_KEY=sk-your-key-here
export KNOWLEDGE_PATH=knowledge/medical
export LLM_TEMPERATURE=0.1
python3 server.py
```

## 🧪 Testing Configuration

Test your configuration:

```bash
# Run health check
curl http://localhost:8000/health

# Test with CLI
python3 query_cli.py "Test question for your domain"

# Run demo
python3 demo_runner.py --skip-etl
```

## 🛠️ Troubleshooting

### Common Issues

1. **Vector store not found:**
   - Run `python3 run_etl.py` to rebuild
   - Check `VECTOR_STORE_PATH` setting

2. **Prompt file not found:**
   - Check `PROMPTS_PATH` and `PROMPT_FILE` settings
   - Ensure the file exists at the specified path

3. **No knowledge files:**
   - Check `KNOWLEDGE_PATH` setting
   - Ensure `.md` files exist in the directory

4. **API key errors:**
   - Verify `OPENAI_API_KEY` is set correctly
   - Check API key permissions and billing

For more help, see the main [README.md](README.md) or run:
```bash
python3 demo_runner.py --help
python3 query_cli.py --help
```