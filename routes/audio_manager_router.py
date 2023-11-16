from fastapi import APIRouter, Depends, Body, Query, UploadFile, HTTPException, File
from controllers.audio_process_controller import audioProcessController

from middleware.user_middle_wares import Authorization
from fastapi.responses import StreamingResponse
from pydub import AudioSegment
from pydub import AudioSegment
from io import BytesIO

router = APIRouter(
    prefix="/audio-manager",
    tags=["Audio Manager"],
)

@router.get("/convert-audio-to-text/{audio_id}")
async def audio_to_text(audio_id:int, authentication=Depends(Authorization())):
    return await audioProcessController.audio_to_text(audio_id)

@router.get("/convert-text-to-audio/{text}")
async def audio_to_text(text:str):
    return await audioProcessController.text_to_audio(text)




@router.post("/audio-shift-pitch")
async def shift_pitch_endpoint(file: UploadFile = File(...), semitones: int = 0, authentication=Depends(Authorization())):
    contents = await file.read()
    shifted_audio = await audioProcessController.shift_pitch(contents, semitones, authentication)
    return True