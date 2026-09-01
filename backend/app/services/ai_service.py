import json
import re
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

_client = None


def _get_client():
    """Lazy-load Gemini client — avoids crashing at startup if key is missing."""
    global _client
    if _client is None:
        from google import genai
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


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
        client = _get_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return _parse_json_response(response.candidates[0].content.parts[0].text)
    except Exception as exc:
        logger.warning("Gemini AI feedback failed: %s", exc)
        return _fallback(ats_score, missing_keywords)


def generate_interview_questions(parsed_resume: dict, job_description: str) -> list:
    """Use Gemini to generate interview questions based on structured resume data and the job description."""

    prompt = f"""You are an experienced technical interviewer.
Generate 5 interview questions for this candidate based ONLY on their actual background below and the job description.
Do NOT invent skills, companies, or experience not listed.
Respond with ONLY a JSON array of strings — no markdown, no explanation.

CANDIDATE SKILLS: {", ".join(parsed_resume.get("skills", []))}
CANDIDATE EXPERIENCE: {json.dumps(parsed_resume.get("experience", []))}
CANDIDATE PROJECTS: {json.dumps(parsed_resume.get("projects", []))}

JOB DESCRIPTION (first 1500 chars):
{job_description[:1500]}

Return exactly this JSON structure:
["<question 1>", "<question 2>", "<question 3>", "<question 4>", "<question 5>"]"""

    try:
        client = _get_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        questions = _parse_json_response(response.candidates[0].content.parts[0].text)
        if not isinstance(questions, list):
            raise ValueError("Expected a JSON array")
        return questions
    except Exception as exc:
        logger.warning("Interview question generation failed: %s", exc)
        return []