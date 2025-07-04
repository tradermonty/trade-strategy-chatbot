import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import json
from server import app, RAGServer

class TestRAGServer:
    
    def test_rag_server_initialization(self):
        """🔴 Red: RAGServer initializationのテスト"""
        with patch('server.OpenAIEmbeddings'):
            rag_server = RAGServer()
            assert rag_server is not None
            assert hasattr(rag_server, 'vector_store')
            assert hasattr(rag_server, 'qa_chain')
            assert hasattr(rag_server, 'embeddings')
            assert hasattr(rag_server, 'prompt_template')
    
    def test_load_vector_store(self):
        """🔴 Red: ベクトルストア読み込みのテスト"""
        with patch('server.FAISS') as mock_faiss, \
             patch('server.OpenAIEmbeddings') as mock_embeddings, \
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
            rag_server.load_vector_store()
            
            # FAISSのload_localが正しく呼び出されることを確認
            mock_faiss.load_local.assert_called_once()
            assert rag_server.vector_store == mock_vector_store
    
    def test_setup_qa_chain(self):
        """🔴 Red: RetrievalQAセットアップのテスト"""
        with patch('server.FAISS') as mock_faiss, \
             patch('server.OpenAIEmbeddings') as mock_embeddings, \
             patch('server.ChatOpenAI') as mock_llm, \
             patch('server.RetrievalQA') as mock_qa:
            
            # ベクトルストアとプロンプトテンプレートのモック
            mock_vector_store = Mock()
            mock_prompt_template = Mock()
            
            rag_server = RAGServer()
            rag_server.vector_store = mock_vector_store
            rag_server.prompt_template = mock_prompt_template
            
            # QAチェーンのモック設定
            mock_qa_chain = Mock()
            mock_qa.from_chain_type.return_value = mock_qa_chain
            
            rag_server.setup_qa_chain()
            
            # RetrievalQAが正しく呼び出されることを確認
            mock_qa.from_chain_type.assert_called_once()
            assert rag_server.qa_chain == mock_qa_chain
    
    def test_query_processing(self):
        """🔴 Red: Process queryのテスト"""
        with patch('server.OpenAIEmbeddings'), \
             patch.object(RAGServer, 'get_system_prompt') as mock_get_prompt:
            
            # RAGサーバーのセットアップ
            rag_server = RAGServer()
            
            # QAチェーンのモック
            mock_qa_chain = Mock()
            mock_qa_chain.invoke.return_value = {
                "result": "テスト回答",
                "source_documents": [
                    Mock(metadata={"source": "test.md"})
                ]
            }
            rag_server.qa_chain = mock_qa_chain
            mock_get_prompt.return_value = "System prompt"
            
            # Process queryの実行
            result = rag_server.process_query("テスト質問")
            
            # 結果の確認
            assert "answer" in result
            assert "sources" in result
            assert "timestamp" in result
            assert result["answer"] == "テスト回答"
            mock_qa_chain.invoke.assert_called_once()


class TestFastAPIEndpoints:
    
    def setup_method(self):
        """各テストメソッドの前に実行される"""
        self.client = TestClient(app)
    
    @patch('server.rag_server')
    def test_health_check_endpoint(self, mock_rag_server):
        """🔴 Red: ヘルスチェックエンドポイントのテスト"""
        # RAGサーバーの状態をモック
        mock_rag_server.vector_store = Mock()
        mock_rag_server.qa_chain = Mock()
        
        response = self.client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data
        assert data["vector_store_loaded"] is True
        assert data["qa_chain_ready"] is True
    
    @patch('server.rag_server')
    def test_query_endpoint_success(self, mock_rag_server):
        """🔴 Red: クエリエンドポイント成功のテスト"""
        from server import app, verify_token
        
        # JWT認証の依存関係をオーバーライド
        def mock_verify_token():
            return {"sub": "test_user"}
        
        app.dependency_overrides[verify_token] = mock_verify_token
        
        # RAGサーバーの応答をモック
        mock_rag_server.process_query.return_value = {
            "answer": "テスト回答",
            "sources": ["test.md"],
            "timestamp": "2025-01-04T10:00:00"
        }
        
        try:
            # テストリクエスト
            headers = {"Authorization": "Bearer valid_token"}
            payload = {"query": "What are the main features?", "user_id": "test_user"}
            
            response = self.client.post("/query", json=payload, headers=headers)
            
            assert response.status_code == 200
            data = response.json()
            assert data["answer"] == "テスト回答"
            assert data["sources"] == ["test.md"]
        finally:
            # オーバーライドをクリア
            app.dependency_overrides.clear()
    
    def test_query_endpoint_unauthorized(self):
        """🔴 Red: 認証失敗のテスト"""
        headers = {"Authorization": "Bearer invalid_token"}
        payload = {"query": "テスト質問", "user_id": "test_user"}
        
        response = self.client.post("/query", json=payload, headers=headers)
        
        assert response.status_code == 401
    
    def test_query_endpoint_missing_query(self):
        """🔴 Red: クエリ欠如のテスト"""
        from server import app, verify_token
        
        # JWT認証の依存関係をオーバーライド
        def mock_verify_token():
            return {"sub": "test_user"}
        
        app.dependency_overrides[verify_token] = mock_verify_token
        
        try:
            headers = {"Authorization": "Bearer valid_token"}
            payload = {"user_id": "test_user"}  # queryフィールドなし
            
            response = self.client.post("/query", json=payload, headers=headers)
            
            assert response.status_code == 422  # Validation Error
        finally:
            # オーバーライドをクリア
            app.dependency_overrides.clear()


class TestJWTAuthentication:
    
    def test_create_access_token(self):
        """🔴 Red: Create access tokenのテスト"""
        from server import create_access_token
        
        test_data = {"sub": "test_user", "user_id": "123"}
        token = create_access_token(test_data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    @patch('server.jwt.decode')
    def test_verify_token_valid(self, mock_decode):
        """🔴 Red: 有効JWTToken verificationのテスト"""
        from server import verify_token
        from fastapi.security import HTTPAuthorizationCredentials
        
        # 有効なトークンのテスト
        mock_decode.return_value = {"sub": "test_user"}
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="valid_token")
        
        result = verify_token(credentials)
        assert result == {"sub": "test_user"}
        mock_decode.assert_called_once()
    
    @patch('server.jwt.decode')
    def test_verify_token_invalid(self, mock_decode):
        """🔴 Red: 無効JWTToken verificationのテスト"""
        from server import verify_token
        from fastapi.security import HTTPAuthorizationCredentials
        from jose import JWTError
        
        # 無効なトークンのテスト
        mock_decode.side_effect = JWTError("Invalid token")
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid_token")
        
        with pytest.raises(Exception):  # HTTPExceptionが発生
            verify_token(credentials)