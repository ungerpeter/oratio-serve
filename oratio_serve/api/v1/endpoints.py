from fastapi import APIRouter, UploadFile, File, Depends
from oratio_serve.services.inference_service import InferenceService
from oratio_serve.api.v1.schemas import TranscriptionResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def get_inference_service():
    return InferenceService()

@router.post("/asr/", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...), 
    inference_service: InferenceService = Depends(get_inference_service)
):
    logger.info("Received transcription request")
    transcription = await inference_service.transcribe(file)
    return TranscriptionResponse(transcription=transcription)