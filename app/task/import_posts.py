import csv
import json
import os

import redis
from celery import shared_task
from sqlalchemy.exc import IntegrityError

from app import app
from app.extension import db
from app.models import Post
from config.celery import CeleryConfig

r = redis.Redis.from_url(f"{CeleryConfig.REDIS_URL}/1")


@shared_task(
    bind=True,
    autoretry_for=(ConnectionError,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def import_posts_from_csv(self, file_path):
    """
    Import posts from a CSV into the database and track progress in Redis.

    Args:
        file_path (str): Path to the CSV file.

    Redis keys:
        csv_progress:<task_id> - import progress (0-100)
        csv_status:<task_id>   - "PENDING", "SUCCESS", or "FAILURE"
        csv_errors:<task_id>   - list of row errors if any
    """
    batch_size = 100
    task_id = self.request.id
    errors = []

    if not os.path.exists(file_path):
        r.set(f"csv_status:{task_id}", "FAILURE")
        r.set(f"csv_error:{task_id}", "File not found")
        return

    with app.app_context():
        try:
            with open(file_path, newline="", encoding="utf-8") as f:
                reader = list(csv.DictReader(f))
                total = len(reader)

                if total == 0:
                    raise ValueError("CSV is empty")

                for idx, row in enumerate(reader, 1):
                    try:
                        db.session.add(
                            Post(
                                title=row["title"],
                                description=row.get("description"),
                                status=int(row.get("status", 1)),
                                create_user_id=1,
                                updated_user_id=1,
                            )
                        )

                        if idx % batch_size == 0:
                            db.session.commit()

                    except IntegrityError:
                        db.session.rollback()
                        errors.append({"row": idx, "error": "duplicate title"})
                        continue

                    progress = int((idx / total) * 100)
                    r.set(f"csv_progress:{task_id}", progress)

                db.session.commit()

            if errors:
                r.set(f"csv_errors:{task_id}", json.dumps(errors))
                r.set(f"csv_status:{task_id}", "FAILURE")
            else:
                r.set(f"csv_status:{task_id}", "SUCCESS")

                r.set(f"csv_progress:{task_id}", 100)

        except Exception as e:
            db.session.rollback()
            r.set(f"csv_status:{task_id}", "FAILURE")
            r.set(f"csv_errors:{task_id}", json.dumps([{"error": str(e)}]))

            raise
