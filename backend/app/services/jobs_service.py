import httpx
import logging
import re
from app.core.config import settings
from app.services.ats_service import calculate_ats_score

logger = logging.getLogger(__name__)

ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs"

SENIOR_PATTERNS = [
    r"\b(\d+)\+?\s*years?\s*(of\s*)?(experience|exp)\b",
    r"\bsenior\b", r"\bsr\.\b", r"\blead\b", r"\bprincipal\b",
    r"\bstaff engineer\b", r"\bhead of\b", r"\bdirector\b",
    r"\b5\+\s*years\b", r"\b6\+\s*years\b", r"\b7\+\s*years\b",
    r"\b8\+\s*years\b", r"\b10\+\s*years\b",
]

FRESHER_SIGNALS = [
    "fresher", "fresh graduate", "entry level", "entry-level",
    "0-1 year", "0 year", "no experience", "recent graduate",
    "junior", "trainee", "intern", "graduate",
]


def is_fresher_resume(resume_text: str) -> bool:
    resume_lower = resume_text.lower()
    return any(signal in resume_lower for signal in FRESHER_SIGNALS)


def is_senior_job(job_description: str) -> bool:
    desc_lower = job_description.lower()
    for pattern in SENIOR_PATTERNS:
        match = re.search(pattern, desc_lower)
        if match:
            if pattern.startswith(r"\b(\d+)"):
                years = int(match.group(1))
                if years >= 3:
                    return True
            else:
                return True
    return False


def extract_job_title(resume_text: str) -> str:
    titles = [
        "python developer", "backend developer", "frontend developer",
        "full stack developer", "software engineer", "data scientist",
        "data analyst", "machine learning engineer", "devops engineer",
        "react developer", "node developer", "java developer",
        "mobile developer", "android developer", "ios developer",
        "cloud engineer", "web developer", "software developer",
    ]
    resume_lower = resume_text.lower()
    for title in titles:
        if title in resume_lower:
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
    scored_jobs = []

    for job in jobs:
        description = job.get("description", "")
        title_text = job.get("title", "")
        company = job.get("company", {}).get("display_name", "Unknown")
        location_text = job.get("location", {}).get("display_name", "Unknown")
        redirect_url = job.get("redirect_url", "")
        created = job.get("created", "")

        if not description:
            continue

        score_result = calculate_ats_score(resume_text, description)
        match_score = score_result["ats_score"]

        # penalize senior jobs for fresher resumes
        if fresher and is_senior_job(description):
            match_score = max(0, match_score - 30)

        scored_jobs.append({
            "title": title_text,
            "company": company,
            "location": location_text,
            "description": description[:300] + "..." if len(description) > 300 else description,
            "match_score": match_score,
            "redirect_url": redirect_url,
            "created": created,
        })

    scored_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    return scored_jobs