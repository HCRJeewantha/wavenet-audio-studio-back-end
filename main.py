from fastapi import FastAPI

app = FastAPI()


@app.post("/convert-audio-to-text")
async def audio_to_text():
    return {"message": "Hello World"}

