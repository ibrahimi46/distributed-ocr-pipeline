# Distributed OCR Pipeline

An asynchronous Optical Character Recognition (OCR) API built with **FastAPI**, **Celery**, and **Redis**. This project demonstrates a distributed architecture pattern, offloading CPU-intensive image processing tasks to background workers to ensure the API remains non-blocking and responsive.

## 🚀 Features

- **Asynchronous Processing:** Uses a producer-consumer pattern to handle heavy OCR tasks without blocking the main thread.
- **Containerized Environment:** Fully isolated services (API, Worker, Broker) orchestrated via **Docker Compose**.
- **Smart Preprocessing:** Includes an image processing pipeline using **Pillow (PIL)** to apply grayscale conversion and binary thresholding for improved OCR accuracy.
- **Confidence Scoring:** Custom logic to calculate the "Health Score" of a document by analyzing confidence levels of individual words (filtering out noise and empty blocks).
- **Structured Output:** Returns clean JSON responses with parsed text and metadata, not just raw strings.

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, FastAPI
- **Task Queue:** Celery
- **Message Broker & Result Store:** Redis
- **OCR Engine:** Tesseract (via `pytesseract`)
- **Image Processing:** Pillow (PIL)
- **Infrastructure:** Docker & Docker Compose

## 🏗️ Architecture

1.  **Client** sends an image via `POST /ocr`.
2.  **API** saves the file to a shared volume, pushes a task to **Redis**, and immediately returns a `task_id`.
3.  **Celery Worker** picks up the task, performs image preprocessing, runs Tesseract, and computes confidence scores.
4.  **Client** polls `GET /result/{task_id}` to retrieve the final structured data.

## ⚡ Quick Start

### Prerequisites

- Docker & Docker Compose

### Running the Application

1.  Clone the repository:

    ```bash
    git clone https://github.com/ibrahimi46/distributed-ocr-pipeline.git
    cd distributed-ocr-pipeline
    ```

2.  Start the services:
    ```bash
    docker compose up --build
    ```

The API will be available at `http://localhost:8000`.

## 📖 API Documentation

### 1. Submit an Image for Processing

**Endpoint:** `POST /ocr`

Uploads an image file to the processing queue.

**Request (cURL):**

```bash
curl -X POST "http://localhost:8000/ocr" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/image.png"
```
