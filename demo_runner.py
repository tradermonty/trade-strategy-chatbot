#!/usr/bin/env python3
"""
🎯 PM実務コンシェルジュ RAG システム - 包括的ライブデモスクリプト
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

# .envファイルから環境変数を読み込み
load_dotenv()

def print_banner():
    """デモバナーを表示"""
    print("=" * 80)
    print("🎯 PM実務コンシェルジュ RAG システム - 包括的ライブデモ")
    print("=" * 80)
    print("🚀 TDD手法で開発されたRAGシステムの実働デモンストレーション")
    print("📚 9つのPMナレッジファイル × LangChain × OpenAI GPT-4")
    print("=" * 80)

def check_requirements():
    """必要な設定の確認"""
    print("\n🔍 システム要件を確認中...")
    
    # OpenAI APIキーの確認
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEYが設定されていません。")
        print("📋 設定方法:")
        print("   .env ファイルに OPENAI_API_KEY=your-api-key-here を記載")
        return False
    else:
        print(f"✅ OPENAI_API_KEY: {api_key[:20]}...{api_key[-10:]}")
    
    # 必要なディレクトリの確認
    knowledge_dir = Path("knowledge")
    if not knowledge_dir.exists():
        print("❌ knowledgeディレクトリが見つかりません。")
        return False
    
    md_files = list(knowledge_dir.glob("*.md"))
    if not md_files:
        print("❌ knowledgeディレクトリにMarkdownファイルが見つかりません。")
        return False
    else:
        print(f"✅ ナレッジファイル: {len(md_files)}個のMarkdownファイル")
        for md_file in md_files[:3]:  # 最初の3つを表示
            print(f"   📄 {md_file.name}")
        if len(md_files) > 3:
            print(f"   ... 他{len(md_files)-3}個")
    
    # 必要なモジュールの確認
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
            print(f"✅ {display_name}: インストール済み")
        except ImportError:
            missing_modules.append(module_name)
            print(f"❌ {display_name}: 未インストール")
    
    if missing_modules:
        print(f"\n📋 未インストールモジュール: {', '.join(missing_modules)}")
        print("   インストールコマンド: pip install -r requirements.txt")
        return False
    
    return True

def run_etl_process(skip_if_exists=True):
    """ETL処理を実行"""
    print("\n🚀 ETL処理を開始します...")
    
    # 既存のベクトルストアをチェック
    vector_store_path = Path("vector_store")
    if vector_store_path.exists() and skip_if_exists:
        print(f"✅ 既存のベクトルストア '{vector_store_path}' が見つかりました。")
        print("   ETL処理をスキップします。")
        return True
    
    try:
        # ETL処理の実行
        print("📚 ナレッジファイルを処理中...")
        result = subprocess.run(
            [sys.executable, "run_etl.py"],
            capture_output=True,
            text=True,
            timeout=300  # 5分でタイムアウト
        )
        
        if result.returncode == 0:
            print("✅ ETL処理が正常に完了しました。")
            # 成功時の出力を解析
            lines = result.stdout.split('\n')
            for line in lines:
                if 'ファイル' in line or 'ドキュメント' in line or 'ベクトルストア' in line:
                    print(f"   {line}")
            return True
        else:
            print("❌ ETL処理でエラーが発生しました。")
            print(f"   エラー: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ ETL処理がタイムアウトしました。")
        return False
    except Exception as e:
        print(f"❌ ETL処理実行エラー: {e}")
        return False

def start_server():
    """RAGサーバーを起動"""
    print("\n🚀 RAGサーバーを起動します...")
    
    try:
        # サーバーをバックグラウンドで起動
        process = subprocess.Popen(
            [sys.executable, "server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # サーバーの起動を待つ
        print("⏳ サーバーの起動を待っています...")
        max_retries = 15
        for i in range(max_retries):
            time.sleep(2)
            try:
                response = requests.get("http://localhost:8000/health", timeout=3)
                if response.status_code == 200:
                    print("✅ サーバーが正常に起動しました。")
                    health_data = response.json()
                    print(f"   🔗 サーバーURL: http://localhost:8000")
                    print(f"   📊 ベクトルストア: {health_data.get('vector_store_loaded', 'N/A')}")
                    print(f"   🤖 QAチェーン: {health_data.get('qa_chain_ready', 'N/A')}")
                    return process
            except requests.RequestException:
                print(f"   ⏳ 起動確認中... ({i+1}/{max_retries})")
                continue
        
        # 起動に失敗した場合
        print("❌ サーバーの起動に失敗しました。")
        process.terminate()
        return None
            
    except Exception as e:
        print(f"❌ サーバー起動エラー: {e}")
        return None

def run_comprehensive_demo_tests(server_process):
    """包括的なデモテストを実行"""
    print("\n🧪 包括的なデモテストを開始します...")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. ルートエンドポイントのテスト
        print("\n1️⃣ ルートエンドポイント（/）のテスト")
        print("   " + "-" * 50)
        response = requests.get(f"{base_url}/")
        print(f"   ✅ ステータス: {response.status_code}")
        root_data = response.json()
        print(f"   📝 サービス名: {root_data.get('service')}")
        print(f"   📅 タイムスタンプ: {root_data.get('timestamp')}")
        
        # 2. ヘルスチェックエンドポイントのテスト
        print("\n2️⃣ ヘルスチェック（/health）のテスト")
        print("   " + "-" * 50)
        response = requests.get(f"{base_url}/health")
        print(f"   ✅ ステータス: {response.status_code}")
        health_data = response.json()
        print(f"   🔧 システム状態: {health_data.get('status')}")
        print(f"   📚 ベクトルストア: {health_data.get('vector_store_loaded')}")
        print(f"   🤖 QAチェーン: {health_data.get('qa_chain_ready')}")
        
        # 3. ログインエンドポイントのテスト
        print("\n3️⃣ ログイン（/login）のテスト")
        print("   " + "-" * 50)
        login_data = {"username": "pm_user", "password": "demo_password"}
        response = requests.post(f"{base_url}/login", params=login_data)
        
        if response.status_code == 200:
            print("   ✅ ログイン成功")
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"   🔑 JWTトークン: {access_token[:30]}...")
            
            # 4. PM実務質問のデモテスト
            print("\n4️⃣ PM実務質問デモテスト")
            print("   " + "-" * 50)
            
            demo_questions = [
                {
                    "query": "PMBOKにおけるスコープ管理の主要プロセスは何ですか？",
                    "category": "PMBOK基礎"
                },
                {
                    "query": "アジャイル開発でのリスク管理のベストプラクティスを教えてください",
                    "category": "アジャイル実践"
                },
                {
                    "query": "ITプロジェクトで失敗しやすい要因とその対策は？",
                    "category": "IT実務"
                },
                {
                    "query": "ステークホルダー管理で最も重要なポイントは？",
                    "category": "ステークホルダー管理"
                }
            ]
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            for i, question in enumerate(demo_questions, 1):
                print(f"\n   📝 質問{i} ({question['category']})")
                print(f"   Q: {question['query']}")
                
                query_data = {
                    "query": question["query"],
                    "user_id": "demo_user"
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
                        
                        print(f"   ✅ 回答取得成功")
                        print(f"   📝 回答: {answer[:150]}...")
                        print(f"   📚 参照ソース: {len(sources)}個")
                        if sources:
                            print(f"   📄 主要ソース: {sources[0][:50]}...")
                        
                        # 回答品質評価
                        if len(answer) > 200:
                            print(f"   🏆 回答品質: 詳細 ({len(answer)}文字)")
                        else:
                            print(f"   ⚠️  回答品質: 簡潔 ({len(answer)}文字)")
                        
                    else:
                        print(f"   ❌ 回答取得失敗: {response.status_code}")
                        
                except requests.RequestException as e:
                    print(f"   ❌ 質問処理エラー: {e}")
                
                time.sleep(1)  # APIレート制限対策
            
            # 5. パフォーマンステスト
            print("\n5️⃣ パフォーマンステスト")
            print("   " + "-" * 50)
            
            test_query = {
                "query": "プロジェクトマネジメントとは何ですか？",
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
                    print(f"   ⏱️  テスト{i+1}: {response_time:.2f}秒")
                else:
                    print(f"   ❌ テスト{i+1}: 失敗")
            
            if response_times:
                avg_time = sum(response_times) / len(response_times)
                print(f"   📊 平均レスポンス時間: {avg_time:.2f}秒")
                
                if avg_time < 3.0:
                    print("   🏆 パフォーマンス: 優秀")
                elif avg_time < 5.0:
                    print("   ✅ パフォーマンス: 良好")
                else:
                    print("   ⚠️  パフォーマンス: 要改善")
                
        else:
            print(f"   ❌ ログイン失敗: {response.status_code}")
            print(f"   エラー: {response.text}")
            
    except Exception as e:
        print(f"❌ デモテスト実行エラー: {e}")
    
    finally:
        # サーバーを終了
        print("\n🛑 サーバーを終了します...")
        server_process.terminate()
        server_process.wait()
        print("✅ サーバーが正常に終了しました。")

def interactive_demo():
    """インタラクティブデモモード"""
    print("\n🎮 インタラクティブデモモードを開始します...")
    print("   サーバーを起動して、手動でテストできます。")
    print("   別のターミナルで以下のコマンドを使用してください：")
    print("   - python3 query_cli.py --interactive")
    print("   - curl -X GET http://localhost:8000/docs")
    print("   - curl -X GET http://localhost:8000/health")
    print("\n   Ctrl+C でサーバーを終了します。")
    
    server_process = start_server()
    if server_process:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 インタラクティブデモを終了します...")
            server_process.terminate()
            server_process.wait()
            print("✅ サーバーが正常に終了しました。")

def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(
        description="PM実務コンシェルジュ RAG システム - 包括的ライブデモ"
    )
    parser.add_argument(
        "--interactive", 
        action="store_true",
        help="インタラクティブデモモード（手動テスト用）"
    )
    parser.add_argument(
        "--skip-etl", 
        action="store_true",
        help="ETL処理をスキップ（既存のベクトルストアを使用）"
    )
    
    args = parser.parse_args()
    
    # バナー表示
    print_banner()
    
    # 1. 要件確認
    if not check_requirements():
        print("\n❌ 必要な設定が不足しています。上記の指示に従って設定してください。")
        return
    
    # 2. ETL処理
    if not run_etl_process(skip_if_exists=args.skip_etl):
        print("\n❌ ETL処理が失敗しました。")
        return
    
    # 3. インタラクティブモードまたは自動デモ
    if args.interactive:
        interactive_demo()
    else:
        # 4. サーバー起動
        server_process = start_server()
        if server_process is None:
            print("\n❌ サーバー起動が失敗しました。")
            return
        
        # 5. 包括的デモテスト実行
        run_comprehensive_demo_tests(server_process)
        
        # 6. デモ完了
        print("\n" + "=" * 80)
        print("🎉 包括的ライブデモが完了しました！")
        print("=" * 80)
        print("\n📋 手動テスト用情報:")
        print("   🔗 サーバーURL: http://localhost:8000")
        print("   📖 API仕様: http://localhost:8000/docs")
        print("   🔑 ログイン: username=pm_user, password=demo_password")
        print("   🖥️  コマンドライン: python3 query_cli.py --interactive")
        print("\n💡 サーバーを手動起動:")
        print("   python3 server.py")
        print("\n🎯 次のステップ:")
        print("   - Docker化: docker build -t pm-consultant-rag .")
        print("   - MCP連携: MCP Model Context Protocol統合")
        print("   - 追加機能: ログ機能、認証強化、プロンプト系統")

if __name__ == "__main__":
    main() 