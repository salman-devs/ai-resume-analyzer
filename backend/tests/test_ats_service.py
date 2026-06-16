from app.services.ats_service import calculate_ats_score


def test_score_is_between_0_and_100():
    resume = "Python developer with FastAPI and PostgreSQL experience"
    jd = "Looking for Python developer with FastAPI skills"
    result = calculate_ats_score(resume, jd)
    assert 0 <= result["ats_score"] <= 100


def test_matched_keywords_detected():
    resume = "Experienced Python developer with FastAPI and React skills"
    jd = "Python FastAPI React developer needed"
    result = calculate_ats_score(resume, jd)
    assert len(result["matched_keywords"]) > 0
    assert "python" in [k.lower() for k in result["matched_keywords"]]


def test_missing_keywords_detected():
    resume = "Python developer with basic skills"
    jd = "Python developer with Docker Kubernetes AWS experience"
    result = calculate_ats_score(resume, jd)
    assert len(result["missing_keywords"]) > 0

def test_empty_resume_raises_error():
    import pytest
    with pytest.raises(ValueError):
        calculate_ats_score("", "Python developer needed")

def test_perfect_match_high_score():
    text = "Python FastAPI PostgreSQL Docker React JWT authentication REST API"
    result = calculate_ats_score(text, text)
    assert result["ats_score"] >= 80