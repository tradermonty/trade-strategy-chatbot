#!/usr/bin/env python3
"""
ETL処理実行スクリプト
実際のナレッジファイルからベクトルストアを作成
インクリメンタル更新機能を含む
"""

import os
import sys
import argparse
from pathlib import Path
from ingest import KnowledgeIngester, IncrementalIngester

def run_full_etl():
    """フル再構築ETL処理"""
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

def run_incremental_update():
    """インクリメンタル更新処理"""
    print("🔄 インクリメンタル更新を開始...")
    
    try:
        # IncrementalIngesterのインスタンス作成
        ingester = IncrementalIngester()
        
        # インクリメンタル更新実行
        stats = ingester.incremental_update()
        
        total_changes = stats["added"] + stats["updated"] + stats["removed"]
        if total_changes > 0:
            print(f"\n✅ インクリメンタル更新が完了しました！")
            print(f"📊 変更統計:")
            print(f"  ➕ 追加: {stats['added']}ファイル")
            print(f"  🔄 更新: {stats['updated']}ファイル")
            print(f"  🗑️  削除: {stats['removed']}ファイル")
            print(f"  ✅ 変更なし: {stats['unchanged']}ファイル")
        else:
            print("📊 変更されたファイルはありませんでした。")
            
    except Exception as e:
        print(f"❌ インクリメンタル更新中にエラーが発生しました: {e}")
        sys.exit(1)
    
    print("\n🎉 インクリメンタル更新が正常に完了しました！")

def add_single_file(file_path: str):
    """単一ファイルを追加"""
    print(f"📄 ファイル追加処理: {file_path}")
    
    if not Path(file_path).exists():
        print(f"❌ ファイルが存在しません: {file_path}")
        sys.exit(1)
    
    try:
        ingester = IncrementalIngester()
        if ingester.add_knowledge_file(file_path):
            print(f"✅ ファイル追加完了: {Path(file_path).name}")
        else:
            print(f"❌ ファイル追加失敗: {Path(file_path).name}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ ファイル追加中にエラーが発生しました: {e}")
        sys.exit(1)

def main():
    """メイン関数 - コマンドライン引数を処理"""
    parser = argparse.ArgumentParser(
        description="Knowledge ETL処理ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python3 run_etl.py                    # フル再構築
  python3 run_etl.py --incremental      # インクリメンタル更新
  python3 run_etl.py --add recipe.md    # 単一ファイル追加
        """
    )
    
    parser.add_argument(
        "--incremental", "-i",
        action="store_true",
        help="インクリメンタル更新を実行（変更されたファイルのみ処理）"
    )
    
    parser.add_argument(
        "--add", "-a",
        metavar="FILE",
        help="指定したファイルを既存ベクターストアに追加"
    )
    
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="確認なしでフル再構築を実行"
    )
    
    args = parser.parse_args()
    
    # 引数に応じて処理を分岐
    if args.add:
        add_single_file(args.add)
    elif args.incremental:
        run_incremental_update()
    else:
        # フル再構築
        if args.force:
            # 強制実行の場合は確認をスキップ
            vector_store_path = Path("vector_store")
            if vector_store_path.exists():
                import shutil
                shutil.rmtree(vector_store_path)
                print("🗑️  既存のベクトルストアを削除しました。")
        run_full_etl()

if __name__ == "__main__":
    main() 