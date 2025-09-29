"""
Streamlit Japanese to English Translation Quiz
日本語→英訳→英文比較による採点システムのGUI
"""
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from japanese_to_english_system import JapaneseToEnglishSystem

st.set_page_config(
    page_title="Japanese to English Quiz",
    page_icon="🇯🇵→🇺🇸",
    layout="wide"
)

# セッション状態の初期化
if 'quiz_system' not in st.session_state:
    st.session_state.quiz_system = JapaneseToEnglishSystem()
    st.session_state.current_question = None
    st.session_state.user_answer = ""
    st.session_state.result = None
    st.session_state.show_result = False

quiz = st.session_state.quiz_system

st.title("🇯🇵→🇺🇸 Japanese to English Translation Quiz")
st.markdown("**新しいアプローチ**: あなたの日本語を英訳して、正解英文と比較します")

# サイドバー：統計情報
st.sidebar.header("📊 システム情報")
st.sidebar.metric("📚 利用可能な問題数", len(quiz.sample_questions))

stats = quiz.get_statistics()
if stats:
    st.sidebar.divider()
    st.sidebar.header("📈 学習統計")
    st.sidebar.metric("📝 総問題数", stats['total_questions'])
    st.sidebar.metric("⭐ 平均スコア", f"{stats['average_score']:.1f}点")
    st.sidebar.metric("🏆 最高スコア", f"{stats['highest_score']}点")

    if stats['grade_distribution']:
        st.sidebar.write("**グレード分布:**")
        for grade in ['S', 'A', 'B', 'C', 'D', 'F']:
            count = stats['grade_distribution'].get(grade, 0)
            if count > 0:
                st.sidebar.write(f"{grade}: {count}回")

st.sidebar.divider()
if st.sidebar.button("🔄 統計をリセット"):
    st.session_state.quiz_system.score_history = []
    st.rerun()

# メインエリア
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📖 問題")

    if st.session_state.current_question is None or st.button("🎲 新しい問題を出題", type="primary"):
        st.session_state.current_question = quiz.get_random_question()
        st.session_state.user_answer = ""
        st.session_state.result = None
        st.session_state.show_result = False

        if st.session_state.current_question:
            st.rerun()

    if st.session_state.current_question:
        question = st.session_state.current_question

        st.subheader("以下の日本語を正しく翻訳してください:")

        # 正解の英文を表示（参考用）
        with st.expander("💡 正解の英文を見る（参考）", expanded=False):
            st.info(f"**正解**: {question['english_reference']}")
            st.caption(f"📚 トピック: {question['topic']}")

        st.info(question['japanese'])

        st.divider()

        user_answer = st.text_area(
            "✏️ あなたの日本語訳を入力してください:",
            value=st.session_state.user_answer,
            height=150,
            key="answer_input",
            help="元の日本語を自分なりの日本語で表現してください"
        )

        st.session_state.user_answer = user_answer

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("📝 採点する", type="primary", disabled=not user_answer.strip()):
                st.session_state.result = quiz.score_translation(user_answer)
                st.session_state.show_result = True
                st.rerun()

        with col_btn2:
            if st.button("⏭️ スキップ"):
                st.session_state.current_question = quiz.get_random_question()
                st.session_state.user_answer = ""
                st.session_state.result = None
                st.session_state.show_result = False
                st.rerun()

with col2:
    st.header("💡 システムの仕組み")

    if st.session_state.current_question:
        st.write("**採点プロセス:**")
        st.write("1. あなたの日本語を分析")
        st.write("2. 英語に自動翻訳")
        st.write("3. 正解英文と比較")
        st.write("4. 類似度を複数の指標で評価")

        st.divider()

        st.write("**評価指標:**")
        if hasattr(quiz, 'use_embeddings') and quiz.use_embeddings:
            st.write("🧠 **ベクトル類似度 (40%)**: AI による意味的な類似性")
            st.write("🔤 **単語類似度 (30%)**: 使用する英単語の一致度")
            st.write("📊 **文字列類似度 (20%)**: 文字レベルの一致度")
            st.write("📏 **構造類似度 (10%)**: 文の長さや構造の類似性")
        else:
            st.write("🔤 **単語類似度 (50%)**: 使用する英単語の一致度")
            st.write("📊 **文字列類似度 (30%)**: 文字レベルの一致度")
            st.write("📏 **構造類似度 (20%)**: 文の長さや構造の類似性")

        japanese_text = st.session_state.current_question['japanese']
        char_count = len(japanese_text)
        word_count = len(japanese_text.replace('、', ' ').replace('。', ' ').split())

        st.divider()
        st.metric("📏 文字数", char_count)
        st.metric("📏 単語数(推定)", word_count)

# 採点結果の表示
if st.session_state.show_result and st.session_state.result:
    st.divider()

    result = st.session_state.result

    st.header("📊 採点結果")

    col_result1, col_result2, col_result3 = st.columns(3)

    with col_result1:
        st.metric("スコア", f"{result['score']}点")

    with col_result2:
        grade_colors = {
            'S': '🌟',
            'A': '✨',
            'B': '⭐',
            'C': '💫',
            'D': '🔆',
            'F': '💧'
        }
        grade_icon = grade_colors.get(result['grade'], '')
        st.metric("グレード", f"{grade_icon} {result['grade']}")

    with col_result3:
        st.metric("総問題数", len(quiz.score_history))

    # フィードバック表示
    if result['score'] >= 80:
        st.success(result['feedback'])
    elif result['score'] >= 60:
        st.info(result['feedback'])
    else:
        st.warning(result['feedback'])

    # 翻訳結果表示
    col_trans1, col_trans2 = st.columns(2)

    with col_trans1:
        st.write("**あなたの日本語:**")
        st.code(result['japanese_input'], language="text")

        st.write("**自動翻訳結果:**")
        st.code(result['translated_english'], language="text")

    with col_trans2:
        st.write("**元の日本語:**")
        st.code(result['question']['japanese'], language="text")

        st.write("**正解英文:**")
        st.code(result['reference_english'], language="text")

    # 詳細分析
    if 'similarity_details' in result:
        st.divider()
        with st.expander("🔍 詳細分析を見る", expanded=True):
            details = result['similarity_details']

            st.markdown("### 📊 各指標のスコア")

            # ベクトル類似度がある場合は4列、ない場合は3列
            vector_score = details.get('vector_similarity', 0) * 100
            if vector_score > 0:
                col_score1, col_score2, col_score3, col_score4 = st.columns(4)

                with col_score1:
                    st.metric("🧠 ベクトル類似度",
                             f"{vector_score:.1f}%",
                             help="AIによる意味的な類似性（DistilBERT）")
            else:
                col_score1, col_score2, col_score3 = st.columns(3)

            # 他の指標
            word_score = details.get('word_similarity', 0) * 100
            string_score = details.get('string_similarity', 0) * 100
            structure_score = details.get('structure_similarity', 0) * 100

            if vector_score > 0:
                with col_score2:
                    st.metric("🔤 単語類似度",
                             f"{word_score:.1f}%",
                             help="英単語の一致度")
                with col_score3:
                    st.metric("📊 文字列類似度",
                             f"{string_score:.1f}%",
                             help="文字レベルの類似度")
                with col_score4:
                    st.metric("📏 構造類似度",
                             f"{structure_score:.1f}%",
                             help="文の長さや構造の類似性")
            else:
                with col_score1:
                    st.metric("🔤 単語類似度",
                             f"{word_score:.1f}%",
                             help="英単語の一致度")
                with col_score2:
                    st.metric("📊 文字列類似度",
                             f"{string_score:.1f}%",
                             help="文字レベルの類似度")
                with col_score3:
                    st.metric("📏 構造類似度",
                             f"{structure_score:.1f}%",
                             help="文の長さや構造の類似性")

            weights = details.get('weights', {})
            if weights:
                # ベクトル類似度の重みも表示
                weight_text = "⚖️ **重み配分**: "
                weight_parts = []

                if weights.get('vector', 0) > 0:
                    weight_parts.append(f"ベクトル{weights.get('vector', 0)*100:.0f}%")
                weight_parts.append(f"単語{weights.get('word', 0)*100:.0f}%")
                weight_parts.append(f"文字列{weights.get('string', 0)*100:.0f}%")
                weight_parts.append(f"構造{weights.get('structure', 0)*100:.0f}%")

                weight_text += " + ".join(weight_parts)
                st.info(weight_text)

            # 単語分析
            if 'word_details' in details:
                word_details = details['word_details']

                st.divider()
                st.markdown("### 🔤 英単語レベルの分析")

                col_word1, col_word2 = st.columns(2)

                with col_word1:
                    st.write("**あなたの翻訳に含まれる英単語:**")
                    if word_details.get('translated_words'):
                        translated_words = ' | '.join(word_details['translated_words'][:10])
                        st.code(translated_words, language="text")
                    else:
                        st.code("(単語が検出されませんでした)", language="text")

                with col_word2:
                    st.write("**正解英文の単語:**")
                    if word_details.get('reference_words'):
                        ref_words = ' | '.join(word_details['reference_words'][:10])
                        st.code(ref_words, language="text")

                if word_details.get('common_words'):
                    st.success(f"✅ 一致した単語 ({len(word_details['common_words'])}個): {', '.join(word_details['common_words'])}")

                if word_details.get('missing_words'):
                    st.error(f"❌ 不足している単語 ({len(word_details['missing_words'])}個): {', '.join(word_details['missing_words'])}")

                if word_details.get('extra_words'):
                    st.warning(f"➕ 余分な単語 ({len(word_details['extra_words'])}個): {', '.join(word_details['extra_words'])}")

            # 翻訳品質分析
            st.divider()
            st.markdown("### 🔄 翻訳品質分析")

            translated_text = result.get('translated_english', '')
            reference_text = result.get('reference_english', '')
            japanese_input = result.get('japanese_input', '')

            col_analysis1, col_analysis2 = st.columns(2)

            with col_analysis1:
                st.write("**文章の特徴:**")

                # 文章の長さ分析
                jp_chars = len(japanese_input)
                trans_chars = len(translated_text)
                ref_chars = len(reference_text)

                st.write(f"• 入力日本語: {jp_chars}文字")
                st.write(f"• 自動翻訳: {trans_chars}文字")
                st.write(f"• 正解英文: {ref_chars}文字")

                # 単語数分析
                trans_words = len(translated_text.split())
                ref_words = len(reference_text.split())

                st.write(f"• 翻訳単語数: {trans_words}語")
                st.write(f"• 正解単語数: {ref_words}語")

            with col_analysis2:
                st.write("**スコア構成要素:**")

                # 各指標の貢献度を計算
                final_score = result.get('score', 0)
                if weights:
                    if vector_score > 0:
                        vector_contribution = (vector_score/100) * weights.get('vector', 0) * 100
                        st.write(f"• ベクトル寄与: {vector_contribution:.1f}点")

                    word_contribution = (word_score/100) * weights.get('word', 0) * 100
                    string_contribution = (string_score/100) * weights.get('string', 0) * 100
                    structure_contribution = (structure_score/100) * weights.get('structure', 0) * 100

                    st.write(f"• 単語類似寄与: {word_contribution:.1f}点")
                    st.write(f"• 文字列寄与: {string_contribution:.1f}点")
                    st.write(f"• 構造類似寄与: {structure_contribution:.1f}点")

            # 改善提案
            st.divider()
            st.markdown("### 💡 改善提案")

            suggestions = []
            if word_score < 70:
                suggestions.append("🔤 **単語選択**: より正確な英単語を使用しましょう")
            if string_score < 60:
                suggestions.append("📊 **表現力**: 文章の表現をより自然にしましょう")
            if structure_score < 50:
                suggestions.append("📏 **文構造**: 文の長さや構造を調整しましょう")
            if vector_score > 0 and vector_score < 80:
                suggestions.append("🧠 **意味理解**: 文章の意味をより正確に表現しましょう")

            if suggestions:
                for suggestion in suggestions:
                    st.write(suggestion)
            else:
                st.success("🎉 素晴らしい翻訳です！すべての指標で高いスコアを獲得しています。")

            st.divider()
            st.info("💡 **採点の仕組み**: あなたの日本語をGoogle翻訳で英訳し、正解の英文と比較しています。翻訳エンジンの精度により結果が変わる場合があります。")

st.divider()

# 学習履歴
with st.expander("📚 学習履歴"):
    if quiz.score_history:
        st.write(f"**全{len(quiz.score_history)}問の結果:**")

        for i, record in enumerate(reversed(quiz.score_history[-10:]), 1):
            col_hist1, col_hist2, col_hist3, col_hist4 = st.columns([3, 1, 1, 1])

            with col_hist1:
                preview = record['japanese_input'][:40] + "..." if len(record['japanese_input']) > 40 else record['japanese_input']
                st.write(f"{i}. {preview}")

            with col_hist2:
                st.write(f"グレード: {record['grade']}")

            with col_hist3:
                st.write(f"{record['score']}点")

            with col_hist4:
                st.write(f"トピック: {record['question']['topic']}")

        if len(quiz.score_history) > 10:
            st.caption(f"... 他 {len(quiz.score_history) - 10}問")
    else:
        st.info("まだ問題に挑戦していません。")

st.markdown("---")
st.markdown("🇯🇵→🇺🇸 **Japanese to English Translation Quiz System** - 新しいアプローチの英語学習ツール")