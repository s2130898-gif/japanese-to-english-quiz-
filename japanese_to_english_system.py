"""
Japanese to English Translation Quiz System
日本語和訳を英訳に変換して、英文同士で評価するシステム
"""
import random
import re
import numpy as np
from difflib import SequenceMatcher
from collections import Counter
import requests
import json
from typing import Dict, List, Tuple

try:
    from english_embeddings import EnglishEmbeddings
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("[WARNING] Vector embedding model not available (running in lightweight mode)")

try:
    from google_translator import GoogleTranslator
    GOOGLE_TRANSLATOR_AVAILABLE = True
except ImportError:
    GOOGLE_TRANSLATOR_AVAILABLE = False
    print("[WARNING] No translation modules available")

# ai_translator は使用しない（Google翻訳のみ）
AI_TRANSLATOR_AVAILABLE = False

class JapaneseToEnglishSystem:
    def __init__(self):
        self.current_question = None
        self.score_history = []
        self.sample_questions = self._load_sample_questions()

        # ベクトル埋め込みモデルの初期化
        if EMBEDDINGS_AVAILABLE:
            try:
                self.embeddings = EnglishEmbeddings()
                self.use_embeddings = True
                print("[AI MODE] Vector similarity calculation available")
            except Exception as e:
                self.embeddings = None
                self.use_embeddings = False
                print(f"[WARNING] Failed to initialize embedding model: {e}")
        else:
            self.embeddings = None
            self.use_embeddings = False

        # 翻訳モデルの初期化 (Google翻訳のみ使用)
        if GOOGLE_TRANSLATOR_AVAILABLE:
            try:
                self.translator = GoogleTranslator()
                self.use_ai_translation = self.translator.available
                if self.use_ai_translation:
                    print("[SUCCESS] Google Translate initialized for high-quality translation")
                else:
                    print("[WARNING] Google Translate not available")
            except Exception as e:
                self.translator = None
                self.use_ai_translation = False
                print(f"[WARNING] Failed to initialize Google Translate: {e}")
        else:
            self.translator = None
            self.use_ai_translation = False
            print("[WARNING] Google Translate not available")

        print("Japanese to English Translation System initialized")

    def _load_sample_questions(self) -> List[Dict]:
        """サンプル問題を読み込み"""
        return [
            {
                "id": 1,
                "japanese": "人工知能は私たちの生活を変えています。",
                "english_reference": "Artificial intelligence is changing our lives.",
                "topic": "Technology"
            },
            {
                "id": 2,
                "japanese": "このプロジェクトは来月までに完成する予定です。",
                "english_reference": "This project is scheduled to be completed by next month.",
                "topic": "Business"
            },
            {
                "id": 3,
                "japanese": "彼女は毎朝公園でジョギングをしています。",
                "english_reference": "She goes jogging in the park every morning.",
                "topic": "Daily Life"
            },
            {
                "id": 4,
                "japanese": "コンピュータのパフォーマンスを向上させる必要があります。",
                "english_reference": "We need to improve the computer's performance.",
                "topic": "Technology"
            },
            {
                "id": 5,
                "japanese": "明日の会議で新しい提案を発表します。",
                "english_reference": "I will present a new proposal at tomorrow's meeting.",
                "topic": "Business"
            },
            {
                "id": 6,
                "japanese": "子供たちは公園で楽しく遊んでいます。",
                "english_reference": "The children are playing happily in the park.",
                "topic": "Daily Life"
            },
            {
                "id": 7,
                "japanese": "機械学習アルゴリズムは大量のデータを処理できます。",
                "english_reference": "Machine learning algorithms can process large amounts of data.",
                "topic": "Technology"
            },
            {
                "id": 8,
                "japanese": "チームワークが成功の鍵です。",
                "english_reference": "Teamwork is the key to success.",
                "topic": "Business"
            },
            {
                "id": 9,
                "japanese": "今日は天気が良いので散歩に行きましょう。",
                "english_reference": "The weather is nice today, so let's go for a walk.",
                "topic": "Daily Life"
            },
            {
                "id": 10,
                "japanese": "この新しいアプリは使いやすく設計されています。",
                "english_reference": "This new app is designed to be user-friendly.",
                "topic": "Technology"
            },
            {
                "id": 11,
                "japanese": "売上を増やすために新しい戦略が必要です。",
                "english_reference": "We need a new strategy to increase sales.",
                "topic": "Business"
            },
            {
                "id": 12,
                "japanese": "彼は毎晩本を読む習慣があります。",
                "english_reference": "He has a habit of reading books every night.",
                "topic": "Daily Life"
            },
            {
                "id": 13,
                "japanese": "クラウドコンピューティングは柔軟性を提供します。",
                "english_reference": "Cloud computing provides flexibility.",
                "topic": "Technology"
            },
            {
                "id": 14,
                "japanese": "顧客満足度を向上させることが重要です。",
                "english_reference": "It is important to improve customer satisfaction.",
                "topic": "Business"
            },
            {
                "id": 15,
                "japanese": "家族との時間を大切にしています。",
                "english_reference": "I value time spent with my family.",
                "topic": "Daily Life"
            },
            {
                "id": 16,
                "japanese": "セキュリティは最優先事項です。",
                "english_reference": "Security is the top priority.",
                "topic": "Technology"
            },
            {
                "id": 17,
                "japanese": "効率的な業務プロセスを確立する必要があります。",
                "english_reference": "We need to establish efficient business processes.",
                "topic": "Business"
            },
            {
                "id": 18,
                "japanese": "週末は友人と映画を見に行きます。",
                "english_reference": "I'm going to see a movie with friends on the weekend.",
                "topic": "Daily Life"
            },
            {
                "id": 19,
                "japanese": "データの分析により重要な洞察が得られます。",
                "english_reference": "Data analysis provides important insights.",
                "topic": "Technology"
            },
            {
                "id": 20,
                "japanese": "市場調査は製品開発に不可欠です。",
                "english_reference": "Market research is essential for product development.",
                "topic": "Business"
            }
        ]

    def get_random_question(self) -> Dict:
        """ランダムに問題を選択"""
        question = random.choice(self.sample_questions)
        self.current_question = question
        return question

    def translate_japanese_to_english(self, japanese_text: str) -> str:
        """日本語を英訳（Google翻訳 or AI翻訳 or モック翻訳）"""
        if self.use_ai_translation and self.translator:
            return self.translator.translate(japanese_text)
        else:
            return self.translate_japanese_to_english_mock(japanese_text)

    def translate_japanese_to_english_mock(self, japanese_text: str) -> str:
        """
        日本語を英訳するモック関数
        実際のシステムでは翻訳APIを使用
        """
        # シンプルな変換ルール（デモ用）
        translations = {
            "人工知能": "artificial intelligence",
            "機械学習": "machine learning",
            "データ": "data",
            "コンピュータ": "computer",
            "プロジェクト": "project",
            "会議": "meeting",
            "チーム": "team",
            "システム": "system",
            "アプリ": "app",
            "セキュリティ": "security",
            "プロセス": "process",
            "分析": "analysis",
            "開発": "development",
            "生活": "life",
            "公園": "park",
            "子供": "children",
            "家族": "family",
            "友人": "friends",
            "映画": "movie",
            "散歩": "walk",
            "ジョギング": "jogging",
            "読書": "reading",
            "本": "book",
            "彼女": "she",
            "彼": "he",
            "私たち": "we",
            "変える": "change",
            "完成する": "complete",
            "向上させる": "improve",
            "発表する": "present",
            "遊ぶ": "play",
            "処理する": "process",
            "成功": "success",
            "散歩": "walk",
            "設計": "design",
            "増やす": "increase",
            "読む": "read",
            "提供する": "provide",
            "大切": "value",
            "効率的": "efficient",
            "重要": "important",
            "不可欠": "essential"
        }

        # 基本的な変換を試行
        result = japanese_text.lower()

        # 句読点を除去
        result = re.sub(r'[。、！？]', '', result)

        # 簡単な単語置換
        for jp, en in translations.items():
            if jp in japanese_text:
                result = result.replace(jp, en)

        # パターンマッチング翻訳（拡張版）
        translation_patterns = {
            # 人工知能関連
            "人工知能": "artificial intelligence",
            "AI": "artificial intelligence",
            "生活を変え": "changing our lives",
            "暮らしを変え": "changing our lifestyle",
            "私たちの": "our",
            "私達の": "our",

            # プロジェクト関連
            "プロジェクト": "project",
            "来月": "next month",
            "完成": "complete",
            "予定": "scheduled",

            # 日常生活関連
            "毎朝": "every morning",
            "公園": "park",
            "ジョギング": "jogging",
            "散歩": "walk",
            "子供": "children",
            "楽しく": "happily",
            "遊ん": "playing",
            "家族": "family",
            "友人": "friends",
            "映画": "movie",
            "本": "book",
            "読む": "read",
            "時間": "time",

            # ビジネス関連
            "会議": "meeting",
            "提案": "proposal",
            "発表": "present",
            "チーム": "team",
            "成功": "success",
            "効率的": "efficient",
            "重要": "important",
            "顧客": "customer",
            "満足": "satisfaction",
            "市場": "market",
            "調査": "research",

            # 技術関連
            "機械学習": "machine learning",
            "データ": "data",
            "処理": "process",
            "分析": "analysis",
            "コンピュータ": "computer",
            "パフォーマンス": "performance",
            "向上": "improve",
            "アプリ": "app",
            "設計": "design",
            "使いやすい": "user friendly",
            "セキュリティ": "security",
            "システム": "system",

            # 動詞
            "変えて": "changing",
            "変える": "change",
            "向上させる": "improve",
            "提供する": "provide",
            "確立する": "establish",
            "増やす": "increase",

            # 形容詞・副詞
            "新しい": "new",
            "良い": "good",
            "天気": "weather",
            "今日": "today",
            "週末": "weekend",
            "毎晩": "every night",
            "習慣": "habit",
            "大切": "important",
            "柔軟": "flexible",
            "最優先": "top priority"
        }

        # より柔軟な翻訳処理
        result_words = []

        # 基本的な単語置換
        words = japanese_text.replace('、', ' ').replace('。', ' ').split()
        for word in words:
            translated = False
            for jp_pattern, en_word in translation_patterns.items():
                if jp_pattern in word:
                    result_words.append(en_word)
                    translated = True
                    break
            if not translated and word.strip():
                # カタカナをそのまま英語として扱う
                if re.match(r'^[ァ-ヴー]+$', word):
                    result_words.append(word)
                else:
                    result_words.append(f"[{word}]")

        # 結果を結合
        if result_words:
            basic_translation = " ".join(result_words)
        else:
            basic_translation = "basic translation result"

        # より具体的なパターンマッチング
        if "人工知能" in japanese_text and "生活" in japanese_text:
            return "artificial intelligence is changing our lives"
        elif "AI" in japanese_text and ("生活" in japanese_text or "暮らし" in japanese_text):
            return "AI is changing our lifestyle"
        elif "プロジェクト" in japanese_text and "完成" in japanese_text:
            return "this project will be completed"
        elif "ジョギング" in japanese_text and "公園" in japanese_text:
            return "jogging in the park"
        elif "会議" in japanese_text and "提案" in japanese_text:
            return "proposal at the meeting"
        elif "子供" in japanese_text and "遊ん" in japanese_text:
            return "children are playing"
        elif "機械学習" in japanese_text and "データ" in japanese_text:
            return "machine learning processes data"
        elif "チームワーク" in japanese_text and "成功" in japanese_text:
            return "teamwork leads to success"
        elif "天気" in japanese_text and "散歩" in japanese_text:
            return "good weather for walking"
        elif "アプリ" in japanese_text and "設計" in japanese_text:
            return "app design"
        else:
            # フォールバック: 基本翻訳を返す
            return basic_translation.lower()

    def calculate_english_similarity(self, translated_text: str, reference_text: str) -> Dict:
        """英文同士の類似度を計算"""

        # 前処理
        trans_clean = self._clean_english_text(translated_text)
        ref_clean = self._clean_english_text(reference_text)

        # 1. 単語レベルの類似度
        word_similarity, word_details = self._calculate_word_similarity(trans_clean, ref_clean)

        # 2. 文字列類似度
        string_similarity = self._calculate_string_similarity(trans_clean, ref_clean)

        # 3. 構造類似度
        structure_similarity = self._calculate_structure_similarity(trans_clean, ref_clean)

        # 4. ベクトル類似度（AIモード）
        vector_similarity = 0.0
        if self.use_embeddings:
            try:
                vector_similarity = self.embeddings.calculate_similarity(trans_clean, ref_clean)
            except Exception as e:
                print(f"ベクトル類似度計算エラー: {e}")
                vector_similarity = 0.0

        # 総合スコア計算（4つの指標を使用）
        if self.use_embeddings and vector_similarity > 0:
            # AIモード: ベクトル類似度も含める
            weights = {
                'vector': 0.4,    # ベクトル類似度 (40%)
                'word': 0.3,      # 単語類似度 (30%)
                'string': 0.2,    # 文字列類似度 (20%)
                'structure': 0.1  # 構造類似度 (10%)
            }
            final_score = (
                vector_similarity * weights['vector'] +
                word_similarity * weights['word'] +
                string_similarity * weights['string'] +
                structure_similarity * weights['structure']
            )
        else:
            # 軽量モード: ベクトル類似度なし
            weights = {
                'word': 0.5,      # 単語類似度 (50%)
                'string': 0.3,    # 文字列類似度 (30%)
                'structure': 0.2  # 構造類似度 (20%)
            }
            final_score = (
                word_similarity * weights['word'] +
                string_similarity * weights['string'] +
                structure_similarity * weights['structure']
            )

        return {
            'final_score': final_score,
            'vector_similarity': vector_similarity,
            'word_similarity': word_similarity,
            'string_similarity': string_similarity,
            'structure_similarity': structure_similarity,
            'word_details': word_details,
            'translated_clean': trans_clean,
            'reference_clean': ref_clean,
            'weights': weights,
            'ai_mode': self.use_embeddings
        }

    def _clean_english_text(self, text: str) -> str:
        """英文をクリーニング"""
        # 小文字化
        text = text.lower().strip()
        # 余分なスペース除去
        text = re.sub(r'\s+', ' ', text)
        # 句読点を標準化
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def _calculate_word_similarity(self, text1: str, text2: str) -> Tuple[float, Dict]:
        """単語レベルの類似度計算"""
        words1 = set(text1.split())
        words2 = set(text2.split())

        common_words = words1 & words2
        all_words = words1 | words2

        if len(all_words) == 0:
            return 0.0, {}

        jaccard_similarity = len(common_words) / len(all_words)

        # 詳細情報
        details = {
            'translated_words': list(words1),
            'reference_words': list(words2),
            'common_words': list(common_words),
            'missing_words': list(words2 - words1),
            'extra_words': list(words1 - words2)
        }

        return jaccard_similarity, details

    def _calculate_string_similarity(self, text1: str, text2: str) -> float:
        """文字列類似度計算"""
        return SequenceMatcher(None, text1, text2).ratio()

    def _calculate_structure_similarity(self, text1: str, text2: str) -> float:
        """構造類似度計算（文長などの基本的な特徴）"""
        len1, len2 = len(text1.split()), len(text2.split())

        if max(len1, len2) == 0:
            return 1.0

        length_similarity = 1 - abs(len1 - len2) / max(len1, len2)

        return length_similarity

    def score_translation(self, user_japanese: str) -> Dict:
        """日本語入力を評価"""

        if not user_japanese.strip():
            return {
                'score': 0,
                'grade': 'F',
                'feedback': '回答が入力されていません。',
                'details': {}
            }

        # 日本語を英訳（AI翻訳 or モック翻訳）
        translated_english = self.translate_japanese_to_english(user_japanese)

        # 現在の問題の正解英文と比較
        if not self.current_question:
            return {
                'score': 0,
                'grade': 'F',
                'feedback': '問題が選択されていません。',
                'details': {}
            }

        reference_english = self.current_question['english_reference']

        # 英文同士で類似度計算
        similarity_result = self.calculate_english_similarity(translated_english, reference_english)

        # スコア化（0-100）
        score = int(similarity_result['final_score'] * 100)

        # グレード判定
        if score >= 90:
            grade = 'S'
            feedback = '素晴らしい！完璧な翻訳です。'
        elif score >= 80:
            grade = 'A'
            feedback = '非常に良い翻訳です！'
        elif score >= 70:
            grade = 'B'
            feedback = '良い翻訳です。いくつか改善点があります。'
        elif score >= 60:
            grade = 'C'
            feedback = 'まずまずです。もう少し正確に翻訳しましょう。'
        elif score >= 40:
            grade = 'D'
            feedback = '意味は伝わっていますが、改善が必要です。'
        else:
            grade = 'F'
            feedback = '翻訳の精度が低いです。再度チャレンジしましょう。'

        result = {
            'score': score,
            'grade': grade,
            'feedback': feedback,
            'japanese_input': user_japanese,
            'translated_english': translated_english,
            'reference_english': reference_english,
            'similarity_details': similarity_result,
            'question': self.current_question
        }

        self.score_history.append(result)

        return result

    def get_statistics(self) -> Dict:
        """統計情報を取得"""
        if not self.score_history:
            return None

        scores = [result['score'] for result in self.score_history]
        grades = [result['grade'] for result in self.score_history]

        grade_dist = {}
        for grade in grades:
            grade_dist[grade] = grade_dist.get(grade, 0) + 1

        return {
            'total_questions': len(self.score_history),
            'average_score': sum(scores) / len(scores),
            'highest_score': max(scores),
            'lowest_score': min(scores),
            'grade_distribution': grade_dist
        }


if __name__ == "__main__":
    # テスト実行
    system = JapaneseToEnglishSystem()

    print("=" * 60)
    print("🎓 Japanese to English Translation Quiz System")
    print("=" * 60)

    # ランダムな問題を取得
    question = system.get_random_question()
    print(f"\n[QUESTION] {question['japanese']}")
    print(f"[TOPIC] {question['topic']}")
    print(f"[REFERENCE] English: {question['english_reference']}")

    # ユーザー入力をシミュレート
    user_input = question['japanese']  # 完全な正解をテスト

    print(f"\n[YOUR INPUT] Japanese: {user_input}")

    # 採点
    result = system.score_translation(user_input)

    print(f"\n📊 採点結果:")
    print(f"スコア: {result['score']}点")
    print(f"グレード: {result['grade']}")
    print(f"フィードバック: {result['feedback']}")
    print(f"翻訳結果: {result['translated_english']}")
    print(f"正解英文: {result['reference_english']}")