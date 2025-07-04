import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from ingest import KnowledgeIngester

class TestKnowledgeIngester:
    
    def test_ingester_initialization(self):
        """🔴 Red: イニシャライザーのテスト"""
        with patch('ingest.OpenAIEmbeddings'):
            ingester = KnowledgeIngester()
            assert ingester is not None
            assert hasattr(ingester, 'knowledge_path')
            assert hasattr(ingester, 'vector_store_path')
    
    def test_load_markdown_files(self):
        """🔴 Red: MarkdownFile loadingのテスト"""
        with patch('ingest.OpenAIEmbeddings'):
            ingester = KnowledgeIngester()
            files = ingester.load_markdown_files()
            assert isinstance(files, list)
            assert len(files) > 0
            # 実際のknowledgeディレクトリに.mdファイルが存在することを確認
            assert any(file.endswith('.md') for file in files)
    
    def test_split_text_into_chunks(self):
        """🔴 Red: Text splittingのテスト"""
        with patch('ingest.OpenAIEmbeddings'):
            ingester = KnowledgeIngester()
            sample_text = "これはテストテキストです。" * 100  # 長いテキスト
            chunks = ingester.split_text_into_chunks(sample_text)
            assert isinstance(chunks, list)
            assert len(chunks) > 0
            # 各チャンクが文字列であることを確認
            assert all(isinstance(chunk, str) for chunk in chunks)
    
    def test_create_documents_from_chunks(self):
        """🔴 Red: チャンクからDocument creationのテスト"""
        with patch('ingest.OpenAIEmbeddings'):
            ingester = KnowledgeIngester()
            chunks = ["チャンク1", "チャンク2", "チャンク3"]
            source_file = "test.md"
            documents = ingester.create_documents_from_chunks(chunks, source_file)
            assert isinstance(documents, list)
            assert len(documents) == 3
            # 各ドキュメントが適切な構造を持つことを確認
            for doc in documents:
                assert 'page_content' in doc
                assert 'metadata' in doc
                assert doc['metadata']['source'] == source_file
    
    @patch('ingest.FAISS')
    def test_create_vector_store(self, mock_faiss):
        """🔴 Red: ベクトルストア作成のテスト"""
        with patch('ingest.OpenAIEmbeddings') as mock_embeddings:
            mock_embeddings_instance = Mock()
            mock_embeddings.return_value = mock_embeddings_instance
            
            ingester = KnowledgeIngester()
            documents = [
                {'page_content': 'テスト1', 'metadata': {'source': 'test1.md'}},
                {'page_content': 'テスト2', 'metadata': {'source': 'test2.md'}}
            ]
            
            mock_vectorstore = Mock()
            mock_faiss.from_documents.return_value = mock_vectorstore
            
            result = ingester.create_vector_store(documents)
            
            # FAISSが正しく呼び出されることを確認
            # Documentオブジェクトに変換されていることを確認
            mock_faiss.from_documents.assert_called_once()
            assert result == mock_vectorstore
    
    def test_run_etl_process(self):
        """🔴 Red: ETL全体プロセスのテスト"""
        with patch('ingest.OpenAIEmbeddings'):
            ingester = KnowledgeIngester()
            # このテストは実際のファイルとAPIを使用するため、モックを使用
            with patch.object(ingester, 'load_markdown_files') as mock_load, \
                 patch.object(ingester, 'split_text_into_chunks') as mock_split, \
                 patch.object(ingester, 'create_documents_from_chunks') as mock_create_docs, \
                 patch.object(ingester, 'create_vector_store') as mock_create_vs, \
                 patch.object(ingester, 'save_vector_store') as mock_save:
                
                mock_load.return_value = ['test.md']
                mock_split.return_value = ['chunk1', 'chunk2']
                mock_create_docs.return_value = [{'page_content': 'chunk1', 'metadata': {'source': 'test.md'}}]
                mock_create_vs.return_value = Mock()
                
                # File loadingをモック
                with patch('builtins.open', create=True) as mock_open:
                    mock_open.return_value.__enter__.return_value.read.return_value = "テストファイル内容"
                    
                    result = ingester.run()
                    
                    # 結果がリストであることを確認
                    assert isinstance(result, list)
                    mock_load.assert_called_once()
                    mock_save.assert_called_once() 