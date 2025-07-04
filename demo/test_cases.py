#!/usr/bin/env python3
"""
🎯 Universal RAG System - Test Cases
Comprehensive test cases for presentations and demos
"""

import os
import requests
import json
import time
from datetime import datetime

class RAGTestCases:
    """Universal RAG System Test Cases"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.access_token = None
    
    def login(self):
        """Login and get access token"""
        # Get authentication information from environment variables
        username = os.getenv("DEMO_USERNAME", "admin")
        password = os.getenv("DEMO_PASSWORD", "change-this-password")
        login_data = {"username": username, "password": password}
        response = requests.post(f"{self.base_url}/login", params=login_data)
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get("access_token")
            print("✅ Login successful")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            return False
    
    def query(self, question, user_id="test_user"):
        """Send query to RAG system"""
        if not self.access_token:
            print("❌ Access token not set")
            return None
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        data = {
            "query": question,
            "user_id": user_id
        }
        
        start_time = time.time()
        response = requests.post(f"{self.base_url}/query", headers=headers, json=data)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            result["response_time"] = end_time - start_time
            return result
        else:
            print(f"❌ Query failed: {response.status_code}")
            return None

# Generic test questions for demonstrations
DEMO_TEST_QUESTIONS = [
    {
        "query": "What are the main concepts covered in the knowledge base?",
        "category": "Overview", 
        "expected_keywords": ["concept", "main", "overview"]
    },
    {
        "query": "How do I get started with this system?",
        "category": "Getting Started", 
        "expected_keywords": ["start", "begin", "setup"]
    },
    {
        "query": "What are the key features and capabilities?",
        "category": "Features", 
        "expected_keywords": ["feature", "capability", "function"]
    },
    {
        "query": "What are the system requirements?",
        "category": "Requirements", 
        "expected_keywords": ["requirement", "system", "need"]
    },
    {
        "query": "How can I configure this for my use case?",
        "category": "Configuration", 
        "expected_keywords": ["configure", "setup", "customize"]
    },
    {
        "query": "What are the best practices for implementation?",
        "category": "Best Practices", 
        "expected_keywords": ["practice", "recommendation", "guideline"]
    },
    {
        "query": "How do I troubleshoot common issues?",
        "category": "Troubleshooting", 
        "expected_keywords": ["troubleshoot", "issue", "problem"]
    },
    {
        "query": "What are the security considerations?",
        "category": "Security", 
        "expected_keywords": ["security", "safe", "protect"]
    }
]

# Live demo questions (replace with domain-specific ones)
LIVE_DEMO_QUESTIONS = [
    {
        "query": "What is the main purpose of this system?", 
        "category": "System Overview", 
        "expected_keywords": ["purpose", "system", "main"]
    },
    {
        "query": "How do I integrate this with my existing workflow?", 
        "category": "Integration", 
        "expected_keywords": ["integrate", "workflow", "existing"]
    },
    {
        "query": "What are the performance characteristics?", 
        "category": "Performance", 
        "expected_keywords": ["performance", "speed", "efficiency"]
    },
    {
        "query": "How do I scale this for larger deployments?", 
        "category": "Scalability", 
        "expected_keywords": ["scale", "large", "deployment"]
    }
]

def run_presentation_demo():
    """Run presentation demo"""
    print("=" * 80)
    print("🎯 Universal RAG System - Presentation Demo")
    print("=" * 80)
    
    # Prepare test system
    test_client = RAGTestCases()
    
    # Login
    print("🔐 Logging into system...")
    if not test_client.login():
        print("❌ Login failed")
        return
    
    print("\n📝 Running demonstration queries...")
    
    total_time = 0
    successful_queries = 0
    
    for i, question_data in enumerate(LIVE_DEMO_QUESTIONS, 1):
        print(f"\n🔍 Query {i}: {question_data['category']}")
        print(f"❓ Question: {question_data['query']}")
        
        result = test_client.query(question_data["query"])
        
        if result:
            successful_queries += 1
            response_time = result["response_time"]
            total_time += response_time
            answer_length = len(result["answer"])
            sources_count = len(result.get("sources", []))
            
            print(f"✅ Response: {answer_length} characters")
            print(f"⏱️  Time: {response_time:.2f}s")
            print(f"📚 Sources: {sources_count}")
            print(f"📄 Preview: {result['answer'][:100]}...")
        else:
            print("❌ Query failed")
        
        time.sleep(1)  # Rate limiting
    
    # Summary
    if successful_queries > 0:
        avg_time = total_time / successful_queries
        print(f"\n📊 Demo Summary:")
        print(f"✅ Successful queries: {successful_queries}/{len(LIVE_DEMO_QUESTIONS)}")
        print(f"⏱️  Average response time: {avg_time:.2f}s")
    
    print("\n" + "=" * 80)
    print("🎉 Presentation demo completed!")
    print("=" * 80)

def run_category_benchmark():
    """Category-wise benchmark test"""
    print("=" * 80)
    print("📊 Universal RAG System - Category Benchmark")
    print("=" * 80)
    
    test_client = RAGTestCases()
    
    if not test_client.login():
        print("❌ Login failed")
        return
    
    # Group questions by category
    categories = {}
    for question in DEMO_TEST_QUESTIONS:
        category = question["category"]
        if category not in categories:
            categories[category] = []
        categories[category].append(question)
    
    overall_stats = {
        "total_time": 0,
        "total_queries": 0,
        "total_answer_length": 0,
        "total_sources": 0
    }
    
    for category, questions in categories.items():
        print(f"\n📂 Category: {category}")
        print("-" * 50)
        
        category_time = 0
        category_answers = 0
        category_length = 0
        category_sources = 0
        
        for question_data in questions:
            print(f"❓ {question_data['query']}")
            
            result = test_client.query(question_data["query"])
            
            if result:
                response_time = result["response_time"]
                answer_length = len(result["answer"])
                sources_count = len(result.get("sources", []))
                
                category_time += response_time
                category_answers += 1
                category_length += answer_length
                category_sources += sources_count
                
                print(f"   ✅ {response_time:.2f}s, {answer_length} chars, {sources_count} sources")
            else:
                print("   ❌ Failed")
            
            time.sleep(0.5)
        
        if category_answers > 0:
            avg_time = category_time / category_answers
            avg_length = category_length / category_answers
            print(f"📊 Category avg: {avg_time:.2f}s, {avg_length:.0f} chars, {category_sources} sources")
            
            overall_stats["total_time"] += category_time
            overall_stats["total_queries"] += category_answers
            overall_stats["total_answer_length"] += category_length
            overall_stats["total_sources"] += category_sources
    
    # Overall summary
    if overall_stats["total_queries"] > 0:
        overall_avg_time = overall_stats["total_time"] / overall_stats["total_queries"]
        overall_avg_length = overall_stats["total_answer_length"] / overall_stats["total_queries"]
        
        print(f"\n📈 Overall Performance:")
        print(f"🔢 Total questions: {overall_stats['total_queries']}")
        print(f"⏱️  Average response: {overall_avg_time:.2f}s")
        print(f"📝 Average answer length: {overall_avg_length:.0f} chars")
        print(f"📚 Total sources referenced: {overall_stats['total_sources']}")
        print(f"📊 Source utilization: {(overall_stats['total_sources']/overall_stats['total_queries']):.1f} sources/query")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Universal RAG System Test Cases")
    parser.add_argument("--demo", action="store_true", help="Run presentation demo")
    parser.add_argument("--benchmark", action="store_true", help="Run category benchmark")
    
    args = parser.parse_args()
    
    if args.demo:
        run_presentation_demo()
    elif args.benchmark:
        run_category_benchmark()
    else:
        print("Please specify --demo or --benchmark")
        parser.print_help()