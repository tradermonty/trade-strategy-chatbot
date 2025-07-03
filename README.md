# 🎯 PM実務コンシェルジュ RAG システム

**TDD手法で開発された現役PM向けの実務知識問い合わせシステム**

![PM Consultant](icons/20250703_0708_プロジェクト達成アイコン_simple_compose_01jz89v2grepev2navkn3aktqb.png)

## 📖 概要

PM実務コンシェルジュRAGシステムは、プロジェクトマネージャーの実務を支援するAI問い合わせシステムです。PMBOK、アジャイル開発、リスク管理などの専門知識を統合し、実践的なアドバイスを提供します。

### 🎯 主要機能

- **🧠 専門知識問い合わせ**: PMBOK、アジャイル、IT業界のベストプラクティス
- **🔍 RAG技術**: LangChain + FAISS + OpenAI Embeddings
- **🔐 JWT認証**: セキュアなAPI アクセス
- **⚡ 高速レスポンス**: 平均7秒以内の回答
- **📚 多様なソース**: 9つの専門ナレッジファイル統合

## 🏗️ アーキテクチャ

```
📱 Client Interface
    ↓
🌐 FastAPI Server (server.py)
    ↓
🧠 LangChain RAG + OpenAI GPT-4
    ↓
📊 FAISS Vector Store
    ↓
📚 Knowledge Base (9 Markdown files)
```

### 🔧 技術スタック

- **Backend**: FastAPI + Uvicorn
- **RAG Engine**: LangChain + RetrievalQA
- **Vector DB**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: OpenAI text-embedding-3-small
- **LLM**: OpenAI GPT-4
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: pytest + TDD

## 🚀 クイックスタート

### 1. 環境構築

```bash
# リポジトリクローン
git clone <repository-url>
cd project-management-agent

# Python仮想環境作成（Python 3.11推奨）
python3.11 -m venv venv
source venv/bin/activate

# 依存関係インストール
pip install -r requirements.txt
```

### 2. 環境変数設定

`.env`ファイルを作成：

```env
OPENAI_API_KEY=your-openai-api-key-here
JWT_SECRET_KEY=your-jwt-secret-key
```

### 3. ベクトルストア作成（初回のみ）

```bash
python3 run_etl.py
```

### 4. サーバー起動

```bash
python3 server.py
```

### 5. 動作確認

```bash
# ヘルスチェック
curl http://localhost:8000/health

# コマンドライン質問ツール
python3 query_cli.py "PMBOKとは何ですか？"

# 対話モード
python3 query_cli.py --interactive
```

## 🎪 デモ・プレゼンテーション

### 包括的ライブデモ

```bash
# 全機能自動テストデモ
python3 demo_runner.py

# ETL処理をスキップして高速デモ
python3 demo_runner.py --skip-etl

# インタラクティブモード（手動テスト用）
python3 demo_runner.py --interactive
```

### プレゼンテーション用テストケース

```bash
# ライブプレゼンテーション用デモ
python3 test_cases.py --demo

# カテゴリ別ベンチマークテスト
python3 test_cases.py --benchmark
```

## 📊 デモ結果サンプル

### ✅ システム性能
- **処理文書**: 9つのMarkdownファイル → 502チャンク
- **平均レスポンス**: 7.51秒
- **回答品質**: 196-578文字の詳細回答
- **ソース統合**: 最大4つのナレッジファイルから統合

### 🎯 対応可能な質問カテゴリ

| カテゴリ | 例 |
|---------|-----|
| **PMベーシック** | プロジェクトの三大制約、PM責任 |
| **アジャイル実践** | スクラム、スプリント、ベロシティ |
| **IT業界特化** | DevOps、クラウド移行、SaaS開発 |
| **リスク管理** | リスクレジスタ、遅延対策 |
| **ステークホルダー管理** | コンフリクト解決、コミュニケーション |

## 🧪 テスト

### 単体テスト実行

```bash
# 全テスト実行
python3 -m pytest tests/ -v

# ETL処理テスト
python3 -m pytest tests/test_ingest.py -v

# サーバーテスト
python3 -m pytest tests/test_server.py -v
```

### TDD開発履歴

1. **Phase 1**: ETL処理 (ingest.py) - Red-Green-Refactor x5回
2. **Phase 2**: RAGサーバー (server.py) - Red-Green-Refactor x6回
3. **Phase 3**: 統合テスト・デモ完成

## 🔧 API仕様

### エンドポイント

- `GET /` - ルートエンドポイント
- `GET /health` - ヘルスチェック
- `POST /login` - JWT認証ログイン
- `POST /query` - PM実務質問・回答

### API使用例

```bash
# ログイン
curl -X POST "http://localhost:8000/login?username=pm_user&password=demo_password"

# 質問送信
curl -X POST "http://localhost:8000/query" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"query": "アジャイル開発のリスク管理は？", "user_id": "test"}'
```

## 📚 ナレッジベース

システムには以下9つの専門ナレッジファイルが統合されています：

1. **PMBOK第6-8版構造比較** - PMBOK進化の全体像
2. **PMBOK GPT知識設計** - AI×PM知識体系
3. **PMBOK×PRINCE2×ITIL 4×ISO 21502マッピング** - 標準の統合比較
4. **PMIコンパニオン標準（IT業界向け）** - IT特化のPM標準
5. **Software & SaaS業界PMベストプラクティス** - 実践的Q&A
6. **プロジェクトスケジューリング・リスク管理** - 詳細調査
7. **IT業界PMリソース** - 最新動向・ツール
8. **AI・ハイブリッドワーク・ESG影響** - 現代PM課題
9. **PMP・PgMP学習ロードマップ** - 資格取得ガイド

## 🎯 プレゼンテーション・ハイライト

### 🏆 TDD成功ストーリー
- **10回以上のRed-Green-Refactorサイクル**
- **テストファースト開発**で堅牢性確保
- **継続的リファクタリング**でコード品質向上

### 🚀 技術的成果
- **LangChain RAG**の実装
- **FAISS**による高速ベクトル検索
- **JWT認証**によるセキュリティ
- **FastAPI**の非同期処理

### 📈 ビジネス価値
- **PM実務の効率化** - 即座に専門知識にアクセス
- **判断支援** - 複数ソースからの統合回答
- **学習支援** - 体系的な知識提供
- **チーム共有** - 標準化された知識ベース

## 🔮 次のステップ

### Option B: 機能拡張
- **プロンプト系統強化** - prompt/project_management_prompt.yaml活用
- **ログ機能** - 使用状況・品質分析
- **エラーハンドリング強化** - 例外処理・フォールバック

### Option C: Docker化・MCP連携
- **Docker化** - ポータブルなデプロイメント
- **MCP統合** - Model Context Protocol対応
- **クラウド展開** - AWS/GCP/Azure対応

## 🤝 コントリビューション

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests first (TDD approach)
4. Implement your feature
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 ライセンス

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 サポート

- **Issues**: GitHub Issues
- **Documentation**: このREADME
- **Demo**: `python3 demo_runner.py`

---

**🎯 現役PMの、現役PMによる、現役PMのためのRAGシステム**

*Developed with ❤️ using TDD methodology* 