"""
Google翻訳APIのテストスクリプト
"""

def test_google_translate():
    print("Testing Google Translate API...")

    try:
        from googletrans import Translator
        translator = Translator()

        # テスト文章
        test_sentences = [
            "売上を伸ばすには新しい戦略が必要です。",
            "今日は良い天気です。",
            "人工知能は私たちの生活を変えています。"
        ]

        for japanese in test_sentences:
            print(f"\n日本語: {japanese}")
            try:
                result = translator.translate(japanese, src='ja', dest='en')
                print(f"英訳: {result.text}")
            except Exception as e:
                print(f"エラー: {e}")

    except ImportError as e:
        print(f"googletrans not installed: {e}")
        print("\nInstalling googletrans...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'googletrans==4.0.0rc1'])
        print("Please run this script again after installation.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_google_translate()