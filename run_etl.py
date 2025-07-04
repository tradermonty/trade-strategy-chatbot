#!/usr/bin/env python3
"""
ETL処理実行スクリプト
実際のナレッジファイルからベクトルストアを作成
Including incremental update functionality
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
    """インクリメンタルUpdate処理（ベクトルストアが存在しない場合は自動的にフル構築）"""
    print("🔄 インクリメンタルUpdateを開始...")
    
    # ベクトルストアの存在確認
    vector_store_path = Path("vector_store")
    if not vector_store_path.exists():
        print("⚠️  ベクトルストアが存在しません。")
        print("🚀 フル構築を実行します...")
        
        # フル構築を実行
        try:
            ingester = KnowledgeIngester()
            documents = ingester.run()
            
            if documents:
                print(f"✅ フル構築が完了しました！")
                print(f"📊 処理されたドキュメント数: {len(documents)}")
                return
            else:
                print("❌ フル構築でエラーが発生しました。")
                sys.exit(1)
                
        except Exception as e:
            print(f"❌ フル構築中にエラーが発生しました: {e}")
            sys.exit(1)
    
    try:
        # IncrementalIngesterのインスタンス作成
        ingester = IncrementalIngester()
        
        # インクリメンタルUpdate実行
        stats = ingester.incremental_update()
        
        total_changes = stats["added"] + stats["updated"] + stats["removed"]
        if total_changes > 0:
            print(f"\n✅ インクリメンタルUpdateが完了しました！")
            print(f"📊 変更統計:")
            print(f"  ➕ Added: {stats['added']} files")
            print(f"  🔄 Update: {stats['updated']}ファイル")
            print(f"  🗑️  Deleted: {stats['removed']} files")
            print(f"  ✅ Unchanged: {stats['unchanged']} files")
        else:
            print("📊 変更されたファイルはありませんでした。")
            
    except Exception as e:
        print(f"❌ インクリメンタルUpdate中にエラーが発生しました: {e}")
        sys.exit(1)
    
    print("\n🎉 インクリメンタルUpdateが正常に完了しました！")

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

def show_status():
    """ベクトルストアとナレッジファイルの状態を表示"""
    print("📊 システム状態確認...")
    
    try:
        # ベクトルストアの状態確認
        vector_store_path = Path("vector_store")
        if vector_store_path.exists():
            print(f"✅ ベクトルストアが存在: {vector_store_path}")
            
            # ベクトルストアファイルのサイズ情報
            index_file = vector_store_path / "index.faiss"
            pkl_file = vector_store_path / "index.pkl"
            
            if index_file.exists():
                size_mb = index_file.stat().st_size / (1024 * 1024)
                print(f"  📊 FAISSインデックス: {size_mb:.2f} MB")
            
            if pkl_file.exists():
                size_kb = pkl_file.stat().st_size / 1024
                print(f"  📊 メタデータ: {size_kb:.2f} KB")
        else:
            print("❌ ベクトルストアが存在しません")
        
        # ナレッジファイルの状態確認
        ingester = KnowledgeIngester()
        knowledge_files = ingester.load_markdown_files()
        print(f"\n📚 ナレッジファイル: {len(knowledge_files)}個")
        
        for i, file_path in enumerate(knowledge_files, 1):
            file_name = Path(file_path).name
            size_kb = Path(file_path).stat().st_size / 1024
            print(f"  {i}. {file_name} ({size_kb:.1f} KB)")
        
        # インクリメンタルUpdateの状態確認
        try:
            inc_ingester = IncrementalIngester()
            metadata = inc_ingester._load_metadata()
            
            if metadata:
                print(f"\n🔄 処理済みファイル: {len(metadata)}個")
                print("  最後の処理時刻:")
                for file_path, meta in metadata.items():
                    file_name = Path(file_path).name
                    last_processed = meta.get("last_processed", "不明")
                    print(f"    {file_name}: {last_processed}")
            else:
                print("\n⚠️  インクリメンタルUpdateのメタデータがありません")
                print("   初回処理時にメタデータが作成されます")
                
        except Exception as e:
            print(f"\n⚠️  メタデータ確認中にエラー: {e}")
        
    except Exception as e:
        print(f"❌ 状態確認中にエラーが発生しました: {e}")
        sys.exit(1)

def main():
    """メイン関数 - コマンドライン引数を処理"""
    parser = argparse.ArgumentParser(
        description="Knowledge ETL処理ツール（デフォルト: インクリメンタルUpdate）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python3 run_etl.py                    # インクリメンタルUpdate（デフォルト）
  python3 run_etl.py --full             # フル再構築
  python3 run_etl.py --add recipe.md    # 単一ファイル追加
  python3 run_etl.py --status           # ベクトルストア状態確認
        """
    )
    
    parser.add_argument(
        "--full", "-f",
        action="store_true",
        help="フル再構築を実行（既存のベクトルストアを削除して新規作成）"
    )
    
    parser.add_argument(
        "--add", "-a",
        metavar="FILE",
        help="指定したファイルをAdd to existing vector store"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="確認なしで処理を実行"
    )
    
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="ベクトルストアとナレッジファイルの状態を確認"
    )
    
    args = parser.parse_args()
    
    # 引数に応じて処理を分岐
    if args.status:
        show_status()
    elif args.add:
        add_single_file(args.add)
    elif args.full:
        # フル再構築
        if args.force:
            # 強制実行の場合は確認をスキップ
            vector_store_path = Path("vector_store")
            if vector_store_path.exists():
                import shutil
                shutil.rmtree(vector_store_path)
                print("🗑️  既存のベクトルストアを削除しました。")
        run_full_etl()
    else:
        # デフォルト: インクリメンタルUpdate
        run_incremental_update()

if __name__ == "__main__":
    main() 