# MCP × LangChain RAG サーバー設計書  

**Version 1.0 — 2025-07-03**  

現役 PM 向け「PM実務コンシェルジュ GPT」を  
- **Markdown ナレッジベース**（9 モジュール）  
- **LangChain Retrieval-Augmented Generation (RAG)**  
- **FastAPI Web API**  
でホストし、**MCP** から HTTP 経由で呼び出すための設計をまとめる。  

---

## 1. システム概要図  

```text
┌───────────┐      HTTPS (JSON)      ┌───────────────────────┐
│   MCP     │ ─────────────────────▶ │  RAG API (FastAPI)    │
└───────────┘                       │  • Auth (JWT)          │
                                     │  • Retriever (FAISS)   │
                                     │  • LLM (OpenAI o3)     │
                                     └────────┬──────────────┘
                                              │
                      VectorStore.load()      │
                                              ▼
                                      FAISS index (local)
                                              ▲
                                      ingest.py (ETL)
                                              ▲
                                      knowledge/*.md
````

---

## 2. ディレクトリ構成

```
project-root/
│
├─ knowledge/                # 9 モジュールの .md
│   ├─ 1_pmbok_evolution.md
│   └─ …
│
├─ ingest.py                 # Markdown → Embedding → FAISS
├─ server.py                 # FastAPI + LangChain
│
├─ prompts/
│   └─ system.yaml           # カスタムGPT Instruction
│
├─ requirements.txt
└─ Dockerfile                # optional
```

---

## 3. コンポーネント詳細

| レイヤ                 | 技術 / ライブラリ                                   | 主な責務                                          |
| ------------------- | -------------------------------------------- | --------------------------------------------- |
| **Knowledge Store** | Markdown + `langchain.text_splitter`         | 800 token/100 overlap で段落分割                   |
| **Embedding**       | `OpenAIEmbeddings` (text-embedding-3-small)  | 日本語混在でも高精度                                    |
| **Vector DB**       | `faiss-cpu` (on-disk)                        | `vector_store/` に保存                           |
| **Retriever**       | `VectorStoreRetriever`                       | `search_kwargs={k:6}`                         |
| **LLM**             | `ChatOpenAI(model="o3")`                     | `temperature=0.3`                             |
| **Prompt**          | `ChatPromptTemplate`                         | system=Instruction, human = 問合せ + context     |
| **API**             | FastAPI `/query` POST                        | req body `{prompt:str}` → resp `{answer:str}` |
| **Auth**            | JWT (Header `Authorization: Bearer <token>`) | MCP にトークン登録                                   |
| **Deployment**      | Docker + Uvicorn `--workers 2`               | 任意の IaaS/FaaS                                 |

---

## 4. 処理フロー

1. **ETL** (`ingest.py`)

   1. Markdown を読み込み → スプリット。
   2. OpenAI で埋め込み作成。
   3. FAISS index を `vector_store/` に保存。
2. **API 呼び出し**

   1. MCP が `/query` に JSON `{prompt}` を POST。
   2. FastAPI で JWT 認証 → LangChain RetrievalQA 実行。
   3. Retriever が Top-k チャンク取得 → Prompt に挿入。
   4. LLM が回答生成。
   5. 回答を JSON 返却（将来: ソースチャンク配列も返せるよう拡張）。

---

## 5. インタフェース仕様

### 5.1 HTTP リクエスト

```
POST /query
Authorization: Bearer <JWT>
Content-Type: application/json

{
  "prompt": "<ユーザー質問テキスト>"
}
```

### 5.2 HTTP レスポンス

```json
{
  "answer": "…生成された日本語回答…"
}
```

> ※将来的に `sources` 配列（参照 markdown ファイル名 & ページ範囲）を追加し、MCP 側で引用表示へ拡張可能。

### 5.3 MCP 連携例

`mission-control.yaml` の一例（抜粋）

```yaml
tasks:
  - id: pm_assistant
    type: web_api
    endpoint: "https://rag.example.com/query"
    method: POST
    headers:
      Authorization: "Bearer ${RAG_JWT}"
    input_mapping:
      prompt: "${task_input}"
    output_mapping:
      "${task_result}": "answer"
```

---

## 6. セキュリティ設計

| 項目              | 方針                                       |
| --------------- | ---------------------------------------- |
| **通信**          | TLS 1.2+                                 |
| **認証**          | MCP 発行の長寿命 JWT もしくは OAuth2 Client Creds  |
| **LLM API Key** | `.env` に保存。Docker secret / Vault 推奨      |
| **監査ログ**        | FastAPI middleware でリクエスト/応答・ベクトル参照ログを出力 |

---

## 7. 非機能要件

| 区分            | 目標値 / 方針                                               |
| ------------- | ------------------------------------------------------ |
| **レイテンシ**     | 1 問合せ ≤ 3 s (o3 利用時)                                   |
| **同時接続**      | FastAPI workers × CPU コア / autoscale                   |
| **スケーラビリティ**  | FAISS on-disk → 必要に応じ `Chroma + PgVector` へ            |
| **更新頻度**      | ナレッジ更新時に `ingest.py` 再実行（GitHub Actions で自動化可）         |
| **DR/バックアップ** | `knowledge/*.md` と `vector_store` を git + S3 へ定期バックアップ |

---

## 8. エラーハンドリング & リトライ

| ケース               | HTTP ステータス | メッセージ例                     |
| ----------------- | ---------- | -------------------------- |
| 認証失敗              | 401        | `"invalid token"`          |
| LLM API RateLimit | 503        | `"LLM backend busy"`       |
| 埋め込みサービス障害        | 502        | `"embedding service down"` |
| ベクトル DB 未初期化      | 500        | `"vector store missing"`   |
| パラメータ不足           | 422        | `"prompt field required"`  |

---

## 9. 今後の拡張ロードマップ

| フェーズ | 内容                                       |
| ---- | ---------------------------------------- |
| v1.1 | 回答 JSON に `sources[]` 追加 → MCP 側で引用リンク表示 |
| v1.2 | マルチテナント対応 (namespace per org)            |
| v1.3 | Streaming 応答 / SSE によるタイピング表示            |
| v2.0 | ベクトル DB をクラスタブルな Chroma or PGVector に置換  |

---

## 10. 参考コードスニペット

### ingest.py

```python
from pathlib import Path
from langchain.text_splitter import MarkdownTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

EMB = OpenAIEmbeddings(model="text-embedding-3-small")
docs = []
splitter = MarkdownTextSplitter(chunk_size=800, chunk_overlap=100)

for md in Path("knowledge").glob("*.md"):
    for chunk in splitter.split_text(md.read_text()):
        docs.append({"page_content": chunk, "metadata": {"source": md.name}})

FAISS.from_documents(docs, EMB).save_local("vector_store")
```

### server.py（抜粋）

```python
from fastapi import FastAPI, HTTPException, Header
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel
from pathlib import Path

app = FastAPI()
vs = FAISS.load_local("vector_store", OpenAIEmbeddings())
retriever = vs.as_retriever(search_kwargs={"k": 6})

SYS = Path("prompts/system.yaml").read_text()
prompt = ChatPromptTemplate.from_messages([
    ("system", SYS),
    ("human", "{question}\n\n[参考情報]\n{context}")
])
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="o3", temperature=0.3),
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt}
)

class Q(BaseModel):
    prompt: str

def verify(token: str): ...
    
@app.post("/query")
def ask(q: Q, authorization: str = Header(...)):
    verify(authorization.replace("Bearer ", ""))
    result = qa({"query": q.prompt})
    return {"answer": result["result"]}
```

---

### さいごに

本設計をベースにまず **ローカル動作 → Docker化 → MCP 登録** の順で進めれば、最短 1 日程度で MVP をリリースできます。運用しながらベクトル DB や LLM モデルのチューニング、ソース引用機能の拡充を行い、PM 実務の「社内ナレッジ・コパイロット」として育てていくことを推奨します。

