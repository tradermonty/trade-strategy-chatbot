# 🎓 RAG Starter Kit

**10分で自分だけのAIアシスタントを作ってRAG技術を学ぼう**

*RAG（検索拡張生成）システムを理解し実装するための初心者向け教育用スターターテンプレート*

[🇺🇸 English](README.md) | 🇯🇵 日本語

## 📖 概要

RAG Starter Kitは、実装を通じてRAG技術を学び理解することを支援するよう設計されています。学生、教育者、AIが初めての開発者が最初のインテリジェントアシスタントを作るのに最適です。

**🎯 学習できること:**
- RAG（検索拡張生成）の仕組み
- ベクトル埋め込みとセマンティック検索
- LLM統合とプロンプトエンジニアリング
- FastAPIによる本格的なAPI構築
- 認証とセキュリティのベストプラクティス

**🚀 構築できるもの:**
10分未満でカスタムナレッジベースに関する質問に答える完全なAIアシスタント。

### 🎯 なぜRAG Starter Kit？

- **📚 教育最優先**: 段階的な説明付きの明確でコメント化されたコード
- **🚀 クイックスタート**: 10分でゼロから動作するAIアシスタント
- **🔧 実践的学習**: 核となるRAG概念を学びながら構築
- **🌉 本格運用への橋渡し**: より複雑なシステムの基盤
- **📖 完全チュートリアル**: 実例として日本料理レシピのナレッジベース付き
- **🎨 カスタマイズ可能**: 独自のユースケースに簡単に適応
- **🔐 セキュリティ込み**: JWT認証とベストプラクティス
- **💡 ベストプラクティス**: モダンなPython、FastAPI、AI開発パターン

## 🎯 プロジェクトの特徴

### ✨ 独自の価値

- 🎓 **教育的優秀性**: TDD手法、包括的ドキュメント
- ⚡ **即座に利用可能**: 複雑な設定不要
- 🎨 **カスタマイズ性**: YAML設定、ドメイン非依存
- 🍜 **実例豊富**: 日本料理レシピによる実用デモ
- 🔄 **効率的更新**: インクリメンタル更新機能


## 🏗️ 学習アーキテクチャ

*RAGシステムの内部動作を理解する*

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

*学習のためのモダンで業界標準のツール*

- **バックエンド**: FastAPI + Uvicorn *(・API開発を学ぶ)*
- **RAGエンジン**: LangChain + RetrievalQA *(・RAGパターンを理解)*
- **ベクターDB**: FAISS *(・セマンティック検索を学ぶ)*
- **埋め込み**: OpenAI text-embedding-3-small *(・ベクトル表現を理解)*
- **LLM**: OpenAI GPT-4 *(・モダンAIを体験)*
- **認証**: JWT *(・セキュリティ基礎を学ぶ)*
- **テスト**: pytest + TDD *(・ベストプラクティスを含む)*

## 🚀 クイックスタート - 初めてのAIアシスタント

*以下のステップで初めてのRAG駆動AIアシスタントを構築*

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
LLM_MODEL=gpt-4o
```

### 3. サンプルナレッジベースの探索

**📚 プリロード例: 日本料理レシピコレクション**

スターターキットには、RAGの動作を理解するための完全な日本料理レシピナレッジベースが含まれています：

```bash
# サンプルナレッジベースを探索
ls knowledge/
# 表示例: 01_basic_rice_dishes.md, 02_noodle_dishes.md, 等

# サンプルドキュメントを表示
cat knowledge/01_basic_rice_dishes.md
```

**🎯 学習機会**: 最適なRAG検索のために構造化された知識がどのように整理されているかを確認してください。

**🔄 後でカスタマイズ**: 構造を理解したら、独自のドキュメントで置き換えてください。

### 4. ベクターストア構築 *(・埋め込みを学ぶ)*

```bash
# ドキュメントを検索可能なベクトルに変換
python3 run_etl.py

# 🎓 ここで何が起きているか：
# 1. ドキュメントがチャンクに分割される
# 2. 各チャンクがベクトル埋め込みになる
# 3. 高速類似検索のためのFAISSインデックスが作成される
```

### 5. AIアシスタントを起動

```bash
# RAG駆動APIを起動
python3 server.py

# 🎉 AIアシスタントが動作中！
# アクセス: http://localhost:8000/docs でインタラクティブAPIドキュメントを確認
```

### 6. 初めての質問

```bash
# ヘルスチェック
curl http://localhost:8000/health

# 日本料理について質問してみましょう
python3 query_cli.py "親子丼の作り方を教えてください"

# 探索のための対話モード
python3 query_cli.py --interactive

# 🎓 こんな学習用質問を試してみてください：
# "日本料理の主な米料理の種類は何ですか？"
# "完美なすし米の作り方を教えてください"
# "ラーメンとうどんの違いは何ですか？"
```

## 🎨 カスタマイズガイド - 独自のモノにしよう

*基本を理解したら、あなたのドメイン用にカスタマイズ*

### 🔄 あなたのドメインへの適応

*独自のAIアシスタント作成のステップバイステップガイド*

1. **📚 ナレッジベースの置き換え**: 
   ```bash
   # サンプルデータをクリア
   rm knowledge/*.md
   
   # あなたのドキュメントを追加
   cp /path/to/your/docs/*.md knowledge/
   ```

2. **🎨 AIの動作をカスタマイズ**:
   ```bash
   # プロンプト設定を編集
   vim prompt/prompt.yaml
   
   # 🎓 学習ティップ: プロンプトがAIレスポンスをどのように形作るかを確認
   ```

3. **⚙️ パフォーマンス最適化**:
   ```bash
   # .envで設定を調整
   LLM_MODEL=gpt-3.5-turbo  # コスト効率的な学習用
   CHUNK_SIZE=1000          # 長いドキュメント用
   ```

4. **🔄 再構築とテスト**:
   ```bash
   python3 run_etl.py  # ベクターストア再構築
   python3 server.py   # カスタムアシスタントをテスト
   ```

### 🎯 学習プロジェクトアイデア

*このドメインでRAG開発を練習*

- **📖 個人的ナレッジベース**: あなたのノート、研究、ドキュメント
- **🏢 会社FAQ**: 社内知識、ポリシー、手順
- **🎓 学習アシスタント**: 教材、教科書、研究論文
- **🍳 レシピコレクション**: 日本料理の例のように、あなたの料理で
- **💼 技術ドキュメント**: APIドキュメント、トラブルシューティングガイド
- **📚 本の要約**: お気に入りの本用アシスタント作成

**🎓 教育価値**: 各ドメインがRAG最適化の異なる側面を教えてくれます

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
docker build -t rag-starter-kit .
docker run -p 8000:8000 --env-file .env rag-starter-kit
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