import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class CeleryConfig:
    """
    Celery configuration for Flask app.
    Uses Redis as both broker and result backend.
    """

    # Redis URL (can be Docker or local)
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
    # Celery settings
    CELERY_BROKER_URL = f"{REDIS_URL}/0"
    CELERY_RESULT_BACKEND = f"{REDIS_URL}/0"
    # Ignore storing results (optional)
    CELERY_TASK_IGNORE_RESULT = True
