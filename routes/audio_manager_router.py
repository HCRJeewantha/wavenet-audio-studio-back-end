from typing import Optional
from fastapi import APIRouter, Depends, Body, Query, UploadFile, HTTPException, File
from pydub import AudioSegment
from io import BytesIO

router = APIRouter(
    prefix="/audio-manager",
    tags=["Audio Manager"],
)

@router.post("/convert-audio-to-text")
async def audio_to_text():
    return {"message": "Hello World"}


@router.post("/convert-audio-to-text")
async def audio_to_text():
    return {"message": "Hello World"}

@router.post("/upload-audio")
async def convert_file(file: UploadFile = File(...)):
    return