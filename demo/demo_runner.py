#!/usr/bin/env python3
"""
🎯 RAG Starter Kit - Comprehensive Live Demo Script
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import requests
import json
from dotenv import load_dotenv
import argparse

# Load environment variables from .env file
load_dotenv()

def print_banner():
    """Display demo banner"""
    print("=" * 80)
    print("🎯 RAG Starter Kit - Comprehensive Live Demo")
    print("=" * 80)
    print("🚀 Educational RAG system demonstration with TDD methodology")
    print("📚 Knowledge Base × LangChain × OpenAI GPT-4")
    print("=" * 80)

def check_requirements():
    """Check required settings"""
    print("\n🔍 Checking system requirements...")
    
    # Check OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY is not set.")
        print("📋 Setup instructions:")
        print("   Add OPENAI_API_KEY=your-api-key-here to .env file")
        return False
    else:
        print(f"✅ OPENAI_API_KEY: {api_key[:20]}...{api_key[-10:]}")
    
    # Check required directories
    knowledge_dir = Path("knowledge")
    if not knowledge_dir.exists():
        print("❌ knowledge directory not found.")
        return False
    
    md_files = list(knowledge_dir.glob("*.md"))
    if not md_files:
        print("❌ No Markdown files found in knowledge directory.")
        return False
    else:
        print(f"✅ Knowledge files: {len(md_files)} Markdown files")
        for md_file in md_files[:3]:  # Show first 3 files
            print(f"   📄 {md_file.name}")
        if len(md_files) > 3:
            print(f"   ... and {len(md_files)-3} more")
    
    # Check required modules
    required_modules = [
        ("fastapi", "FastAPI"),
        ("langchain", "LangChain"),
        ("openai", "OpenAI"),
        ("faiss", "FAISS"),
        ("uvicorn", "Uvicorn"),
        ("requests", "Requests")
    ]
    
    missing_modules = []
    for module_name, display_name in required_modules:
        try:
            __import__(module_name)
            print(f"✅ {display_name}: Installed")
        except ImportError:
            missing_modules.append(module_name)
            print(f"❌ {display_name}: Not installed")
    
    if missing_modules:
        print(f"\n📋 Missing modules: {', '.join(missing_modules)}")
        print("   Install command: pip install -r requirements.txt")
        return False
    
    return True

def run_etl_process(skip_if_exists=True):
    """Run ETL process"""
    print("\n🚀 Starting ETL process...")
    
    # Check existing vector store
    vector_store_path = Path("vector_store")
    if vector_store_path.exists() and skip_if_exists:
        print(f"✅ Existing vector store '{vector_store_path}' found.")
        print("   Skipping ETL process.")
        return True
    
    try:
        # Run ETL process
        print("📚 Processing knowledge files...")
        result = subprocess.run(
            [sys.executable, "run_etl.py"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print("✅ ETL process completed successfully.")
            # Parse success output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'file' in line.lower() or 'document' in line.lower() or 'vector' in line.lower():
                    print(f"   {line}")
            return True
        else:
            print("❌ ETL process encountered errors.")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ ETL process timed out.")
        return False
    except Exception as e:
        print(f"❌ ETL process execution error: {e}")
        return False

def start_server():
    """Start RAG server"""
    print("\n🚀 Starting RAG server...")
    
    try:
        # Start server in background
        process = subprocess.Popen(
            [sys.executable, "server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for server startup
        print("⏳ Waiting for server startup...")
        max_retries = 15
        for i in range(max_retries):
            time.sleep(2)
            try:
                response = requests.get("http://localhost:8000/health", timeout=3)
                if response.status_code == 200:
                    print("✅ Server started successfully.")
                    health_data = response.json()
                    print(f"   🔗 Server URL: http://localhost:8000")
                    print(f"   📊 Vector store: {health_data.get('vector_store_loaded', 'N/A')}")
                    print(f"   🤖 QA chain: {health_data.get('qa_chain_ready', 'N/A')}")
                    return process
            except requests.RequestException:
                print(f"   ⏳ Startup check... ({i+1}/{max_retries})")
                continue
        
        # Startup failed
        print("❌ Server startup failed.")
        process.terminate()
        return None
            
    except Exception as e:
        print(f"❌ Server startup error: {e}")
        return None

def run_comprehensive_demo_tests(server_process):
    """Run comprehensive demo tests"""
    print("\n🧪 Starting comprehensive demo tests...")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. Root endpoint test
        print("\n1️⃣ Root endpoint (/) test")
        print("   " + "-" * 50)
        response = requests.get(f"{base_url}/")
        print(f"   ✅ Status: {response.status_code}")
        root_data = response.json()
        print(f"   📝 Service: {root_data.get('message')}")
        print(f"   📅 Timestamp: {root_data.get('timestamp')}")
        
        # 2. Health check endpoint test
        print("\n2️⃣ Health check (/health) test")
        print("   " + "-" * 50)
        response = requests.get(f"{base_url}/health")
        print(f"   ✅ Status: {response.status_code}")
        health_data = response.json()
        print(f"   🔧 System status: {health_data.get('status')}")
        print(f"   📚 Vector store: {health_data.get('vector_store_loaded')}")
        print(f"   🤖 QA chain: {health_data.get('qa_chain_ready')}")
        
        # 3. Login endpoint test
        print("\n3️⃣ Login (/login) test")
        print("   " + "-" * 50)
        # Get authentication information from environment variables
        username = os.getenv("DEMO_USERNAME", "admin")
        password = os.getenv("DEMO_PASSWORD", "change-this-password")
        login_data = {"username": username, "password": password}
        response = requests.post(f"{base_url}/login", params=login_data)
        
        if response.status_code == 200:
            print("   ✅ Login successful")
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"   🔑 JWT token: {access_token[:30]}...")
            
            # 4. Demo question tests
            print("\n4️⃣ Demo question tests")
            print("   " + "-" * 50)
            
            demo_questions = [
                {
                    "query": "What are the main features of this system?",
                    "category": "System Overview"
                },
                {
                    "query": "How do I configure this for my specific use case?",
                    "category": "Configuration"
                },
                {
                    "query": "What are the best practices for implementation?",
                    "category": "Best Practices"
                },
                {
                    "query": "How do I troubleshoot common issues?",
                    "category": "Troubleshooting"
                }
            ]
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            for i, question in enumerate(demo_questions, 1):
                print(f"\n   📝 Question {i} ({question['category']})")
                print(f"   Q: {question['query']}")
                
                query_data = {
                    "query": question["query"],
                    "user_id": username
                }
                
                try:
                    response = requests.post(
                        f"{base_url}/query",
                        json=query_data,
                        headers=headers,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        answer = result['answer']
                        sources = result.get('sources', [])
                        
                        print(f"   ✅ Response retrieved successfully")
                        print(f"   📝 Answer: {answer[:150]}...")
                        print(f"   📚 Reference sources: {len(sources)}")
                        if sources:
                            print(f"   📄 Main source: {sources[0][:50]}...")
                        
                        # Response quality evaluation
                        if len(answer) > 200:
                            print(f"   🏆 Response quality: Detailed ({len(answer)} chars)")
                        else:
                            print(f"   ⚠️  Response quality: Concise ({len(answer)} chars)")
                        
                    else:
                        print(f"   ❌ Response retrieval failed: {response.status_code}")
                        
                except requests.RequestException as e:
                    print(f"   ❌ Question processing error: {e}")
                
                time.sleep(1)  # API rate limiting
            
            # 5. Performance test
            print("\n5️⃣ Performance test")
            print("   " + "-" * 50)
            
            test_query = {
                "query": "What is the main purpose of this system?",
                "user_id": "performance_test"
            }
            
            response_times = []
            for i in range(3):
                start_time = time.time()
                response = requests.post(
                    f"{base_url}/query",
                    json=test_query,
                    headers=headers,
                    timeout=30
                )
                end_time = time.time()
                
                if response.status_code == 200:
                    response_time = end_time - start_time
                    response_times.append(response_time)
                    print(f"   ⏱️  Test {i+1}: {response_time:.2f}s")
                else:
                    print(f"   ❌ Test {i+1}: Failed")
            
            if response_times:
                avg_time = sum(response_times) / len(response_times)
                print(f"   📊 Average response time: {avg_time:.2f}s")
                
                if avg_time < 3.0:
                    print("   🏆 Performance: Excellent")
                elif avg_time < 5.0:
                    print("   ✅ Performance: Good")
                else:
                    print("   ⚠️  Performance: Needs improvement")
                
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Demo test execution error: {e}")
    
    finally:
        # Terminate server
        print("\n🛑 Terminating server...")
        server_process.terminate()
        server_process.wait()
        print("✅ Server terminated successfully.")

def interactive_demo():
    """Interactive demo mode"""
    print("\n🎮 Starting interactive demo mode...")
    print("   Server will start and remain available for manual testing.")
    print("   Use the following commands in separate terminals:")
    print("   - python3 query_cli.py --interactive")
    print("   - curl -X GET http://localhost:8000/docs")
    print("   - curl -X GET http://localhost:8000/health")
    print("\n   Press Ctrl+C to terminate server.")
    
    server_process = start_server()
    if server_process:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Terminating interactive demo...")
            server_process.terminate()
            server_process.wait()
            print("✅ Server terminated successfully.")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="RAG Starter Kit - Comprehensive Live Demo"
    )
    parser.add_argument(
        "--interactive", 
        action="store_true",
        help="Interactive demo mode (for manual testing)"
    )
    parser.add_argument(
        "--skip-etl", 
        action="store_true",
        help="Skip ETL process (use existing vector store)"
    )
    
    args = parser.parse_args()
    
    # Display banner
    print_banner()
    
    # 1. Requirements check
    if not check_requirements():
        print("\n❌ Required settings are missing. Please follow the above instructions.")
        return
    
    # 2. ETL process
    if not run_etl_process(skip_if_exists=args.skip_etl):
        print("\n❌ ETL process failed.")
        return
    
    # 3. Interactive mode or automatic demo
    if args.interactive:
        interactive_demo()
    else:
        # 4. Start server
        server_process = start_server()
        if server_process is None:
            print("\n❌ Server startup failed.")
            return
        
        # 5. Run comprehensive demo tests
        run_comprehensive_demo_tests(server_process)
        
        # 6. Demo completion
        print("\n" + "=" * 80)
        print("🎉 Comprehensive live demo completed!")
        print("=" * 80)
        print("\n📋 Manual testing information:")
        print("   🔗 Server URL: http://localhost:8000")
        print("   📖 API docs: http://localhost:8000/docs")
        print(f"   🔑 Login: username={username}, password=***")
        print("   🖥️  Command line: python3 query_cli.py --interactive")
        print("\n💡 Manual server startup:")
        print("   python3 server.py")
        print("\n🎯 Next steps:")
        print("   - Docker deployment: docker build -t rag-starter-kit .")
        print("   - Integration: Use the REST API endpoints")
        print("   - Customization: Replace knowledge files and prompts")

if __name__ == "__main__":
    main()