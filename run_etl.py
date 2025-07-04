#!/usr/bin/env python3
"""
ETL処理実行スクリプト
実際のナレッジファイルからベクトルストアを作成
"""

import os
import sys
from pathlib import Path
from ingest import KnowledgeIngester

def main():
    """ETL処理を実行"""
    print("🚀 Knowledge ETL processing started...")
    
    # 出力ディレクトリの確認・作成
    vector_store_path = Path("vector_store")
    if vector_store_path.exists():
        print(f"⚠️  既存のベクトルストア '{vector_store_path}' が見つかりました。")
        response = input("既存のベクトルストアを削除して新規作成しますか？ (y/N): ")
        if response.lower() in ['y', 'yes']:
            import shutil
            shutil.rmtree(vector_store_path)
            print("🗑️  既存のベクトルストアを削除しました。")
        else:
            print("❌ ETL処理をキャンセルしました。")
            return
    
    try:
        # KnowledgeIngesterのインスタンス作成
        ingester = KnowledgeIngester()
        
        # ETL処理実行
        print("📚 Markdownファイルを読み込み中...")
        documents = ingester.run()
        
        if documents:
            print(f"✅ ETL処理が完了しました！")
            print(f"📊 処理されたドキュメント数: {len(documents)}")
            print(f"💾 ベクトルストア保存先: {vector_store_path}")
            
            # ナレッジファイルの一覧表示
            knowledge_files = ingester.load_markdown_files()
            print(f"\n📋 処理されたナレッジファイル:")
            for i, file_path in enumerate(knowledge_files, 1):
                file_name = Path(file_path).name
                print(f"  {i}. {file_name}")
                
        else:
            print("❌ ETL処理でエラーが発生しました。")
            
    except Exception as e:
        print(f"❌ ETL処理中にエラーが発生しました: {e}")
        sys.exit(1)
    
    print("\n🎉 ETL処理が正常に完了しました！")
    print("次のステップ: python3 server.py でRAGサーバーを起動してください。")

if __name__ == "__main__":
    main() 