"""
🟢 Green フェーズ: テストを通すための最小限の実装
ETL処理でMarkdownファイルをベクトルストアに変換
"""

from pathlib import Path
from typing import List, Dict, Any
from config import Config
from langchain.text_splitter import MarkdownTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

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


if __name__ == "__main__":
    # 直接実行された場合のテスト
    ingester = KnowledgeIngester()
    documents = ingester.run()
    print(f"処理完了: {len(documents)}個のドキュメント") 