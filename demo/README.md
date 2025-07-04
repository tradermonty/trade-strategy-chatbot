# Demo Scripts

このフォルダにはUniversal RAG Systemのデモ用スクリプトが含まれています。

## ファイル構成

### `demo_runner.py`
- **用途**: 包括的なライブデモ実行スクリプト
- **機能**:
  - システム要件チェック
  - ETL プロセス自動実行
  - サーバー起動
  - 包括的なデモテスト実行
  - インタラクティブデモ

### `test_cases.py`
- **用途**: プレゼンテーション・ベンチマーク用テストケース
- **機能**:
  - プレゼンテーション用デモ
  - カテゴリー別ベンチマーク
  - ライブデモ用クエリ

## 使用方法

### 1. 包括的なデモを実行

```bash
# プロジェクトルートから実行
python demo/demo_runner.py

# または対話モードで実行
python demo/demo_runner.py --interactive
```

### 2. テストケースの実行

```bash
# プレゼンテーション用デモ
python demo/test_cases.py

# またはPythonから実行
python -c "from demo.test_cases import run_presentation_demo; run_presentation_demo()"
```

### 3. カテゴリー別ベンチマーク

```bash
python -c "from demo.test_cases import run_category_benchmark; run_category_benchmark()"
```

## 注意事項

1. **事前準備**: サーバーが起動していることを確認してください
2. **環境変数**: `.env` ファイルに `OPENAI_API_KEY` が設定されていることを確認してください
3. **ナレッジベース**: `knowledge/` フォルダに `.md` ファイルが存在することを確認してください

## デモ用質問カテゴリ

- システム概要
- 機能紹介
- 統合方法
- パフォーマンス特性
- スケーラビリティ
- セキュリティ考慮事項
- トラブルシューティング
- ベストプラクティス 