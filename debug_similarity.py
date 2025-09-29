"""
ベクトル類似度の動作をデバッグするテスト
"""
try:
    from english_embeddings import EnglishEmbeddings

    # エンベディングモデルを初期化
    embeddings = EnglishEmbeddings()

    # テスト文章
    text1 = "good morning"
    text2 = "It is important to improve customer satisfaction."

    print(f"Text 1: {text1}")
    print(f"Text 2: {text2}")

    # ベクトル化
    vec1 = embeddings.encode([text1])[0]
    vec2 = embeddings.encode([text2])[0]

    print(f"\nVector 1 shape: {vec1.shape}")
    print(f"Vector 1 norm: {(vec1**2).sum()**0.5}")
    print(f"Vector 2 shape: {vec2.shape}")
    print(f"Vector 2 norm: {(vec2**2).sum()**0.5}")

    # 類似度計算
    similarity = embeddings.calculate_similarity(text1, text2)
    print(f"\nCalculated similarity: {similarity:.4f} ({similarity*100:.1f}%)")

    # 手動計算で確認
    import numpy as np
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    manual_similarity = dot_product / (norm1 * norm2)

    print(f"Manual calculation: {manual_similarity:.4f} ({manual_similarity*100:.1f}%)")

    # 他の例でテスト
    print("\n" + "="*50)
    print("Additional tests:")

    test_pairs = [
        ("hello", "hi"),
        ("good morning", "good evening"),
        ("I love cats", "I love dogs"),
        ("machine learning", "artificial intelligence"),
        ("the weather is nice", "it's a beautiful day")
    ]

    for t1, t2 in test_pairs:
        sim = embeddings.calculate_similarity(t1, t2)
        print(f"{t1:25} vs {t2:25} = {sim:.4f} ({sim*100:.1f}%)")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()