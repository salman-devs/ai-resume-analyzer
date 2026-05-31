import json
import re
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

_model = None


def _get_model():
    """Lazy-load Gemini model — avoids crashing at startup if key is missing."""
    global _model
    if _model is None:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        _model = genai.GenerativeModel("gemini-1.5-flash")
    return _model


def _fallback(ats_score: int, missing_keywords: list) -> dict:
    top_missing = ", ".join(missing_keywords[:5]) if missing_keywords else "none detected"
    return {
        "overall_assessment": (
            f"AI feedback is temporarily unavailable. "
            f"Your ATS keyword match score is {ats_score}/100."
        ),
        "strengths": [
            "Resume was successfully parsed and analyzed",
            "ATS keyword scan completed",
        ],
        "improvements": [
            "Add missing keywords from the job description",
            "Tailor your experience bullet points to the role",
            "Quantify achievements where possible",
        ],
        "keyword_tips": f"Consider naturally incorporating: {top_missing}.",
        "formatting_tips": (
            "Use standard section headers (Experience, Education, Skills). "
            "Avoid tables, columns, and graphics that confuse ATS parsers."
        ),
        "score_breakdown": {
            "keyword_match": ats_score,
            "estimated_readability": 70,
            "estimated_relevance": min(100, ats_score + 5),
        },
    }


def _parse_json_response(raw: str) -> dict:
    """Strip markdown fences and parse JSON from Gemini response."""
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw.strip())
    return json.loads(raw.strip())


def generate_ai_feedback(
    resume_text: str,
    job_description: str,
    ats_score: int,
    matched_keywords: list,
    missing_keywords: list,
) -> dict:
    """Use Gemini to generate structured resume feedback."""

    prompt = f"""You are an expert ATS consultant and professional resume writer.
Analyze the resume against the job description and respond with ONLY a JSON object — no markdown, no explanation.

RESUME (first 3000 chars):
{resume_text[:3000]}

JOB DESCRIPTION (first 2000 chars):
{job_description[:2000]}

ATS SCORE: {ats_score}/100
MATCHED KEYWORDS: {", ".join(matched_keywords[:20])}
MISSING KEYWORDS: {", ".join(missing_keywords[:20])}

Return exactly this JSON structure:
{{
  "overall_assessment": "<2-3 sentences on overall fit>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "improvements": ["<improvement 1>", "<improvement 2>", "<improvement 3>"],
  "keyword_tips": "<specific advice on incorporating the missing keywords naturally>",
  "formatting_tips": "<brief ATS formatting and structure suggestions>",
  "score_breakdown": {{
    "keyword_match": {ats_score},
    "estimated_readability": <integer 0-100>,
    "estimated_relevance": <integer 0-100>
  }}
}}"""

    try:
        model = _get_model()
        response = model.generate_content(prompt)
        return _parse_json_response(response.text)
    except Exception as exc:
        logger.warning("Gemini AI feedback failed: %s", exc)
        return _fallback(ats_score, missing_keywords)