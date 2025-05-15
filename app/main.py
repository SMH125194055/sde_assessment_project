import uuid
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException, Header, BackgroundTasks, Request
from app.utils import mock_model_predict
from app.models import (
    PredictionRequest,
    SyncPredictionResponse,
    AsyncPredictionSubmitResponse,
    PredictionStatusResponse
)

# Initialize FastAPI app
app = FastAPI(title="ZypherAI Mock Prediction Service")

# In-memory storage for asynchronous prediction results and statuses.
#  For a production system, you'd use a database or a more robust distributed cache. 
# Key: prediction_id (str), Value: Dict {"status": str, "result": Optional[Dict[str, str]]}
prediction_store: Dict[str, Dict] = {}

# --- Helper function for background task ---
def process_prediction_background(prediction_id: str, input_data: str):
    print(f"Background task started for prediction_id: {prediction_id}")
    try:
        result = mock_model_predict(input_data)
        prediction_store[prediction_id] = {"status": "completed", "result": result}
        print(f"Background task completed for prediction_id: {prediction_id}. Result: {result}")
    except Exception as e:
        print(f"Error in background task for prediction_id: {prediction_id}: {e}")
        prediction_store[prediction_id] = {"status": "failed", "result": None, "error": str(e)}

# --- Endpoints ---

@app.get("/", summary="Root endpoint to check service status")
async def read_root():
    
    return {"message": "Welcome to the ZypherAI Mock Prediction Service!"}

@app.post("/predict",
            response_model=None, # Using None because response type varies
            summary="Run synchronous or asynchronous model prediction",
            description="Accepts user input for model prediction. "
                         "If 'Async-Mode' header is true, processes asynchronously.")
async def predict(
    request_data: PredictionRequest,
    background_tasks: BackgroundTasks,
     async_mode: Optional[str] = Header(None, alias="Async-Mode") # 
) -> Dict:
    
    user_input = request_data.input

    # This line is indented 4 spaces from the margin
    if async_mode and async_mode.lower() == "true":
        # This line is indented 8 spaces from the margin (4 for 'if' + 4 more)
        prediction_id = str(uuid.uuid4())
        # This line MUST ALSO be indented 8 spaces from the margin
        prediction_store[prediction_id] = {"status": "processing", "result": None}
        # This line MUST ALSO be indented 8 spaces from the margin
        print(f"Asynchronous request received. Prediction ID: {prediction_id}, Input: {user_input}")
        # And so on...
        background_tasks.add_task(process_prediction_background, prediction_id, user_input)
        return AsyncPredictionSubmitResponse(
            message="Request received. Processing asynchronously.",
            prediction_id=prediction_id
        ).model_dump()
    # This 'else' aligns with the 'if' (4 spaces from the margin)
    else:
        # Content inside 'else' would be 8 spaces from the margin
        print("Synchronous processing")
        #  Synchronous Processing 
        print(f"Synchronous request received. Input: {user_input}")
        result = mock_model_predict(user_input)
        #  FastAPI will return 200 OK by default 
        return SyncPredictionResponse(**result).model_dump()


@app.get("/predict/{prediction_id}",
           response_model=PredictionStatusResponse,
           summary="Retrieve asynchronous prediction status or results",
            description="Fetches the status or result of an asynchronous prediction request using its ID.")
async def get_prediction_status(prediction_id: str) -> PredictionStatusResponse:
    
    print(f"Status check for prediction_id: {prediction_id}")
    job = prediction_store.get(prediction_id)

    if not job:
        print(f"Prediction ID not found: {prediction_id}")
        raise HTTPException(status_code=404, detail="Prediction ID not found.") # 

    if job["status"] == "processing":
        print(f"Prediction still processing for ID: {prediction_id}")
        #  The assessment specifies 400 for processing 
        raise HTTPException(status_code=400, detail="Prediction is still being processed.")

    if job["status"] == "completed":
        print(f"Prediction completed for ID: {prediction_id}. Result: {job['result']}")
        return PredictionStatusResponse(
            prediction_id=prediction_id,
            output=job["result"]
         ) # 

    if job["status"] == "failed":
        print(f"Prediction failed for ID: {prediction_id}. Error: {job.get('error')}")
        raise HTTPException(status_code=500, detail=job.get("error", "Prediction processing failed."))

    # Should not be reached if statuses are handled correctly
    raise HTTPException(status_code=500, detail="Unknown prediction status.")

