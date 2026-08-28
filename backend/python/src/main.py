from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src import logic

app = FastAPI()

class ScanRequest(BaseModel):
    folder_path: str
    threshold: int = 8

@app.post("/analyze")
async def analyze_images(request: ScanRequest):
    try:
        duplicates = logic.find_duplicates(
            folder_path=request.folder_path,
            threshold=request.threshold
        )
        return {
            "status": "success",
            "data": duplicates
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
