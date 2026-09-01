import logging
import numpy as np

logger = logging.getLogger(__name__)

_model = None


def _get_model():
    """Lazy-load the embedding model — avoids slow import at app startup."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_embedding(text: str) -> np.ndarray:
    """
    Convert text into a 384-dimensional embedding vector.
    """
    model = _get_model()
    return model.encode(text, convert_to_numpy=True)


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """
    Cosine similarity between two vectors, scaled to 0-100.
    1.0 (identical meaning) -> 100, 0 (unrelated) -> 50, -1 (opposite) -> 0.
    """
    dot = np.dot(vec_a, vec_b)
    norm = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if norm == 0:
        return 0.0
    similarity = dot / norm
    return round(float((similarity + 1) / 2) * 100, 2)


def semantic_similarity(text_a: str, text_b: str) -> float:
    """
    Convenience function: embed both texts and return their similarity score (0-100).
    """
    vec_a = get_embedding(text_a)
    vec_b = get_embedding(text_b)
    return cosine_similarity(vec_a, vec_b)