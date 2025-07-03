import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import json
from server import app, RAGServer

class TestRAGServer:
    
    def test_rag_server_initialization(self):
        """🔴 Red: RAGサーバー初期化のテスト"""
        with patch('server.OpenAIEmbeddings'):
            rag_server = RAGServer()
            assert rag_server is not None
            assert hasattr(rag_server, 'vector_store')
            assert hasattr(rag_server, 'llm')
            assert hasattr(rag_server, 'retriever')
            assert hasattr(rag_server, 'qa_chain')
    
    def test_load_vector_store(self):
        """🔴 Red: ベクトルストア読み込みのテスト"""
        with patch('server.FAISS') as mock_faiss, \
             patch('server.OpenAIEmbeddings') as mock_embeddings, \
             patch('server.ChatOpenAI'), \
             patch('server.Path') as mock_path:
            
            # Pathが存在することをモック
            mock_path_instance = Mock()
            mock_path.return_value = mock_path_instance
            mock_path_instance.exists.return_value = True
            
            mock_vector_store = Mock()
            mock_faiss.load_local.return_value = mock_vector_store
            mock_embeddings_instance = Mock()
            mock_embeddings.return_value = mock_embeddings_instance
            
            rag_server = RAGServer()
            result = rag_server.load_vector_store()
            
            # FAISSのload_localが正しく呼び出されることを確認
            mock_faiss.load_local.assert_called_once()
            assert result == mock_vector_store
    
    def test_setup_retrieval_qa(self):
        """🔴 Red: RetrievalQAセットアップのテスト"""
        with patch('server.FAISS') as mock_faiss, \
             patch('server.OpenAIEmbeddings') as mock_embeddings, \
             patch('server.ChatOpenAI') as mock_llm, \
             patch('server.RetrievalQA') as mock_qa, \
             patch('server.Path') as mock_path:
            
            # Pathが存在することをモック
            mock_path_instance = Mock()
            mock_path.return_value = mock_path_instance
            mock_path_instance.exists.return_value = True
            
            # ベクトルストアをモック
            mock_vector_store = Mock()
            mock_faiss.load_local.return_value = mock_vector_store
            mock_embeddings_instance = Mock()
            mock_embeddings.return_value = mock_embeddings_instance
            
            # LLMをモック
            mock_llm_instance = Mock()
            mock_llm.return_value = mock_llm_instance
            
            # RetrievalQAをモック
            mock_qa_chain = Mock()
            mock_qa.from_chain_type.return_value = mock_qa_chain
            
            # リトリーバーをモック
            mock_retriever = Mock()
            mock_vector_store.as_retriever.return_value = mock_retriever
            
            rag_server = RAGServer()
            result = rag_server.setup_retrieval_qa()
            
            # RetrievalQAが正しく設定されることを確認
            mock_qa.from_chain_type.assert_called_once()
            assert result == mock_qa_chain
    
    def test_query_processing(self):
        """🔴 Red: クエリ処理のテスト"""
        with patch('server.OpenAIEmbeddings'):
            
            rag_server = RAGServer()
            rag_server.qa_chain = Mock()
            rag_server.qa_chain.return_value = {"result": "テスト回答"}
            
            result = rag_server.process_query("テスト質問")
            
            assert result == "テスト回答"
            rag_server.qa_chain.assert_called_once_with({"query": "テスト質問"})


class TestFastAPIEndpoints:
    
    def setup_method(self):
        """各テストメソッドの前に実行される"""
        self.client = TestClient(app)
    
    def test_health_check_endpoint(self):
        """🔴 Red: ヘルスチェックエンドポイントのテスト"""
        response = self.client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    @patch('server.verify_jwt_token')
    @patch('server.rag_server')
    def test_query_endpoint_success(self, mock_rag_server, mock_verify_jwt):
        """🔴 Red: クエリエンドポイント成功のテスト"""
        # JWT認証をモック
        mock_verify_jwt.return_value = True
        
        # RAGサーバーの応答をモック
        mock_rag_server.process_query.return_value = "テスト回答"
        
        # テストリクエスト
        headers = {"Authorization": "Bearer valid_token"}
        payload = {"prompt": "PMBOKについて教えて"}
        
        response = self.client.post("/query", json=payload, headers=headers)
        
        assert response.status_code == 200
        assert response.json() == {"answer": "テスト回答"}
        mock_rag_server.process_query.assert_called_once_with("PMBOKについて教えて")
    
    @patch('server.verify_jwt_token')
    def test_query_endpoint_unauthorized(self, mock_verify_jwt):
        """🔴 Red: 認証失敗のテスト"""
        # JWT認証を失敗させる
        mock_verify_jwt.side_effect = Exception("Invalid token")
        
        headers = {"Authorization": "Bearer invalid_token"}
        payload = {"prompt": "テスト質問"}
        
        response = self.client.post("/query", json=payload, headers=headers)
        
        assert response.status_code == 401
        assert "invalid token" in response.json()["detail"].lower()
    
    def test_query_endpoint_missing_prompt(self):
        """🔴 Red: プロンプト欠如のテスト"""
        headers = {"Authorization": "Bearer valid_token"}
        payload = {}  # promptフィールドなし
        
        response = self.client.post("/query", json=payload, headers=headers)
        
        assert response.status_code == 422  # Validation Error


class TestJWTAuthentication:
    
    def test_verify_jwt_token_valid(self):
        """🔴 Red: 有効JWTトークン検証のテスト"""
        from server import verify_jwt_token
        
        # 有効なトークンのテスト
        with patch('server.jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "test_user"}
            
            result = verify_jwt_token("valid_token")
            assert result is True
            mock_decode.assert_called_once()
    
    def test_verify_jwt_token_invalid(self):
        """🔴 Red: 無効JWTトークン検証のテスト"""
        from server import verify_jwt_token
        
        # 無効なトークンのテスト
        with patch('server.jwt.decode') as mock_decode:
            mock_decode.side_effect = Exception("Invalid token")
            
            with pytest.raises(Exception):
                verify_jwt_token("invalid_token") 