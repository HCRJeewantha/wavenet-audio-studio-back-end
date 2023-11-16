from typing import Optional
from fastapi import APIRouter, Depends, Body, Query

router = APIRouter(
    prefix="/audio-manager",
    tags=["Audio Manager"],
)


@router.post("/convert-audio-to-text")
async def audio_to_text():
    return {"message": "Hello World"}
