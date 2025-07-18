# CPPI Portfolio Insurance Strategy - アーニー・チャン式戦略
定率ポートフォリオ保険戦略

## 概要 / Overview

CPPI（Constant Proportion Portfolio Insurance）は、下落リスクを制限しながら上昇機会を捉える動的ポートフォリオ戦略です。アーニー・チャン氏の改良版は、最大ドローダウン制御とKelly基準を組み合わせた実践的アプローチを提供します。

## 基本原理 / Core Principles

### 二口座システム
**資金配分**:
- **取引口座**: 総資産のD%（リスク運用部分）
- **現金口座**: 総資産の(1-D)%（安全資産部分）
- D = 許容最大ドローダウン率（例：20%）

**基本ルール**:
- 新高値更新時：利益の(1-D)%を現金口座に移転
- 高値未更新時：現金口座は変更せず、取引口座のみ増減
- 最大損失：設定ドローダウンD%で制限

### ハイウォーターマーク管理
**リバランス条件**:
```
新高値時：S_t = (1-D) × W_t, Γ_t = D × W_t
非高値時：S_t = S_{t-1}, Γ_t = W_t - S_{t-1}
```
- W_t: 現在総資産
- S_t: 現金口座残高
- Γ_t: 取引口座残高

## Kelly基準との組合せ / Kelly Criterion Integration

### レバレッジ計算
**Kelly最適レバレッジ**:
```
K = μ/σ² (期待リターン÷分散)
```

**実装方法**:
- 取引口座に対してKellyレバレッジK倍を適用
- 全資産ベースでは実質 K×D倍のエクスポージャー
- 損失時の自動デレバレッジ効果

### リスク制御メカニズム
**ドローダウン制限**:
- 総資産 ≥ 過去最高値 × (1-D)
- 取引口座が0になるとD%の損失で停止
- 現金口座は常に非減少（利益ロック機能）

## 実装例 / Implementation Example

### パラメータ設定
**保守的設定**:
- 最大ドローダウン：D = 0.15（15%）
- Kellyレバレッジ：K = 1.5
- リバランス頻度：日次

**積極的設定**:
- 最大ドローダウン：D = 0.25（25%）
- Kellyレバレッジ：K = 2.0
- リバランス頻度：日次

### 計算手順
1. **初期配分**: 取引口座25%、現金口座75%
2. **高値更新時**: 利益の75%を現金口座に移転
3. **損失時**: 取引口座のみ減少、現金口座は維持
4. **停止条件**: ドローダウンが25%に達した時点

## パフォーマンス特性 / Performance Characteristics

### 期待効果
**リターン特性**:
- 上昇相場：レバレッジ効果で市場を上回る
- 下落相場：ドローダウン制限で損失を抑制
- 長期成長率：Kelly基準により理論最適に近似

**リスク特性**:
- 最大ドローダウン：設定値D%で確実に制限
- ボラティリティ：動的レバレッジにより市場追随
- 尖度・歪度：オプション類似の非対称分布

### シミュレーション結果例
**期待パフォーマンス**（D=20%設定）:
- 年率リターン：15.2%（vs市場10.5%）
- ボラティリティ：18.8%（vs市場15.2%）
- シャープレシオ：0.81（vs市場0.69）
- 最大ドローダウン：19.8%（vs市場-35.2%）

## 従来CPPI との比較 / vs Traditional CPPI

### アーニー・チャン改良点
**ドローダウン重視**:
- 従来：フロア値の絶対保護
- チャン式：相対ドローダウン制限

**利益管理**:
- 従来：満期時一括精算
- チャン式：高値更新時の段階的利確

**レバレッジ**:
- 従来：固定マルチプライヤー
- チャン式：Kelly基準による最適化

### 実践上の優位性
1. **明確な損失限度**: D%という分かりやすい基準
2. **利益の段階確保**: 高値更新毎の部分利確
3. **理論的最適性**: Kelly基準による成長率最大化
4. **心理的受容性**: ドローダウン制限による安心感

## 実装時の注意点 / Implementation Considerations

### 取引コスト影響
**頻繁リバランス**:
- 高値更新時の資金移動コスト
- レバレッジ調整時の取引手数料
- 税務上の実現損益処理

**コスト軽減策**:
- リバランス閾値の設定（±1%以上の変動時のみ）
- 税効率的な口座活用（IRA等）
- 低コスト商品の選択（ETF等）

### 商品選択基準
**リスク資産**:
- 流動性の高い資産（株式インデックス等）
- ボラティリティが適度（年率15-25%）
- 長期期待リターンが正

**安全資産**:
- 元本保証性（預金、国債等）
- 流動性確保（即座の換金可能）
- 金利収入（可能な範囲で）

## 心理的効果とメリット / Psychological Benefits

### 投資家心理
**安心感の提供**:
- 明確な損失限度の設定
- 段階的な利益確保の実感
- システマティックな判断基準

**行動バイアス軽減**:
- 感情的売買の防止
- 損切りルールの自動化
- 利確タイミングの体系化

### 長期継続性
**戦略の持続可能性**:
- 大損失による戦略放棄の回避
- 一定の成功体験による継続意欲
- 規律ある投資行動の習慣化

CPPI戦略は理論的優位性と実践的有用性を兼ね備えた、リスク制御型成長戦略として、長期資産形成に適した手法です。特にアーニー・チャン式の改良版は、現代的なリスク管理ニーズに対応した実用的なアプローチを提供します。