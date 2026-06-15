import httpx
import logging
import re
from app.core.config import settings
from app.services.ats_service import calculate_ats_score

logger = logging.getLogger(__name__)

ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs"

SENIOR_PATTERNS = [
    r"\b([4-9]|\d{2,})\+?\s*years?\s*(of\s*)?(experience|exp)\b",
    r"\bsenior\b", r"\bsr\.\b", r"\blead\b", r"\bprincipal\b",
    r"\bstaff engineer\b", r"\bhead of\b", r"\bdirector\b",
]

FRESHER_SIGNALS = [
    "fresher", "fresh graduate", "entry level", "entry-level",
    "0-1 year", "0 year", "no experience", "recent graduate",
    "junior", "trainee", "intern", "graduate", "beginner",
]


def is_fresher_resume(resume_text: str) -> bool:
    resume_lower = resume_text.lower()
    # check explicit fresher signals
    if any(signal in resume_lower for signal in FRESHER_SIGNALS):
        return True
    # if resume mentions very few years of experience, treat as fresher
    matches = re.findall(r'(\d+)\+?\s*years?\s*(of\s*)?(experience|exp)', resume_lower)
    if matches:
        years = [int(m[0]) for m in matches]
        if max(years) <= 2:
            return True
        return False
    # no experience mentioned at all — likely fresher
    return True


def is_senior_job(job_title: str, job_description: str) -> bool:
    text = (job_title + " " + job_description).lower()
    for pattern in SENIOR_PATTERNS:
        if re.search(pattern, text):
            return True
    return False


def extract_job_title(resume_text: str) -> str:
    resume_lower = resume_text.lower()

    # priority order — more specific titles first
    priority_titles = [
        ("full stack developer", ["full stack", "fullstack", "full-stack"]),
        ("python full stack developer", ["python full stack", "python fullstack"]),
        ("react developer", ["react.js", "reactjs", "react developer"]),
        ("data scientist", ["data science", "data scientist", "machine learning"]),
        ("machine learning engineer", ["machine learning", "deep learning", "ml engineer"]),
        ("devops engineer", ["devops", "ci/cd", "kubernetes", "docker"]),
        ("data analyst", ["data analyst", "data analysis", "tableau", "power bi"]),
        ("android developer", ["android", "kotlin"]),
        ("ios developer", ["ios", "swift", "xcode"]),
        ("backend developer", ["backend", "back-end", "back end", "api developer"]),
        ("frontend developer", ["frontend", "front-end", "front end", "ui developer"]),
        ("python developer", ["django", "flask", "fastapi"]),
        ("java developer", ["java", "spring boot", "hibernate"]),
        ("node developer", ["node.js", "nodejs", "express.js"]),
        ("software engineer", ["software engineer", "software developer"]),
        ("web developer", ["web development", "web developer"]),
    ]

    for title, signals in priority_titles:
        if any(signal in resume_lower for signal in signals):
            return title

    return "software developer"


async def fetch_and_score_jobs(
    resume_text: str,
    title: str,
    location: str = "india",
    results_per_page: int = 20,
) -> list:
    params = {
        "app_id": settings.ADZUNA_APP_ID,
        "app_key": settings.ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": title,
        "where": location,
        "content-type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                f"{ADZUNA_BASE_URL}/in/search/1",
                params=params,
            )
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError as e:
        logger.error("Adzuna API error: %s", e)
        return []

    jobs = data.get("results", [])
    fresher = is_fresher_resume(resume_text)
    logger.info("Resume detected as: %s", "fresher" if fresher else "experienced")

    scored_jobs = []

    for job in jobs:
        description = job.get("description", "")
        job_title = job.get("title", "")
        company = job.get("company", {}).get("display_name", "Unknown")
        location_text = job.get("location", {}).get("display_name", "Unknown")
        redirect_url = job.get("redirect_url", "")
        created = job.get("created", "")

        if not description:
            continue

        score_result = calculate_ats_score(resume_text, description)
        match_score = score_result["ats_score"]

        # penalize senior jobs for fresher resumes
        if fresher and is_senior_job(job_title, description):
            match_score = max(0, match_score - 40)

        # skip jobs below 20% after penalty
        if match_score < 20:
            continue

        scored_jobs.append({
            "title": job_title,
            "company": company,
            "location": location_text,
            "description": description[:300] + "..." if len(description) > 300 else description,
            "match_score": match_score,
            "redirect_url": redirect_url,
            "created": created,
        })

    scored_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    return scored_jobs