import re
from typing import Set


STOP_WORDS: Set[str] = {
    "and", "or", "the", "a", "an", "in", "on", "at", "to", "for",
    "of", "with", "is", "are", "was", "were", "be", "been", "have",
    "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "this", "that", "these", "those",
    "we", "you", "he", "she", "it", "they", "i", "my", "your", "our",
    "as", "by", "from", "up", "about", "into", "through", "during",
    "also", "than", "then", "so", "if", "but", "not", "no", "more",
    "all", "any", "both", "each", "few", "most", "other", "some",
    "such", "nor", "only", "own", "same", "too", "very", "just",
    "its", "their", "them", "who", "which", "how", "when", "where",
    "there", "here", "new", "get", "use", "work", "make", "good",
    "well", "own", "must", "need", "want", "like", "know", "look",
    "time", "year", "way", "day", "man", "us", "one", "out", "per",
}

BIGRAM_PATTERNS = [
    r"machine learning", r"deep learning", r"natural language",
    r"computer vision", r"data science", r"data analysis",
    r"software engineering", r"product management", r"project management",
    r"cloud computing", r"ci/cd", r"rest api", r"restful api",
    r"unit test", r"test driven", r"agile methodology", r"scrum master",
    r"version control", r"object oriented", r"microservices architecture",
    r"full stack", r"front end", r"back end", r"open source",
]


def extract_keywords(text: str) -> Set[str]:
    """
    Extract meaningful keywords from text.
    Captures important bigrams first, then filters single-word tokens.
    """
    text_lower = text.lower()
    found: Set[str] = set()

    # 1. extract known bigrams
    for pattern in BIGRAM_PATTERNS:
        if re.search(pattern, text_lower):
            found.add(pattern.replace(r"\/", "/"))

    # 2. clean and tokenize
    cleaned = re.sub(r"[^a-z0-9\+\#\.\s]", " ", text_lower)
    words = cleaned.split()

    # 3. keep meaningful tokens: length > 2, not a stop word
    for word in words:
        word = word.strip(".")
        if len(word) > 2 and word not in STOP_WORDS:
            found.add(word)

    return found


def calculate_ats_score(resume_text: str, job_description: str) -> dict:
    """
    Compare resume against job description.
    Returns ATS score (0-100), matched keywords, and missing keywords.
    """
    if not resume_text or not job_description:
        raise ValueError("Resume text and job description cannot be empty.")

    jd_keywords = extract_keywords(job_description)
    resume_keywords = extract_keywords(resume_text)

    matched = jd_keywords & resume_keywords
    missing = jd_keywords - resume_keywords

    score = round((len(matched) / len(jd_keywords)) * 100) if jd_keywords else 0
    score = min(score, 100)

    return {
        "ats_score": score,
        "matched_keywords": sorted(matched),
        "missing_keywords": sorted(missing),
        "total_jd_keywords": len(jd_keywords),
        "total_matched": len(matched),
    }