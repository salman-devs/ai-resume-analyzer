from app.services.ats_service import calculate_ats_score
from app.services.embedding_service import semantic_similarity

KEYWORD_WEIGHT = 0.6
SEMANTIC_WEIGHT = 0.4


def calculate_hybrid_match(resume_text: str, job_description: str) -> dict:
    """
    Combine keyword-based ATS score with semantic similarity into
    one explainable hybrid Job Match Score.
    """
    keyword_result = calculate_ats_score(resume_text, job_description)
    keyword_score = keyword_result["ats_score"]

    semantic_score = semantic_similarity(resume_text, job_description)

    hybrid_score = round(
        (keyword_score * KEYWORD_WEIGHT) + (semantic_score * SEMANTIC_WEIGHT)
    )
    hybrid_score = min(hybrid_score, 100)

    return {
        "hybrid_score": hybrid_score,
        "keyword_score": keyword_score,
        "semantic_score": semantic_score,
        "keyword_weight": KEYWORD_WEIGHT,
        "semantic_weight": SEMANTIC_WEIGHT,
        "matched_keywords": keyword_result["matched_keywords"],
        "missing_keywords": keyword_result["missing_keywords"],
    }