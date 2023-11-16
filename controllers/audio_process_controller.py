import speech_recognition as sr

class AudioProcessControllerClass():
    async def speech_to_text(audio_file_path):
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