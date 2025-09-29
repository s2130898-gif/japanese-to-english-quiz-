"""
English Text Embeddings using DistilBERT
英文専用のベクトル埋め込みモデル
"""
import numpy as np
from typing import List
import torch
from transformers import AutoTokenizer, AutoModel

class EnglishEmbeddings:
    """英文専用のDistilBERT埋め込みモデル"""

    def __init__(self):
        print("[LOADING] English AI embedding model loading...")
        print("[INFO] First launch takes 3-4 minutes...")

        # 英語専用のDistilBERT
        model_name = 'distilbert-base-uncased'

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

        self.model.eval()
        self.dimension = 768

        print("[SUCCESS] DistilBERT English model (768 dimensions) loaded")
        print("[INFO] AI vector similarity calculation enabled for English text")

    def encode(self, texts: List[str]) -> np.ndarray:
        """複数の英文をベクトル化"""
        embeddings = []

        with torch.no_grad():
            for text in texts:
                inputs = self.tokenizer(
                    text,
                    return_tensors='pt',
                    truncation=True,
                    max_length=512,
                    padding=True
                )

                outputs = self.model(**inputs)
                # 平均プーリングを使用（より良い表現）
                token_embeddings = outputs.last_hidden_state
                input_mask_expanded = inputs['attention_mask'].unsqueeze(-1).expand(token_embeddings.size()).float()
                # マスクされたトークンを除外して平均を計算
                sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
                sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
                embedding = (sum_embeddings / sum_mask).squeeze().numpy()
                embeddings.append(embedding)

        return np.array(embeddings)

    def encode_single(self, text: str) -> List[float]:
        """単一の英文をベクトル化"""
        return self.encode([text])[0].tolist()

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """2つの英文間のコサイン類似度を計算"""
        vec1 = self.encode([text1])[0]
        vec2 = self.encode([text2])[0]

        # コサイン類似度
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = dot_product / (norm1 * norm2)
        return float(similarity)