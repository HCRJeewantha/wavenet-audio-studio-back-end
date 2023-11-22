import speech_recognition as sr
from pydub import AudioSegment
from fastapi import HTTPException, UploadFile
from io import BytesIO
import random
import string
from database.sqlite_connection import get_db
from sqlalchemy.orm import Session
from models.sqlite_models import Audio
from enums.enum_storage import AudioTypes
from fastapi.responses import StreamingResponse
from gtts import gTTS
from fastapi.responses import JSONResponse
import pyttsx3
import os
from pathlib import Path

db: Session = next(get_db())


def get_digit_code(k=4):
    digit = ''.join(random.choices(string.digits, k=k))
    return digit
class AudioProcessControllerClass():

    async def save_audio_data(self, name, path, type, user_id):
        try:
            audio = Audio(
                name=name,
                path=path,
                type=type,
                user_id=user_id,
            )

            db.add(audio)
            db.commit()
            db.refresh(audio)

            data = {
                "id": audio.id
            }

            return JSONResponse({
                    "status": True,
                    "message": "Audio has been updated successful",
                    "result": data
                })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
        finally:
            db.close()

    async def remove_audio_data(self, id):
        try:
            audio: Audio = db.query(
                Audio
            ).filter(
                Audio.id ==id
            ).first()

            file_path = audio.path
            file_path = Path(file_path)
            file_path.unlink()

            db.delete(audio)
            db.commit()

            return JSONResponse({
                    "status": True,
                    "message": "Audio has been updated successful",
                    "result": ""
                })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
        finally:
            db.close()

    async def get_audio(self, authentication):
        try:
            user_id = authentication.sub

            audio_list: list[Audio] = db.query(
                Audio
            ).filter(
                Audio.user_id == user_id
            ).all()

            data = []

            for item in audio_list:
                audio = {
                    "id": item.id,
                    "name": item.name,
                    "path": item.path,
                    "type": item.type,
                    
                }
                data.append(audio)

            return JSONResponse({
                        "status": True,
                        "message": "Audio list",
                        "result": data
                    })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
        finally:
            db.close()

    async def get_audio_by_path(self, path, authentication):

        return StreamingResponse(
            open(path, "rb"),
            media_type="audio/wav",
            headers={"Content-Disposition": f"attachment; filename={os.path.basename(path)}"}
        )

    async def audio_preprocess_and_store(self, file, authentication):
        user_id = authentication.sub
        unique_code = get_digit_code(4)

        try:
            # Read the audio file
            upload_audio = await file.read()

            # Convert audio to WAV
            audio = AudioSegment.from_file(BytesIO(upload_audio))
            wav_data = audio.export(format="wav").read()

            # Save the WAV file on the server
            wav_filename = f"{user_id}_{unique_code}_{file.filename.rsplit('.', 1)[0]}.wav"
            wav_path = f"audio/uploads/{wav_filename}"  # Specify your desired path

            # save audio path in db
            await self.save_audio_data(wav_filename, wav_path, AudioTypes.Original, user_id)

            with open(wav_path, "wb") as wav_file:
                wav_file.write(wav_data)

            return JSONResponse({
                    "status": True,
                    "message": "Audio has been updated successful",
                    "result": audio
            })

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
        
    async def get_audio_by_id(self, id:int):
        try:
            audio_file = db.query(
                Audio
            ).filter(
                Audio.id == id
            ).first()

            return audio_file
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")
        finally:
            db.close()

    async def audio_to_text(self, file):
        recognizer = sr.Recognizer()

        if file:
            # Load the audio file
            audio_file = sr.AudioFile(file)

            with audio_file as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source)

                # Listen to the audio file
                audio = recognizer.record(source)

                try:
                    # Use the recognizer to convert speech to text
                    text = recognizer.recognize_google(audio)

                    return JSONResponse({
                    "status": True,
                    "message": "Audio to text conversion successful",
                    "result": text
                    })
                except sr.UnknownValueError:
                    raise HTTPException(status_code=500, detail=f"Could not understand audio: {str(e)}")
                except sr.RequestError as e:
                    raise HTTPException(status_code=500, detail=f"Google API request failed: {str(e)}")

    async def text_to_audio(self, text:str, authentication, gender: str = 'male'):
        try:
            engine = pyttsx3.init()

            # Set the voice gender
            voices = engine.getProperty('voices')

            # languages = set(voice.languages[0] for voice in voices)
            # print("Available Languages:", languages)

            if gender.lower() == 'female':
                engine.setProperty('voice', voices[1].id)  # Index 1 corresponds to a female voice
            
            user_id = authentication.sub
            unique_code = get_digit_code(4)

            wav_filename = f"{user_id}_{unique_code}_text_to_speech.wav"
            output_path = f"audio/text_to_audio/{wav_filename}"

            engine.save_to_file(text, output_path)
            engine.runAndWait()

            # Return the audio as a streaming response
            return StreamingResponse(
            open(output_path, "rb"),
            media_type="audio/wav",
            headers={"Content-Disposition": f"attachment; filename={os.path.basename(output_path)}"}
        )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error converting text to speech: {str(e)}")
        finally:
            engine.stop()
        

    async def shift_pitch(self, audio_data: bytes, semitones: int, authentication):
        audio = AudioSegment.from_file(BytesIO(audio_data))
        shifted = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * (2 ** (semitones / 12.0)))
        })

        user_id = authentication.sub
        unique_code = get_digit_code(4)

        wav_filename = f"{user_id}_{unique_code}_pitch_shift.wav"
        wav_path = f"audio/shift_pitch/{wav_filename}"  # Specify your desired path

        shifted.export(wav_path, format="wav")

        # save audio path in db
        # await self.save_audio_data(wav_filename, wav_path, AudioTypes.Modified, user_id)

        return StreamingResponse(
            open(wav_path, "rb"),
            media_type="audio/wav",
            headers={"Content-Disposition": f"attachment; filename={os.path.basename(wav_path)}"}
        )
    
    async def save_audio(self, type, file: UploadFile, authentication):
        user_id = authentication.sub
        unique_code = get_digit_code(4)

        wav_filename = f"{user_id}_{unique_code}_upload.wav"
        try:
            if type == 1:
                wav_path = f"audio/uploads/{wav_filename}"
            if type == 2:
                wav_path = f"audio/text_to_audio/{wav_filename}"
            if type == 3:
                wav_path = f"audio/shift_pitch/{wav_filename}"
                
            with open(wav_path, "wb") as audio_file:
                audio_file.write(file.file.read())

            return  await self.save_audio_data(wav_filename, wav_path, type, user_id)
            

        except Exception as e:
            raise e
        



audioProcessController = AudioProcessControllerClass()