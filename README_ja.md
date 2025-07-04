# 🚀 汎用RAG APIシステム

**任意のドメインにカスタマイズ可能な本格運用対応のRAG（検索拡張生成）APIシステム**

[🇺🇸 English](README.md) | 🇯🇵 日本語

## 📖 概要

汎用RAG APIシステムは、最新のAI技術を使用して構築された柔軟でドメイン非依存の質問応答システムです。ナレッジベースとプロンプトを置き換えるだけで、技術文書からカスタマーサポート、法的文書から医療知識まで、あらゆる分野に特化したAIアシスタントを作成できます。

### 🎯 主要機能

- **🧠 ドメイン非依存設計**: 任意の知識領域に簡単に適応可能
- **🔍 高度なRAG技術**: LangChain + FAISS + OpenAI Embeddings
- **🔐 JWT認証**: 標準搭載のセキュアなAPI アクセス
- **⚡ 高性能**: 高速レスポンス時間に最適化
- **📚 柔軟なナレッジベース**: Markdownドキュメント対応
- **🎨 カスタマイズ可能プロンプト**: YAML ベースのプロンプト設定
- **🏗️ 本格運用対応**: スケーラブルなFastAPI構築
- **🔄 インクリメンタル更新**: 効率的なファイル単位更新機能

## 🏗️ アーキテクチャ

```
📱 クライアントアプリケーション
    ↓
🌐 FastAPIサーバー (server.py)
    ↓
🧠 LangChain RAG + OpenAI GPT-4
    ↓
📊 FAISSベクターストア
    ↓
📚 ナレッジベース (Markdownファイル)
```

### 🔧 技術スタック

- **バックエンド**: FastAPI + Uvicorn
- **RAGエンジン**: LangChain + RetrievalQA
- **ベクターDB**: FAISS (Facebook AI Similarity Search)
- **埋め込み**: OpenAI text-embedding-3-small
- **LLM**: OpenAI GPT-4 (設定可能)
- **認証**: JWT (JSON Web Tokens)
- **テスト**: pytest + TDD手法
- **更新機能**: インクリメンタル更新対応

## 🚀 クイックスタート

### 1. 環境セットアップ

```bash
# リポジトリクローン
git clone <repository-url>
cd rag-api

# Python仮想環境作成（Python 3.11推奨）
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係インストール
pip install -r requirements.txt
```

### 2. 設定

`.env`ファイルを作成:

```env
OPENAI_API_KEY=your-openai-api-key-here
JWT_SECRET_KEY=your-jwt-secret-key

# オプション設定
CHUNK_SIZE=800
CHUNK_OVERLAP=100
RETRIEVAL_K=6
LLM_TEMPERATURE=0.3
LLM_MODEL=gpt-4
```

### 3. ナレッジベースの準備

1. 既存のナレッジベースをクリア:
   ```bash
   rm knowledge/*.md
   ```

2. あなたのドメイン固有のドキュメントを追加:
   ```bash
   cp /path/to/your/documents/*.md knowledge/
   ```

3. プロンプト設定をカスタマイズ:
   ```bash
   vim prompt/prompt.yaml
   ```

### 4. ベクターストア構築

```bash
# 初回構築またはフル再構築
python3 run_etl.py --full

# インクリメンタル更新（推奨）
python3 run_etl.py

# 単一ファイル追加
python3 run_etl.py --add new_document.md

# システム状態確認
python3 run_etl.py --status
```

### 5. サーバー起動

```bash
python3 server.py
```

### 6. APIテスト

```bash
# ヘルスチェック
curl http://localhost:8000/health

# コマンドライン質問ツール
python3 query_cli.py "ここに質問を入力"

# 対話モード
python3 query_cli.py --interactive
```

## 🎨 カスタマイズガイド

### あなたのドメインへの適応

1. **ナレッジベース**: `knowledge/`ディレクトリにMarkdownドキュメントを配置
2. **プロンプトエンジニアリング**: `prompt/prompt.yaml`でAIアシスタントの動作を定義
3. **モデル選択**: `.env`で`LLM_MODEL`を更新（例: gpt-4, gpt-3.5-turbo）
4. **埋め込み戦略**: コンテンツタイプに応じて`CHUNK_SIZE`と`CHUNK_OVERLAP`を調整

### 適用例

- **技術文書**: ソフトウェアマニュアル、API仕様書、トラブルシューティングガイド
- **カスタマーサポート**: FAQ、製品情報、サポート手順
- **法的文書**: 契約書、ポリシー、規制コンプライアンス
- **医療知識**: 臨床ガイドライン、薬剤情報、プロトコル
- **教育コンテンツ**: 授業資料、教科書、研究論文

## 📊 API仕様

### エンドポイント

- `GET /` - ルートエンドポイント
- `GET /health` - ヘルスチェック
- `POST /login` - JWT認証
- `POST /query` - 質問送信と回答取得

### Query API例

```bash
# ログイン
curl -X POST "http://localhost:8000/login?username=demo_user&password=demo_password"

# 質問送信
curl -X POST "http://localhost:8000/query" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"query": "ここに質問を入力", "user_id": "user123"}'
```

### レスポンス形式

```json
{
  "answer": "詳細な回答内容...",
  "sources": ["document1.md", "document2.md"],
  "timestamp": "2025-01-04T10:30:00"
}
```

## 🔄 インクリメンタル更新機能

### 基本的な使用方法

```bash
# デフォルト: 変更されたファイルのみ更新
python3 run_etl.py

# フル再構築
python3 run_etl.py --full

# 単一ファイル追加
python3 run_etl.py --add new_recipe.md

# システム状態確認
python3 run_etl.py --status
```

### 更新機能の特徴

- **🔍 変更検知**: MD5ハッシュベースの効率的なファイル変更検知
- **📝 メタデータ管理**: ファイル処理履歴の自動追跡
- **⚡ 高速更新**: 変更されたファイルのみ処理
- **🛡️ 安全性**: 既存データを保護しながら部分更新

## 🧪 テスト

```bash
# 全テスト実行
python3 -m pytest tests/ -v

# 特定テストモジュール実行
python3 -m pytest tests/test_ingest.py -v
python3 -m pytest tests/test_server.py -v

# インクリメンタル更新テスト
python3 test_incremental.py
```

## 🎯 パフォーマンス最適化

### ベクターストア最適化

- **チャンクサイズ**: コンテンツ構造に応じて調整（デフォルト: 800トークン）
- **オーバーラップ**: コンテキスト継続性確保（デフォルト: 100トークン）
- **検索数**: コンテキストとパフォーマンスのバランス（デフォルト: 6チャンク）

### LLM設定

- **温度**: 事実回答は低く（0.1-0.3）、創造的回答は高く（0.7-0.9）
- **モデル選択**: 複雑な推論にはGPT-4、速度優先にはGPT-3.5-turbo

## 🐳 Dockerデプロイ

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python3 run_etl.py --force

EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

ビルド・実行:
```bash
docker build -t universal-rag-api .
docker run -p 8000:8000 --env-file .env universal-rag-api
```

## 🔒 セキュリティ考慮事項

### 🚨 **重要: デプロイ前の確認事項**

1. **⚠️ APIキーセキュリティ**:
   ```bash
   # ❌ 実際のAPIキーをgitにコミットしないでください
   # ✅ 環境変数を使用してください
   export OPENAI_API_KEY=your-real-api-key-here
   
   # ✅ またはシークレット管理システムを使用
   # AWS Secrets Manager, Azure Key Vault等
   ```

2. **🔐 認証設定**:
   ```bash
   # セキュアなJWTシークレット生成（32文字以上）
   python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
   
   # セキュアなデモ認証情報設定
   export DEMO_USERNAME=your-admin-username
   export DEMO_PASSWORD=your-secure-password
   ```

3. **🛡️ 本格運用セキュリティチェックリスト**:
   - [ ] 全通信でHTTPS（TLS/SSL）を使用
   - [ ] ユニークで暗号学的にセキュアなJWTシークレットキー生成
   - [ ] 環境変数経由での認証情報設定
   - [ ] APIエンドポイントのレート制限有効化
   - [ ] 包括的な入力検証実装
   - [ ] 適切なエラーハンドリング（情報漏洩回避）
   - [ ] セキュアヘッダー使用（CORS、CSP等）
   - [ ] 定期的なセキュリティ監査と依存関係更新

### 🔧 **セキュリティ設定**

- **JWTセキュリティ**: デフォルトで24時間でトークン期限切れ
- **FAISSセキュリティ**: `allow_dangerous_deserialization=True`使用 - 信頼できるデータソースを確保
- **環境変数**: 全ての機密データは環境変数で設定可能
- **デフォルト認証情報**: ハードコードから環境変数ベース認証に変更済み

## 📈 監視とログ

- **リクエストログ**: API使用状況とパフォーマンス追跡
- **エラーモニタリング**: 障害キャプチャとアラート
- **ベクターストアメトリクス**: 検索効果監視
- **LLM使用量**: トークン消費とコスト追跡

## 🚀 スケーリング戦略

1. **水平スケーリング**: ロードバランサー背後の複数APIインスタンスデプロイ
2. **ベクターストア**: 分散ソリューションへの移行検討（Chroma、Pinecone）
3. **キャッシング**: 頻繁なクエリのRedis実装
4. **非同期処理**: 重い操作のバックグラウンドジョブ使用

## 🤝 コントリビュート

1. リポジトリをフォーク
2. フィーチャーブランチ作成（`git checkout -b feature/amazing-feature`）
3. TDD手法でテスト作成
4. フィーチャー実装
5. 変更をコミット（`git commit -m 'Add amazing feature'`）
6. ブランチにプッシュ（`git push origin feature/amazing-feature`）
7. プルリクエスト作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 🛠️ トラブルシューティング

### よくある問題

1. **インポートエラー**: 仮想環境がアクティブ化されていることを確認
2. **APIキー問題**: OPENAI_API_KEYが正しく設定されていることを確認
3. **メモリエラー**: チャンクサイズを減らすかバッチ処理を実装
4. **レスポンス遅延**: GPT-3.5-turbo使用またはキャッシング実装を検討

### ヘルプ

- **ドキュメント**: このREADMEとインラインコードコメント
- **問題報告**: バグレポートと機能リクエストはGitHub Issues
- **デモ**: `python3 demo_runner.py`で対話的サンプル実行

## 🎮 デモとサンプル

### 対話的デモ実行

```bash
# フルデモシステム実行
python3 demo/demo_runner.py

# テストケース実行
python3 demo/test_cases.py
```

### サンプルナレッジベース

現在のシステムには**日本料理レシピ集**が含まれています:
- 基本のご飯もの（親子丼、カツ丼、チャーハン等）
- 麺類（ラーメン、うどん、そば等）
- 焼き物（照り焼き、唐揚げ、焼き鳥等）
- 煮物（肉じゃが、筑前煮、カレー等）
- 汁物（味噌汁、すまし汁、豚汁等）
- 副菜（きんぴらごぼう、ひじき煮等）
- 和菓子（だんご、どら焼き、わらび餅等）
- 基本技術（だしの取り方、調理法等）

---

**🚀 数分であなた独自のドメイン特化AIアシスタントを構築しましょう！**

*LangChain、FastAPI、OpenAIの力で実現*