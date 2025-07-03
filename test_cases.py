#!/usr/bin/env python3
"""
🎯 PM実務コンシェルジュ RAG システム - 追加テストケース
プレゼンテーション・デモ用の包括的なテストケース集
"""

import requests
import json
import time
from datetime import datetime

class PMConsultantTestCases:
    """PM実務コンシェルジュの追加テストケース"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.access_token = None
    
    def login(self):
        """ログインしてアクセストークンを取得"""
        login_data = {"username": "pm_user", "password": "demo_password"}
        response = requests.post(f"{self.base_url}/login", params=login_data)
        
        if response.status_code == 200:
            self.access_token = response.json()["access_token"]
            return True
        return False
    
    def ask_question(self, query, category="一般"):
        """質問を送信して回答を取得"""
        if not self.access_token:
            return None
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        query_data = {
            "query": query,
            "user_id": f"test_{category.lower()}"
        }
        
        start_time = time.time()
        response = requests.post(
            f"{self.base_url}/query",
            json=query_data,
            headers=headers,
            timeout=30
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            result["response_time"] = end_time - start_time
            result["category"] = category
            return result
        return None

# 📚 プレゼンテーション用テストケース集
PRESENTATION_TEST_CASES = [
    # 🏆 PMベーシック質問
    {
        "category": "PMベーシック",
        "questions": [
            "プロジェクトマネージャーの主要な責任は何ですか？",
            "プロジェクトの三大制約（トリプル制約）とは何ですか？",
            "プロジェクトライフサイクルの主要フェーズを教えてください",
            "品質管理と品質保証の違いは何ですか？"
        ]
    },
    
    # 🚀 アジャイル・スクラム実践
    {
        "category": "アジャイル実践",
        "questions": [
            "スクラムマスターとプロダクトオーナーの役割の違いは？",
            "スプリントプランニングで最も重要なポイントは？",
            "アジャイル開発でのベロシティとは何ですか？",
            "デイリースタンドアップミーティングの効果的な進め方は？"
        ]
    },
    
    # 💼 IT業界特化
    {
        "category": "IT業界特化",
        "questions": [
            "DevOpsプロジェクトでのプロジェクトマネジメントのポイントは？",
            "クラウド移行プロジェクトでの主要なリスクと対策は？",
            "SaaS開発プロジェクトでの特有の課題は何ですか？",
            "APIプロジェクトでのステークホルダー管理のコツは？"
        ]
    },
    
    # 🎯 リスク・課題管理
    {
        "category": "リスク管理",
        "questions": [
            "リスクレジスタの作成と管理方法を教えてください",
            "プロジェクト遅延が発生した時の対処法は？",
            "ステークホルダー間のコンフリクト解決方法は？",
            "予算超過リスクの早期発見と対策は？"
        ]
    },
    
    # 📊 測定・改善
    {
        "category": "測定改善",
        "questions": [
            "プロジェクトの健全性を測る主要KPIは？",
            "チームパフォーマンスの改善方法は？",
            "プロジェクト振り返りの効果的な進め方は？",
            "継続的改善プロセスの導入方法は？"
        ]
    }
]

# 🎪 ライブデモ用の質問セット
LIVE_DEMO_QUESTIONS = [
    {
        "query": "プロジェクトが炎上しそうな時の緊急対応策は？",
        "category": "緊急対応",
        "expected_keywords": ["ステークホルダー", "リスク", "コミュニケーション", "リソース"]
    },
    {
        "query": "リモートワーク環境でのプロジェクト管理のベストプラクティスは？", 
        "category": "現代課題",
        "expected_keywords": ["コミュニケーション", "ツール", "進捗管理", "チーム"]
    },
    {
        "query": "AIプロジェクトの特有な管理ポイントは？",
        "category": "最新技術",
        "expected_keywords": ["データ", "実験", "反復", "不確実性"]
    },
    {
        "query": "ESG経営とプロジェクトマネジメントの関係は？",
        "category": "戦略的視点", 
        "expected_keywords": ["持続可能性", "環境", "社会", "ガバナンス"]
    }
]

def run_presentation_demo():
    """プレゼンテーション用デモ実行"""
    print("=" * 80)
    print("🎯 PM実務コンシェルジュ RAG - プレゼンテーション用デモ")
    print("=" * 80)
    
    # テスト対象システムの準備
    test_client = PMConsultantTestCases()
    
    # ログイン
    print("🔐 システムにログイン中...")
    if not test_client.login():
        print("❌ ログインに失敗しました")
        return
    print("✅ ログイン成功")
    
    # ライブデモ質問を実行
    print("\n🎪 ライブデモ質問セット")
    print("-" * 50)
    
    for i, demo_q in enumerate(LIVE_DEMO_QUESTIONS, 1):
        print(f"\n📝 質問{i} ({demo_q['category']})")
        print(f"Q: {demo_q['query']}")
        
        result = test_client.ask_question(demo_q['query'], demo_q['category'])
        
        if result:
            answer = result['answer']
            response_time = result['response_time']
            sources = result.get('sources', [])
            
            print(f"✅ 回答取得: {response_time:.2f}秒")
            print(f"📝 回答: {answer[:200]}...")
            print(f"📚 ソース: {len(sources)}個")
            
            # キーワード評価
            found_keywords = []
            for keyword in demo_q['expected_keywords']:
                if keyword in answer:
                    found_keywords.append(keyword)
            
            print(f"🎯 期待キーワード: {found_keywords} / {demo_q['expected_keywords']}")
            
            if len(found_keywords) >= len(demo_q['expected_keywords']) * 0.5:
                print("🏆 回答品質: 優秀")
            else:
                print("⚠️  回答品質: 改善可能")
        else:
            print("❌ 回答取得失敗")
        
        time.sleep(1)
    
    print("\n" + "=" * 80)
    print("🎉 プレゼンテーション用デモ完了！")
    print("=" * 80)

def run_category_benchmark():
    """カテゴリ別ベンチマークテスト"""
    print("=" * 80)
    print("📊 PM実務コンシェルジュ RAG - カテゴリ別ベンチマーク")
    print("=" * 80)
    
    test_client = PMConsultantTestCases()
    
    if not test_client.login():
        print("❌ ログインに失敗しました")
        return
    
    all_results = []
    
    for category_data in PRESENTATION_TEST_CASES:
        category = category_data["category"]
        questions = category_data["questions"]
        
        print(f"\n📂 カテゴリ: {category}")
        print("-" * 40)
        
        category_results = []
        
        for i, question in enumerate(questions, 1):
            print(f"\n   質問{i}: {question[:50]}...")
            
            result = test_client.ask_question(question, category)
            
            if result:
                category_results.append(result)
                response_time = result['response_time']
                answer_length = len(result['answer'])
                sources_count = len(result.get('sources', []))
                
                print(f"   ✅ {response_time:.1f}秒 | {answer_length}文字 | {sources_count}ソース")
            else:
                print("   ❌ 失敗")
            
            time.sleep(0.5)
        
        # カテゴリ統計
        if category_results:
            avg_time = sum(r['response_time'] for r in category_results) / len(category_results)
            avg_length = sum(len(r['answer']) for r in category_results) / len(category_results)
            total_sources = sum(len(r.get('sources', [])) for r in category_results)
            
            print(f"\n   📊 統計: {avg_time:.1f}秒平均 | {avg_length:.0f}文字平均 | {total_sources}総ソース")
            
            all_results.extend(category_results)
    
    # 全体統計
    if all_results:
        total_questions = len(all_results)
        overall_avg_time = sum(r['response_time'] for r in all_results) / total_questions
        overall_avg_length = sum(len(r['answer']) for r in all_results) / total_questions
        overall_sources = sum(len(r.get('sources', [])) for r in all_results)
        
        print(f"\n" + "=" * 80)
        print("📈 全体統計サマリー")
        print("=" * 80)
        print(f"🔢 総質問数: {total_questions}")
        print(f"⏱️  平均レスポンス: {overall_avg_time:.2f}秒")
        print(f"📝 平均回答長: {overall_avg_length:.0f}文字")
        print(f"📚 総参照ソース: {overall_sources}個")
        print(f"📊 ソース活用率: {(overall_sources/total_questions):.1f}個/質問")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="PM実務コンシェルジュ追加テストケース")
    parser.add_argument("--demo", action="store_true", help="プレゼンテーション用デモ実行")
    parser.add_argument("--benchmark", action="store_true", help="カテゴリ別ベンチマーク実行")
    
    args = parser.parse_args()
    
    if args.demo:
        run_presentation_demo()
    elif args.benchmark:
        run_category_benchmark()
    else:
        print("使用方法:")
        print("  python3 test_cases.py --demo       : プレゼンテーション用デモ")
        print("  python3 test_cases.py --benchmark  : カテゴリ別ベンチマーク")
        print("\n💡 使用前にサーバーを起動してください: python3 server.py") 