"""
直接翻訳テスト
"""
def test_direct_translation():
    print("=== 直接Google翻訳テスト ===")

    try:
        from googletrans import Translator
        translator = Translator()

        # テスト文章
        test_text = "この英文と同じ意味になる日本語を入力してください"
        print(f"入力: {test_text}")

        # 翻訳実行
        result = translator.translate(test_text, src='ja', dest='en')
        print(f"翻訳結果: {result.text}")
        print(f"信頼度: {result.confidence if hasattr(result, 'confidence') else 'N/A'}")
        print(f"検出言語: {result.src}")

        # 別のテスト
        test_text2 = "彼女は毎朝公園でジョギングをしています。"
        print(f"\n入力: {test_text2}")
        result2 = translator.translate(test_text2, src='ja', dest='en')
        print(f"翻訳結果: {result2.text}")

    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_translation()