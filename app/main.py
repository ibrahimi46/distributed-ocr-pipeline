from fastapi import FastAPI, UploadFile, File
from app.celery_worker import perform_ocr_task
from celery.result import AsyncResult
import uuid
import os
import shutil

UPLOAD_DIR = "uploads"

app = FastAPI(title="Image OCR")

@app.post("/ocr")
def process_ocr(file: UploadFile = File(...)):
    file_extension = file.filename.split(".")[-1]
    new_file_name = f"{uuid.uuid4()}.{file_extension}"
    save_path = os.path.join(UPLOAD_DIR, new_file_name)

    # create the upload dir if not exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # open the save path and copy the file to it
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    task = perform_ocr_task.delay(save_path)

    return {"filename" : new_file_name, "task_id": task.id}

@app.post("/result/{task_id}")
def task_result(task_id: str):
    result = AsyncResult(id=task_id)
    return {"task_id" : task_id, "task_state": result.state, "task_result" : result.result}