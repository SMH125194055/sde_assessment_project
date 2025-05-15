from pydantic import BaseModel
from typing import Dict, Optional

class PredictionRequest(BaseModel):
    input: str

class SyncPredictionResponse(BaseModel):
    input: str
    result: str

class AsyncPredictionSubmitResponse(BaseModel):
    message: str
    prediction_id: str

class PredictionStatusResponse(BaseModel):
    prediction_id: Optional[str] = None
    status: Optional[str] = None # e.g., "processing", "completed", "not_found"
    output: Optional[Dict[str, str]] = None
    error: Optional[str] = None