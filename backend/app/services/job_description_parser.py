import json
import re
import logging
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.job_data import ParsedJobDescription

logger = logging.getLogger(__name__)

_client = None


def _get_client():
    """Lazy-load Gemini client — mirrors ai_service.py's pattern."""
    global _client
    if _client is None:
        from google import genai
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def _parse_json_response(raw: str) -> dict:
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw.strip())
    return json.loads(raw.strip())


PARSE_PROMPT = """You are a job description parsing engine. Extract structured information from the job description text below.

Rules:
- Only extract information that is EXPLICITLY present in the text.
- Do NOT invent, infer, or guess any skills, requirements, or qualifications not stated.
- Distinguish "required" skills (must-have, explicitly stated as required/must have) from "preferred" skills (nice-to-have, explicitly stated as preferred/bonus/plus).
- Respond with ONLY a JSON object — no markdown, no explanation.

JOB DESCRIPTION TEXT:
{job_description}

Return exactly this JSON structure:
{{
  "job_title": "<string or null>",
  "company": "<string or null>",
  "required_skills": ["<skill1>", "<skill2>"],
  "preferred_skills": ["<skill1>"],
  "responsibilities": ["<responsibility1>"],
  "qualifications": ["<qualification1>"],
  "min_experience_years": <integer or null>
}}"""


def parse_job_description(job_description: str) -> ParsedJobDescription:
    """
    Extract structured job description data via Gemini, validated against ParsedJobDescription.
    Raises ValueError if Gemini is unavailable or returns invalid data.
    """
    prompt = PARSE_PROMPT.format(job_description=job_description[:4000])

    try:
        client = _get_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        raw_json = _parse_json_response(response.candidates[0].content.parts[0].text)
        return ParsedJobDescription(**raw_json)
    except ValidationError as exc:
        logger.error("Job description parse validation failed: %s", exc)
        raise ValueError(f"Job description parsing returned invalid structure: {exc}")
    except Exception as exc:
        logger.error("Job description parsing failed: %s", exc)
        raise ValueError(f"Could not parse job description: {exc}")