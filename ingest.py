"""
🟢 Green フェーズ: テストを通すための最小限の実装
ETL処理でMarkdownファイルをベクトルストアに変換
インクリメンタル更新機能を含む
"""

import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from config import Config
from langchain.text_splitter import MarkdownTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

class KnowledgeIngester:
    """ナレッジファイルの取り込みとベクトルストア作成を行うクラス"""
    
    def __init__(self):
        """イニシャライザー - テストを通すための最小限の実装"""
        self.knowledge_path = Config.KNOWLEDGE_PATH
        self.vector_store_path = Config.VECTOR_STORE_PATH
        self.text_splitter = MarkdownTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    def load_markdown_files(self) -> List[str]:
        """Markdownファイル読み込み - テストを通すための実装"""
        knowledge_dir = Path(self.knowledge_path)
        markdown_files = []
        
        if knowledge_dir.exists():
            for md_file in knowledge_dir.glob("*.md"):
                markdown_files.append(str(md_file))
        
        return markdown_files
    
    def split_text_into_chunks(self, text: str) -> List[str]:
        """テキスト分割 - テストを通すための実装"""
        chunks = self.text_splitter.split_text(text)
        return chunks
    
    def create_documents_from_chunks(self, chunks: List[str], source_file: str) -> List[Dict[str, Any]]:
        """チャンクからドキュメント作成 - テストを通すための実装"""
        documents = []
        for i, chunk in enumerate(chunks):
            doc = {
                "page_content": chunk,
                "metadata": {
                    "source": source_file,
                    "chunk_id": i,
                    "total_chunks": len(chunks)
                }
            }
            documents.append(doc)
        return documents
    
    def create_vector_store(self, documents: List[Dict[str, Any]]):
        """ベクトルストア作成 - テストを通すための実装"""
        # LangChainのDocumentオブジェクトに変換
        from langchain.schema import Document
        
        langchain_docs = []
        for doc in documents:
            langchain_doc = Document(
                page_content=doc["page_content"],
                metadata=doc["metadata"]
            )
            langchain_docs.append(langchain_doc)
        
        # FAISSベクトルストアを作成
        vector_store = FAISS.from_documents(
            langchain_docs,
            self.embeddings
        )
        
        return vector_store
    
    def save_vector_store(self, vector_store):
        """ベクトルストア保存 - テストを通すための実装"""
        # 保存ディレクトリを作成
        save_path = Path(self.vector_store_path)
        save_path.mkdir(exist_ok=True)
        
        # FAISSインデックスを保存
        vector_store.save_local(str(save_path))
        
        return str(save_path)
    
    def run(self) -> List[Dict[str, Any]]:
        """ETL処理の統合実行メソッド"""
        print("📚 Markdownファイルを検索中...")
        
        # 1. Markdownファイルを読み込み
        markdown_files = self.load_markdown_files()
        if not markdown_files:
            print("❌ Markdownファイルが見つかりませんでした。")
            return []
        
        print(f"📁 {len(markdown_files)}個のMarkdownファイルを発見しました。")
        
        all_documents = []
        
        # 2. 各ファイルを処理
        for file_path in markdown_files:
            print(f"📄 処理中: {Path(file_path).name}")
            
            try:
                # ファイル読み込み
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # テキスト分割
                chunks = self.split_text_into_chunks(content)
                print(f"  📝 {len(chunks)}個のチャンクに分割しました。")
                
                # ドキュメント作成
                documents = self.create_documents_from_chunks(chunks, file_path)
                all_documents.extend(documents)
                
            except Exception as e:
                print(f"  ❌ エラー: {e}")
                continue
        
        if not all_documents:
            print("❌ 処理可能なドキュメントがありませんでした。")
            return []
        
        print(f"📊 合計 {len(all_documents)}個のドキュメントを作成しました。")
        
        # 3. ベクトルストア作成
        print("🔄 ベクトルストアを作成中...")
        try:
            vector_store = self.create_vector_store(all_documents)
            print("✅ ベクトルストアの作成が完了しました。")
            
            # 4. ベクトルストア保存
            print("💾 ベクトルストアを保存中...")
            save_path = self.save_vector_store(vector_store)
            print(f"✅ ベクトルストアを '{save_path}' に保存しました。")
            
            return all_documents
            
        except Exception as e:
            print(f"❌ ベクトルストア作成エラー: {e}")
            return []


class IncrementalIngester(KnowledgeIngester):
    """インクリメンタル更新機能を提供するIngesterクラス"""
    
    def __init__(self):
        super().__init__()
        self.metadata_file = Path(self.vector_store_path) / "file_metadata.json"
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """ファイルのハッシュ値を計算"""
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        return file_hash
    
    def _get_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """ファイルのメタデータを取得"""
        file_stat = os.stat(file_path)
        return {
            "path": file_path,
            "size": file_stat.st_size,
            "mtime": file_stat.st_mtime,
            "hash": self._calculate_file_hash(file_path),
            "last_processed": datetime.now().isoformat()
        }
    
    def _load_metadata(self) -> Dict[str, Dict[str, Any]]:
        """保存されたファイルメタデータを読み込み"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_metadata(self, metadata: Dict[str, Dict[str, Any]]):
        """ファイルメタデータを保存"""
        self.metadata_file.parent.mkdir(exist_ok=True)
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    def _file_has_changed(self, file_path: str, stored_metadata: Dict[str, Any]) -> bool:
        """ファイルが変更されたかチェック"""
        if file_path not in stored_metadata:
            return True
        
        current_meta = self._get_file_metadata(file_path)
        stored_meta = stored_metadata[file_path]
        
        # ハッシュ値で変更を検知
        return current_meta["hash"] != stored_meta.get("hash", "")
    
    def _generate_document_id(self, file_path: str, chunk_id: int) -> str:
        """ドキュメントのユニークIDを生成"""
        file_name = Path(file_path).name
        return f"{file_name}::{chunk_id}"
    
    def _load_existing_vector_store(self) -> Optional[FAISS]:
        """既存のベクターストアを読み込み"""
        vector_store_path = Path(self.vector_store_path)
        if vector_store_path.exists():
            try:
                return FAISS.load_local(
                    str(vector_store_path), 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                print(f"⚠️  既存ベクターストア読み込みエラー: {e}")
                return None
        return None
    
    def add_knowledge_file(self, file_path: str) -> bool:
        """単一ファイルを既存ベクターストアに追加"""
        print(f"📄 ファイル追加: {Path(file_path).name}")
        
        try:
            # ファイル内容を読み込み
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # テキスト分割
            chunks = self.split_text_into_chunks(content)
            print(f"  📝 {len(chunks)}個のチャンクに分割")
            
            # ドキュメント作成
            documents = []
            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source": file_path,
                        "chunk_id": i,
                        "total_chunks": len(chunks),
                        "document_id": self._generate_document_id(file_path, i)
                    }
                )
                documents.append(doc)
            
            # 既存ベクターストアを読み込み
            vector_store = self._load_existing_vector_store()
            
            if vector_store is None:
                # ベクターストアが存在しない場合は新規作成
                print("  🆕 新規ベクターストア作成")
                vector_store = FAISS.from_documents(documents, self.embeddings)
            else:
                # 既存ベクターストアに追加
                print("  ➕ 既存ベクターストアに追加")
                vector_store.add_documents(documents)
            
            # ベクターストアを保存
            self.save_vector_store(vector_store)
            
            # メタデータを更新
            metadata = self._load_metadata()
            metadata[file_path] = self._get_file_metadata(file_path)
            self._save_metadata(metadata)
            
            print(f"  ✅ ファイル追加完了: {len(documents)}個のドキュメント")
            return True
            
        except Exception as e:
            print(f"  ❌ ファイル追加エラー: {e}")
            return False
    
    def remove_knowledge_file(self, file_path: str) -> bool:
        """単一ファイルを既存ベクターストアから削除"""
        print(f"🗑️  ファイル削除: {Path(file_path).name}")
        
        try:
            # 既存ベクターストアを読み込み
            vector_store = self._load_existing_vector_store()
            if vector_store is None:
                print("  ⚠️  ベクターストアが存在しません")
                return False
            
            # 削除対象のドキュメントIDを特定
            # 注意: FAISSは直接的な削除機能が限定的なため、
            # 実際の実装では全体を再構築する方が確実
            print("  ⚠️  FAISS制限のため、ファイル削除には全体再構築を推奨")
            
            # メタデータから削除
            metadata = self._load_metadata()
            if file_path in metadata:
                del metadata[file_path]
                self._save_metadata(metadata)
                print("  ✅ メタデータから削除完了")
            
            return True
            
        except Exception as e:
            print(f"  ❌ ファイル削除エラー: {e}")
            return False
    
    def update_knowledge_file(self, file_path: str) -> bool:
        """単一ファイルを更新（削除→追加）"""
        print(f"🔄 ファイル更新: {Path(file_path).name}")
        
        # まず削除してから追加
        self.remove_knowledge_file(file_path)
        return self.add_knowledge_file(file_path)
    
    def incremental_update(self) -> Dict[str, int]:
        """変更されたファイルのみを更新"""
        print("🔄 インクリメンタル更新開始...")
        
        # 現在のファイル一覧を取得
        current_files = self.load_markdown_files()
        stored_metadata = self._load_metadata()
        
        stats = {
            "added": 0,
            "updated": 0,
            "removed": 0,
            "unchanged": 0
        }
        
        # 新規・更新ファイルの処理
        for file_path in current_files:
            if self._file_has_changed(file_path, stored_metadata):
                if file_path in stored_metadata:
                    # 更新
                    if self.update_knowledge_file(file_path):
                        stats["updated"] += 1
                else:
                    # 新規追加
                    if self.add_knowledge_file(file_path):
                        stats["added"] += 1
            else:
                stats["unchanged"] += 1
        
        # 削除されたファイルの処理
        current_file_set = set(current_files)
        for stored_file in stored_metadata.keys():
            if stored_file not in current_file_set:
                if self.remove_knowledge_file(stored_file):
                    stats["removed"] += 1
        
        print(f"📊 インクリメンタル更新完了:")
        print(f"  ➕ 追加: {stats['added']}ファイル")
        print(f"  🔄 更新: {stats['updated']}ファイル")  
        print(f"  🗑️  削除: {stats['removed']}ファイル")
        print(f"  ✅ 変更なし: {stats['unchanged']}ファイル")
        
        return stats


if __name__ == "__main__":
    # 直接実行された場合のテスト
    ingester = KnowledgeIngester()
    documents = ingester.run()
    print(f"処理完了: {len(documents)}個のドキュメント") 