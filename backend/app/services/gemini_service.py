import httpx
import json
from app.core.config import settings

def get_ai_feedback(resume_text: str, job_description: str, ats_score: int) -> dict:
    prompt = f"""
You are an expert ATS and career coach.
Analyze this resume against the job description.
ATS Score: {ats_score}%

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Respond ONLY with valid JSON:
{{
    "overall_assessment": "2-3 sentence summary",
    "strengths": ["strength 1", "strength 2", "strength 3"],
    "weaknesses": ["weakness 1", "weakness 2"],
    "improvements": ["improvement 1", "improvement 2", "improvement 3"],
    "missing_skills": ["skill 1", "skill 2"],
    "verdict": "Strong Match or Good Match or Partial Match or Weak Match"
}}
"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = httpx.post(url, json=payload, timeout=30)
        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"].strip()

        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()

        return json.loads(text)

    except Exception as e:
        return {
            "overall_assessment": "AI feedback unavailable at this time.",
            "strengths": [],
            "weaknesses": [],
            "improvements": [],
            "missing_skills": [],
            "verdict": "Unknown",
            "error": str(e)
        }