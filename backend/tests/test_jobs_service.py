from app.services.jobs_service import (
    extract_job_title,
    is_fresher_resume,
    is_senior_job,
)


def test_extract_full_stack_title():
    resume = "I am a full stack developer with Python and React experience"
    assert extract_job_title(resume) == "full stack developer"


def test_extract_python_title():
    resume = "Backend developer with FastAPI and Django experience"
    title = extract_job_title(resume)
    assert "python" in title or "backend" in title or "developer" in title


def test_extract_default_title():
    resume = "I have some general programming skills"
    assert extract_job_title(resume) == "software developer"


def test_is_fresher_resume_true():
    resume = "I am a fresher looking for entry level opportunities"
    assert is_fresher_resume(resume) is True


def test_is_fresher_no_experience_mentioned():
    resume = "Python React FastAPI skills projects built during college"
    assert is_fresher_resume(resume) is True


def test_is_senior_job_true():
    jd = "We are looking for a senior developer with 5+ years of experience"
    assert is_senior_job("Senior Python Developer", jd) is True


def test_is_senior_job_false():
    jd = "We are looking for a junior developer to join our team"
    assert is_senior_job("Junior Python Developer", jd) is False