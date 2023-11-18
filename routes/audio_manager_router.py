from fastapi import APIRouter, Depends, Body, Query, UploadFile, HTTPException, File
from controllers.audio_process_controller import audioProcessController

from middleware.user_middle_wares import Authorization
from fastapi.responses import StreamingResponse
from pydub import AudioSegment
from pydub import AudioSegment
from io import BytesIO
from fastapi.responses import JSONResponse
import os
import shutil
from request.audio_manager_requests import GetAudioRequest

router = APIRouter(
    prefix="/audio-manager",
    tags=["Audio Manager"],
)

@router.post("/convert-audio-to-text")
async def audio_to_text(file: UploadFile = File(...), authentication=Depends(Authorization())):
    try:
        temp_file_path = f"{file.filename}"
       
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        value = await audioProcessController.audio_to_text(temp_file_path)

        # Clean up temporary file
        os.remove(temp_file_path)
        return value
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get("/convert-text-to-audio/{text}")
async def audio_to_text(text:str,gender: str, authentication=Depends(Authorization())):
    return await audioProcessController.text_to_audio(text, authentication, gender)

@router.post("/audio-shift-pitch")
async def shift_pitch_endpoint(file: UploadFile = File(...), semitones: int = 0, authentication=Depends(Authorization())):
    contents = await file.read()
    return await audioProcessController.shift_pitch(contents, semitones, authentication)


@router.post("/save-audio/{type}")
async def save_audio(type: int, file: UploadFile = File(...), authentication=Depends(Authorization())):
    return await audioProcessController.save_audio(type, file, authentication)

@router.delete("/remove-audio/{id}")
async def save_audio(id: int, authentication=Depends(Authorization())):
    return await audioProcessController.remove_audio_data(id)

@router.get("/get-audio-list")
async def get_audio(authentication=Depends(Authorization())):
    return await audioProcessController.get_audio(authentication)

@router.post("/get-audio")
async def get_audio_by_path(request:GetAudioRequest, authentication=Depends(Authorization())):
    return await audioProcessController.get_audio_by_path(request.path, authentication)