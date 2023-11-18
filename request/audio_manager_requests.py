from pydantic import BaseModel
from fastapi import UploadFile

class AudioTextRequest(BaseModel):
    file: UploadFile

class GetAudioRequest(BaseModel):
    path: str