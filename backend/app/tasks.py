import logging
from app.worker import celery_app
from app.services.ai_service import generate_ai_feedback

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def run_ai_feedback(
    self,
    resume_text: str,
    job_description: str,
    ats_score: int,
    matched_keywords: list,
    missing_keywords: list,
) -> dict:
    try:
        return generate_ai_feedback(
            resume_text,
            job_description,
            ats_score,
            matched_keywords,
            missing_keywords,
        )
    except Exception as exc:
        logger.error("AI feedback task failed: %s", exc)
        raise self.retry(exc=exc, countdown=5)