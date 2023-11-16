import speech_recognition as sr
from pydub import AudioSegment
from fastapi import HTTPException
from io import BytesIO

class AudioProcessControllerClass():

    async def audio_preprocess_and_store(file):
        try:
            # Read the audio file
            upload_audio = await file.read()

            # Convert audio to WAV
            audio = AudioSegment.from_file(BytesIO(upload_audio))
            wav_data = audio.export(format="wav").read()

            # Save the WAV file on the server
            wav_filename = f"{file.filename.rsplit('.', 1)[0]}.wav"
            wav_path = f"uploads/{wav_filename}"  # Specify your desired path

            with open(wav_path, "wb") as wav_file:
                wav_file.write(wav_data)

            return {"message": "Conversion successful", "wav_filename": wav_filename}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def audio_to_text(audio_file_path):
        recognizer = sr.Recognizer()

        # Load the audio file
        audio_file = sr.AudioFile(audio_file_path)

        with audio_file as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)

            # Listen to the audio file
            audio = recognizer.record(source)

            try:
                # Use the recognizer to convert speech to text
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Google API request failed; {e}")

audioProcessController = AudioProcessControllerClass()