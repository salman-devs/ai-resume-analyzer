import json
import re
import logging
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.resume_data import ParsedResume

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


PARSE_PROMPT = """You are a resume parsing engine. Extract structured information from the resume text below.

Rules:
- Only extract information that is EXPLICITLY present in the text.
- Do NOT invent, infer, or guess any skills, dates, companies, or qualifications not stated.
- If a field is not present, omit it or leave it empty — do not fabricate a value.
- Respond with ONLY a JSON object — no markdown, no explanation.

RESUME TEXT:
{resume_text}

Return exactly this JSON structure:
{{
  "full_name": "<string or null>",
  "email": "<string or null>",
  "phone": "<string or null>",
  "skills": ["<skill1>", "<skill2>"],
  "education": [
    {{"institution": "<string>", "degree": "<string or null>", "field_of_study": "<string or null>", "start_date": "<string or null>", "end_date": "<string or null>"}}
  ],
  "experience": [
    {{"company": "<string>", "title": "<string>", "start_date": "<string or null>", "end_date": "<string or null>", "description": "<string or null>"}}
  ],
  "projects": [
    {{"name": "<string>", "description": "<string or null>", "technologies": ["<tech1>"]}}
  ],
  "certifications": [
    {{"name": "<string>", "issuer": "<string or null>", "date": "<string or null>"}}
  ]
}}"""


def parse_resume(resume_text: str) -> ParsedResume:
    """
    Extract structured resume data via Gemini, validated against ParsedResume.
    Raises ValueError if Gemini is unavailable or returns invalid data.
    """
    prompt = PARSE_PROMPT.format(resume_text=resume_text[:6000])

    try:
        client = _get_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        raw_json = _parse_json_response(response.candidates[0].content.parts[0].text)
        return ParsedResume(**raw_json)
    except ValidationError as exc:
        logger.error("Resume parse validation failed: %s", exc)
        raise ValueError(f"Resume parsing returned invalid structure: {exc}")
    except Exception as exc:
        logger.error("Resume parsing failed: %s", exc)
        raise ValueError(f"Could not parse resume: {exc}")