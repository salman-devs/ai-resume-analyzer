import re
from typing import List

def extract_keywords(text: str) -> List[str]:
    """Extract meaningful keywords from text."""
    text = text.lower()
    # remove special characters
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    words = text.split()
    # filter out common stop words
    stop_words = {
        'and', 'or', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
        'we', 'you', 'he', 'she', 'it', 'they', 'i', 'my', 'your', 'our',
        'as', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'also', 'than', 'then', 'so', 'if', 'but', 'not', 'no', 'more'
    }
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    return list(set(keywords))

def calculate_ats_score(resume_text: str, job_description: str) -> dict:
    """
    Compare resume against job description.
    Returns score, matched keywords, and missing keywords.
    """
    if not resume_text or not job_description:
        raise ValueError("Resume text and job description cannot be empty.")

    jd_keywords = set(extract_keywords(job_description))
    resume_keywords = set(extract_keywords(resume_text))

    matched = jd_keywords.intersection(resume_keywords)
    missing = jd_keywords.difference(resume_keywords)

    score = round((len(matched) / len(jd_keywords)) * 100) if jd_keywords else 0

    return {
        "ats_score": score,
        "matched_keywords": sorted(list(matched)),
        "missing_keywords": sorted(list(missing)),
        "total_jd_keywords": len(jd_keywords),
        "total_matched": len(matched),
    }