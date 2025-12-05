from celery import Celery
from app.ocr_engine import read_image
import os

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
backend_url = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery = Celery(
    "worker_app",
    broker=broker_url,
    backend=backend_url
)

@celery.task(name="ocr_task")
def perform_ocr_task(image_path: str):
    return read_image(image_path=image_path)
