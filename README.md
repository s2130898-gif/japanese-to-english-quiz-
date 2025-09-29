# 🇯🇵→🇺🇸 Japanese to English Translation Quiz System

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces)

## 概要 / Overview

**新しいアプローチの英語学習システム / Advanced AI-Powered English Learning System**

従来の「英文→日本語」ではなく、「日本語→英訳→英文同士比較」で評価します。
This innovative system evaluates Japanese-English translation skills using AI-powered similarity analysis.

## 🎯 システムの仕組み / How It Works

```
1. 日本語問題文を表示 / Display Japanese reference text
   ↓
2. ユーザーが日本語で回答 / User inputs their Japanese translation
   ↓
3. Google翻訳で自動英訳 / Auto-translate to English via Google Translate
   ↓
4. 正解英文とAI比較・採点 / AI-powered comparison and scoring with reference English
```

## ✨ 特徴 / Features

### 🔄 新しいアプローチ / New Approach
- **逆方向評価**: 日本語で理解→英語で比較 / Reverse evaluation: Japanese comprehension → English comparison
- **AI採点**: DistilBERT ベクトル類似度による客観評価 / AI scoring with DistilBERT vector similarity
- **翻訳スキル向上**: 日本語表現力も同時に鍛える / Improves both translation and expression skills

### 📊 AI評価システム / AI Evaluation System
1. **🧠 ベクトル類似度 (40%)**: DistilBERT による意味的類似性 / Vector similarity using DistilBERT
2. **🔤 単語類似度 (30%)**: 英単語の一致度 / English word matching accuracy
3. **📊 文字列類似度 (20%)**: 文字レベルの精度 / Character-level text similarity
4. **📏 構造類似度 (10%)**: 文長・構造の類似性 / Sentence structure similarity

### 📚 豊富な問題
- 20問のサンプル問題
- 技術・ビジネス・日常生活の3分野
- 難易度別の問題構成

## 🚀 クイックスタート / Quick Start

### 🌐 Web App (Hugging Face Spaces)

**Live Demo**: Access the web application directly on Hugging Face Spaces

### ローカル環境で実行 / Local Development

```bash
# 1. Clone the repository
git clone [repository-url]
cd japanese-to-english-quiz

# 2. Install dependencies / 必要なパッケージをインストール
pip install -r requirements.txt

# 3. Run the app / アプリを起動
streamlit run app.py

# 4. Open browser / ブラウザが自動で開きます
# Local URL: http://localhost:8501
```

### 🚀 Deploy to Hugging Face Spaces

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Choose **Streamlit** as the SDK
3. Upload these files to your Space repository:
   - `app.py` (main application)
   - `japanese_to_english_system.py`
   - `english_embeddings.py`
   - `google_translator.py`
   - `requirements.txt`
   - `README.md`
4. Your app will automatically deploy!

### 使い方

1. **「🎲 新しい問題を出題」**をクリック
2. 表示された日本語を読む
3. **自分なりの日本語**で表現し直す
4. **「📝 採点する」**をクリック
5. 結果を確認し、詳細分析を見る

## 📊 採点例

### 問題
```
元の日本語: 人工知能は私たちの生活を変えています。
正解英文: Artificial intelligence is changing our lives.
```

### ユーザーの回答例
```
あなたの回答: AIが私達の暮らしを変えている。
↓ (自動翻訳)
翻訳結果: AI is changing our lifestyle.
```

### 採点結果
```
📊 スコア: 85点 (グレード A)

🔤 単語類似度: 75% (ai≈artificial intelligence, changing, our)
📊 文字列類似度: 88% (構造がほぼ同じ)
📏 構造類似度: 92% (文長・語順が類似)

総合: 75%×0.5 + 88%×0.3 + 92%×0.2 = 85点
```

## 🎓 学習効果

### 従来システムとの比較

| 方式 | 従来 | 新方式 |
|------|------|--------|
| **入力** | 英文→日本語 | 日本語→日本語 |
| **評価** | 日本語同士比較 | 英文同士比較 |
| **課題** | 採点の主観性 | 翻訳精度に依存 |
| **効果** | 読解力向上 | 表現力+理解力 |

### 学習メリット
✅ **表現力向上**: 同じ意味を別の日本語で表現
✅ **理解度確認**: 本当に理解しているかテスト
✅ **客観評価**: 英文比較による公平な採点
✅ **逆方向思考**: 新しい角度からの英語学習

## 🛠️ 技術仕様

### ファイル構成
```
japanese-to-english-quiz/
├── japanese_to_english_system.py    # コアロジック
├── streamlit_japanese_to_english.py # GUI
├── requirements.txt                 # 依存パッケージ
└── README.md                       # このファイル
```

### 翻訳エンジン / Translation Engine
**Current**: Google Translate API (googletrans library)
**Previous**: MarianMT (Helsinki-NLP/opus-mt-ja-en) - switched due to quality issues

### AI技術 / AI Technology
- **Vector Embeddings**: DistilBERT (distilbert-base-uncased) with 768 dimensions
- **Similarity Calculation**: Cosine similarity with proper mean pooling
- **Translation**: Google Translate API for high-quality Japanese-English translation

### 評価アルゴリズム
```python
# 単語類似度（Jaccard係数）
word_similarity = |words1 ∩ words2| / |words1 ∪ words2|

# 文字列類似度（SequenceMatcher）
string_similarity = difflib.SequenceMatcher(text1, text2).ratio()

# 構造類似度（文長差）
structure_similarity = 1 - |len1 - len2| / max(len1, len2)

# 総合スコア
final_score = word_sim×0.5 + string_sim×0.3 + structure_sim×0.2
```

## 📈 拡張可能性

### 今後の改善案
1. **本格翻訳API**: Google Translate等の導入
2. **問題数追加**: 100問以上に拡張
3. **難易度調整**: 初級〜上級レベル別
4. **分野特化**: IT・医療・法律など専門分野
5. **音声対応**: 読み上げ・音声入力機能

### カスタマイズ
```python
# 重みの調整
weights = {
    'word': 0.6,      # 単語重視
    'string': 0.2,    # 文字列軽視
    'structure': 0.2  # 構造軽視
}

# 問題の追加
new_question = {
    "japanese": "新しい日本語問題",
    "english_reference": "New English reference",
    "topic": "カスタム"
}
```

## 🤔 従来システムとの使い分け

### このシステムが向いている場合
- 日本語表現力を鍛えたい
- 理解度を客観的に測りたい
- 新しいアプローチで学習したい
- 翻訳スキルも向上させたい

### 従来システムが向いている場合
- 英文読解力を直接鍛えたい
- 英語→日本語の変換に集中したい
- より正確な日本語評価が必要

## 📝 ライセンス

独立したJapanese to English Translation Quiz Systemです。

## 🔗 関連プロジェクト

- [English Quiz System](../english-quiz-system/) - 従来方式の英日翻訳システム

---

**新しいアプローチで英語学習を体験してください！** 🇯🇵→🇺🇸