from typing import List

import math

import numpy as np


def generate_embeddings(text_chunks: List[str]) -> List[List[float]]:
    """Produce deterministic embeddings without relying on a remote model download."""
    embeddings = []
    for chunk in text_chunks:
        tokens = chunk.lower().split()
        vector = np.zeros(64, dtype="float32")
        for index, token in enumerate(tokens[:64]):
            token_hash = sum(ord(char) for char in token)
            vector[index % 64] += float(token_hash % 17 + len(token))
        if tokens:
            vector = vector / max(1, len(tokens))
        embeddings.append(vector.tolist())
    return embeddings
