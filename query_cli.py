#!/usr/bin/env python3
"""
Universal RAG API - Command Line Query Tool
"""

import argparse
import json
import os
import requests
import sys
from datetime import datetime
import urllib.parse


class RAGQueryCLI:
    """Universal RAG API Command Line Interface"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.access_token = None
        
    def login(self, username=None, password=None):
        """ログインしてアクセストークンを取得"""
        # Get authentication information from environment variables（引数で上書き可能）
        username = username or os.getenv("DEMO_USERNAME", "admin")
        password = password or os.getenv("DEMO_PASSWORD", "change-this-password")
        
        try:
            url = f"{self.base_url}/login"
            params = {"username": username, "password": password}
            response = requests.post(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                print("✅ ログイン成功")
                return True
            else:
                print(f"❌ ログイン失敗: {response.status_code}")
                print(response.text)
                return False
                
        except Exception as e:
            print(f"❌ ログインエラー: {e}")
            return False
    
    def query(self, question, user_id="cli_user"):
        """質問をRAGサーバーに送信"""
        if not self.access_token:
            print("❌ アクセストークンが設定されていません")
            return None
            
        try:
            url = f"{self.base_url}/query"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}"
            }
            data = {
                "query": question,
                "user_id": user_id
            }
            
            print(f"🤔 質問を送信中: {question}")
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ クエリ失敗: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"❌ クエリエラー: {e}")
            return None
    
    def format_response(self, response_data):
        """回答を整形して表示"""
        if not response_data:
            return
            
        print("\n" + "="*80)
        print("🎯 RAG Assistant Response")
        print("="*80)
        print(f"📝 Answer: {response_data.get('answer', 'N/A')}")
        print()
        
        sources = response_data.get('sources', [])
        if sources:
            print("📚 参考資料:")
            for i, source in enumerate(sources, 1):
                # ファイル名だけを表示
                filename = source.split('/')[-1] if '/' in source else source
                print(f"  {i}. {filename}")
        
        timestamp = response_data.get('timestamp', '')
        if timestamp:
            print(f"\n⏰ 回答時刻: {timestamp}")
        
        print("="*80)
    
    def health_check(self):
        """サーバーの健康状態をチェック"""
        try:
            url = f"{self.base_url}/health"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                print("🟢 サーバー状態: 正常")
                print(f"   ベクトルストア: {'✅' if data.get('vector_store_loaded') else '❌'}")
                print(f"   QAチェーン: {'✅' if data.get('qa_chain_ready') else '❌'}")
                return True
            else:
                print(f"❌ サーバー接続失敗: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ サーバー接続エラー: {e}")
            return False


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description="Universal RAG API - Command Line Query Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 質問を引数で指定
  python3 query_cli.py "What are the main features of this system?"
  
  # 対話モードで質問
  python3 query_cli.py --interactive
  
  # サーバーの健康状態をチェック
  python3 query_cli.py --health
        """
    )
    
    parser.add_argument(
        "question",
        nargs="?",
        help="Question to ask the RAG system"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="対話モードで質問を入力"
    )
    
    parser.add_argument(
        "--health",
        action="store_true",
        help="サーバーの健康状態をチェック"
    )
    
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="RAGサーバーのURL (デフォルト: http://localhost:8000)"
    )
    
    args = parser.parse_args()
    
    # Initialize Universal RAG CLI
    cli = RAGQueryCLI(args.url)
    
    # ヘルスチェック
    if args.health:
        cli.health_check()
        return
    
    # サーバーの状態確認
    if not cli.health_check():
        print("❌ サーバーに接続できません。サーバーが起動していることを確認してください。")
        sys.exit(1)
    
    # ログイン
    if not cli.login():
        print("❌ ログインに失敗しました。")
        sys.exit(1)
    
    # 対話モード
    if args.interactive:
        print("\n🤖 Universal RAG API - Interactive Mode")
        print("質問を入力してください。終了するには 'quit' または 'exit' を入力してください。")
        print("-" * 60)
        
        while True:
            try:
                question = input("\n❓ Question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 お疲れ様でした！")
                    break
                
                if not question:
                    print("⚠️ 質問を入力してください。")
                    continue
                
                # 質問を送信
                response = cli.query(question)
                cli.format_response(response)
                
            except KeyboardInterrupt:
                print("\n👋 お疲れ様でした！")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")
    
    # 引数で質問が指定された場合
    elif args.question:
        response = cli.query(args.question)
        cli.format_response(response)
    
    # 引数が指定されていない場合
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 