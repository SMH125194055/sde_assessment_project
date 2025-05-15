# ZypherAI Mock Prediction Service - SDE Assessment

This project implements a web application server that simulates machine learning model predictions. It's developed as part of the SDE Assessment for ZypherAI, allowing users to submit data for synchronous or asynchronous mock predictions and retrieve results.

**Last Updated:** May 15, 2025

## Features

* **Synchronous Predictions:** A `/predict` (POST) endpoint for immediate mock model predictions.
* **Asynchronous Predictions:**
  * The `/predict` (POST) endpoint supports an `Async-Mode: true` header for non-blocking requests.
  * Returns a `prediction_id` for tracking.
  * A `/predict/{prediction_id}` (GET) endpoint to retrieve the status and results of asynchronous predictions.
* **Mock Model Simulation:** Utilizes the provided `mock_model_predict` function to simulate processing delay and generate randomized results.
* **Containerized Application:** Includes a `Dockerfile` for building and running the application with Docker.
* **Modern Python Framework:** Built using FastAPI, providing automatic data validation, serialization, and interactive API documentation.
* **In-Memory Task Management:** Asynchronous task statuses and results are managed in memory for simplicity, as permitted by the assessment.

## Project Structure

sde_assessment_project/

├── app/

│   ├── init.py         # Makes 'app' a Python package

│   ├── main.py             # FastAPI application, endpoint logic

│   ├── models.py           # Pydantic models for request/response validation

│   └── utils.py            # Contains the mock_model_predict function

├── .gitignore              # Specifies intentionally untracked files

├── Dockerfile              # Defines the Docker image for the application

├── README.md               # This file: project documentation

└── requirements.txt        # Python package dependencies

## Prerequisites

* Python 3.9+ (The code uses features compatible with Python 3.9; adapt if using other versions)
* pip (Python package installer)
* Docker (for containerized deployment, as per Part C of the assessment)

## Setup and Running Locally (Without Docker)

1. **Clone the repository (or create the files as described):**
   If you have this project in a Git repository:

   ```bash
   git clone <your-repo-url>
   cd sde_assessment_project
   ```

   Otherwise, ensure all the files listed in the "Project Structure" are in place with the correct content.
2. **Create and activate a virtual environment (recommended):**

   ```bash
   python -m venv venv
   ```

   * **Windows (Command Prompt/PowerShell):**
     ```bash
     venv\Scripts\activate
     ```
   * **macOS/Linux (bash/zsh):**
     ```bash
     source venv/bin/activate
     ```
3. **Install dependencies:**
   Ensure your `requirements.txt` contains:

   ```
   fastapi
   uvicorn[standard]
   ```

   Then run:

   ```bash
   pip install -r requirements.txt
   ```
4. **Run the FastAPI application using Uvicorn:**
   From the `sde_assessment_project` root directory:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
   ```

   * The `--reload` flag enables auto-reloading on code changes, useful for development.
5. **Access the application:**

   * **Root endpoint:** `http://localhost:8080/`
   * **Interactive API Docs (Swagger UI):** `http://localhost:8080/docs`
   * **Alternative API Docs (ReDoc):** `http://localhost:8080/redoc`

## Building and Running with Docker

1. **Ensure Docker Desktop is installed and running.**
2. **Navigate to the project root directory (`sde_assessment_project`).**
3. **Build the Docker image:**

   ```bash
   docker build -t zypherai-mock-predictor .
   ```

   (You can replace `zypherai-mock-predictor` with your preferred image name).
4. **Run the Docker container:**

   ```bash
   docker run -p 8080:8080 zypherai-mock-predictor
   ```

   * This maps port 8080 on your host to port 8080 in the container.
5. **Access the application (same URLs as running locally):**

   * **API Docs (Swagger UI):** `http://localhost:8080/docs`

## API Endpoints

The application exposes the following endpoints. For detailed request/response schemas and interactive testing, please use the Swagger UI at `http://localhost:8080/docs`.

* **`GET /`**:

  * Description: Root endpoint to check service status.
  * Response: A welcome message: `{"message":"Welcome to the ZypherAI Mock Prediction Service!"}`
* **`POST /predict`**:

  * Description: Submits input data for model prediction. Operates synchronously by default.
    For asynchronous processing, include the header `Async-Mode: true`.
  * Request Body (JSON):
    ```json
    {
        "input": "your sample input data"
    }
    ```
  * Synchronous Response (200 OK):
    ```json
    {
        "input": "your sample input data",
        "result": "mocked_result_value"
    }
    ```
  * Asynchronous Response (202 Accepted, with `Async-Mode: true` header):
    ```json
    {
        "message": "Request received. Processing asynchronously.",
        "prediction_id": "unique-prediction-id"
    }
    ```
* **`GET /predict/{prediction_id}`**:

  * Description: Retrieves the status or result of an asynchronous prediction request using its ID.
  * Responses:
    * **200 OK (Completed):**
      ```json
      {
          "prediction_id": "unique-prediction-id",
          "output": {"input": "your sample input data", "result": "mocked_result_value"}
      }
      ```
    * **400 Bad Request (Processing):**
      ```json
      {
          "error": "Prediction is still being processed."
      }
      ```
    * **404 Not Found (Invalid ID):**
      ```json
      {
          "error": "Prediction ID not found."
      }
      ```
    * **500 Internal Server Error (Processing Failed):**
      ```json
      {
          "error": "Actual error message if prediction failed during background processing"
      }
      ```

## Assumptions Made

* **In-Memory Storage for Asynchronous Tasks:** Prediction statuses and results for asynchronous tasks are stored in a Python dictionary (`prediction_store`) in memory. This data will be lost if the server restarts. This approach was chosen for simplicity as allowed by the assessment.
* **Unique Prediction IDs:** `uuid.uuid4()` is used to generate unique `prediction_id` strings.
* **Error Handling:** Status codes and error messages for the `/predict/{prediction_id}` endpoint are implemented as specified in the assessment document (400 for processing, 404 for not found). A 500 error is returned if the background task encounters an unhandled exception.
* **Python Version:** The application is developed assuming Python 3.9+. FastAPI and Uvicorn are the primary dependencies.
* **`mock_model_predict` Function:** The provided mock function is used as is, simulating a delay and random output.

## Alternative Approaches Considered (and Not Pursued for this Assessment)

* **External Queue System (e.g., Redis, RabbitMQ, Kafka):**
  * **Reason for not pursuing:** While ideal for robust, scalable production systems, the assessment permitted in-memory storage for asynchronous tasks to maintain simplicity for this exercise. Implementing an external queue would involve additional setup (e.g., a `docker-compose.yml` for the queue service) and more complex task management logic.
  * **Benefits if used:** Would provide better task persistence, decoupling of services, horizontal scaling capabilities for worker processes, and more sophisticated retry mechanisms.
* **Celery with a Message Broker:**
  * **Reason for not pursuing:** Celery is a powerful distributed task queue system. For this assessment, FastAPI's built-in `BackgroundTasks` feature was deemed sufficient to meet the asynchronous processing requirement without adding external dependencies like Celery and a message broker (e.g., Redis or RabbitMQ).
  * **Benefits if used:** Similar to an external queue system, Celery offers more features for distributed task management, monitoring, and scaling.

## Thoughts on Efficiency and Optimization

* **Asynchronous Processing:** The use of `BackgroundTasks` in FastAPI for asynchronous predictions ensures the `/predict` endpoint remains responsive under async mode, as the client does not wait for the `mock_model_predict` function's delay.
* **FastAPI Performance:** FastAPI is a high-performance ASGI framework, known for its speed due to its use of Starlette and Pydantic.
* **Docker Image Optimization:** The provided `Dockerfile` uses a multi-stage build (a `builder` stage for installing dependencies and a slim `runtime` stage for the final image). This is a good practice for reducing the final image size.
* **`prediction_store` (In-Memory):**
  * **Time Complexity:** Dictionary lookups (for `GET /predict/{prediction_id}`) and insertions are O(1) on average.
  * **Space Complexity:** The `prediction_store` dictionary will grow linearly (O(N)) with the number of unique asynchronous prediction requests processed during the server's runtime. For a system with a very large number of long-running or persistent tasks, this would not be suitable, and a database or external cache would be necessary.
* **`mock_model_predict`:** The inherent delay in this function (10-17 seconds) is fixed and simulates an I/O-bound or compute-bound task. The application efficiently hands this off to a background task in async mode.

---
