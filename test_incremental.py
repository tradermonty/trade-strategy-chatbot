#!/usr/bin/env python3
"""
インクリメンタル更新機能のテストケース
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# テスト用の一時的なAPIキーを設定
os.environ["OPENAI_API_KEY"] = "test-api-key"

from ingest import IncrementalIngester

def test_file_change_detection():
    """ファイル変更検知のテスト"""
    print("🧪 ファイル変更検知テスト開始...")
    
    # テスト用の一時ディレクトリを作成
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_file = temp_path / "test.md"
        
        # OpenAI APIをモック
        with patch('langchain_openai.OpenAIEmbeddings') as mock_embeddings:
            mock_embeddings.return_value = MagicMock()
            
            # IncrementalIngesterのテスト用インスタンス
            ingester = IncrementalIngester()
            ingester.knowledge_path = str(temp_path)
            ingester.vector_store_path = str(temp_path / "vector_store")
            
            # 初期ファイル作成
            test_file.write_text("# テストファイル\n初期内容")
            
            # 初回メタデータ取得
            metadata1 = ingester._get_file_metadata(str(test_file))
            print(f"  📄 初期メタデータ: ハッシュ={metadata1['hash'][:8]}...")
            
            # ファイル内容を変更
            test_file.write_text("# テストファイル\n変更後の内容")
            
            # 変更後メタデータ取得
            metadata2 = ingester._get_file_metadata(str(test_file))
            print(f"  📄 変更後メタデータ: ハッシュ={metadata2['hash'][:8]}...")
            
            # 変更検知テスト
            stored_metadata = {str(test_file): metadata1}
            has_changed = ingester._file_has_changed(str(test_file), stored_metadata)
            
            assert has_changed, "ファイル変更が検知されませんでした"
            print("  ✅ ファイル変更検知成功")
            
            # 変更なしのテスト
            stored_metadata = {str(test_file): metadata2}
            has_changed = ingester._file_has_changed(str(test_file), stored_metadata)
            
            assert not has_changed, "変更していないファイルが変更ありと判定されました"
            print("  ✅ 変更なし検知成功")

def test_metadata_persistence():
    """メタデータ永続化のテスト"""
    print("🧪 メタデータ永続化テスト開始...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # OpenAI APIをモック
        with patch('langchain_openai.OpenAIEmbeddings') as mock_embeddings:
            mock_embeddings.return_value = MagicMock()
            
            ingester = IncrementalIngester()
            ingester.knowledge_path = str(temp_path)
            ingester.vector_store_path = str(temp_path / "vector_store")
            ingester.metadata_file = temp_path / "vector_store" / "file_metadata.json"
            
            # テストメタデータ
            test_metadata = {
                "test1.md": {
                    "path": "test1.md",
                    "hash": "abc123",
                    "mtime": 1234567890.0
                },
                "test2.md": {
                    "path": "test2.md", 
                    "hash": "def456",
                    "mtime": 1234567891.0
                }
            }
            
            # メタデータ保存
            ingester._save_metadata(test_metadata)
            print("  💾 メタデータ保存完了")
            
            # メタデータ読み込み
            loaded_metadata = ingester._load_metadata()
            
            assert loaded_metadata == test_metadata, "保存・読み込みしたメタデータが一致しません"
            print("  ✅ メタデータ永続化成功")

def test_document_id_generation():
    """ドキュメントID生成のテスト"""
    print("🧪 ドキュメントID生成テスト開始...")
    
    with patch('langchain_openai.OpenAIEmbeddings') as mock_embeddings:
        mock_embeddings.return_value = MagicMock()
        
        ingester = IncrementalIngester()
        
        # ドキュメントID生成テスト
        file_path = "/path/to/recipe.md"
        chunk_id = 5
        
        doc_id = ingester._generate_document_id(file_path, chunk_id)
        expected_id = "recipe.md::5"
        
        assert doc_id == expected_id, f"期待されるID '{expected_id}' と異なります: '{doc_id}'"
        print(f"  ✅ ドキュメントID生成成功: {doc_id}")

def test_incremental_update_logic():
    """インクリメンタル更新ロジックのテスト"""
    print("🧪 インクリメンタル更新ロジックテスト開始...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # OpenAI APIとFAISSをモック
        with patch('langchain_openai.OpenAIEmbeddings') as mock_embeddings, \
             patch('langchain_community.vectorstores.FAISS') as mock_faiss:
            
            mock_embeddings.return_value = MagicMock()
            mock_faiss.load_local.return_value = MagicMock()
            mock_faiss.from_documents.return_value = MagicMock()
            
            ingester = IncrementalIngester()
            ingester.knowledge_path = str(temp_path)
            ingester.vector_store_path = str(temp_path / "vector_store")
            ingester.metadata_file = temp_path / "vector_store" / "file_metadata.json"
            
            # テストファイル作成
            file1 = temp_path / "file1.md"
            file2 = temp_path / "file2.md"
            file3 = temp_path / "file3.md"
            
            file1.write_text("# ファイル1\n内容1")
            file2.write_text("# ファイル2\n内容2") 
            file3.write_text("# ファイル3\n内容3")
            
            # 初期メタデータ（file1, file2のみ存在）
            initial_metadata = {
                str(file1): ingester._get_file_metadata(str(file1)),
                str(file2): {
                    "path": str(file2),
                    "hash": "old_hash",  # 異なるハッシュで更新を模擬
                    "mtime": 1234567890.0
                }
            }
            ingester._save_metadata(initial_metadata)
            
            # add_knowledge_fileとupdate_knowledge_fileメソッドをモック
            with patch.object(ingester, 'add_knowledge_file', return_value=True) as mock_add, \
                 patch.object(ingester, 'update_knowledge_file', return_value=True) as mock_update, \
                 patch.object(ingester, 'remove_knowledge_file', return_value=True) as mock_remove:
                
                # インクリメンタル更新実行
                stats = ingester.incremental_update()
                
                # 結果検証
                print(f"  📊 統計結果: {stats}")
                
                # file1: 変更なし, file2: 更新, file3: 新規追加を期待
                assert stats["unchanged"] >= 1, "変更なしファイルが検出されませんでした"
                assert stats["updated"] >= 1, "更新ファイルが検出されませんでした"  
                assert stats["added"] >= 1, "新規ファイルが検出されませんでした"
                
                print("  ✅ インクリメンタル更新ロジック成功")

def run_all_tests():
    """全テストを実行"""
    print("🚀 インクリメンタル更新機能テスト開始\n")
    
    try:
        test_file_change_detection()
        print()
        
        test_metadata_persistence()
        print()
        
        test_document_id_generation()
        print()
        
        test_incremental_update_logic()
        print()
        
        print("🎉 全テスト完了！すべて成功しました。")
        return True
        
    except Exception as e:
        print(f"❌ テスト失敗: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)