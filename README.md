
# WaveVox (Backend)

WaveVox, powered by FastAPI and Angular, seamlessly converts text to audio, transcribes audio to text, and crafts personalized voice scripts. Effortlessly transform content with efficiency and security. Unleash creativity and streamline your audio needs with user-friendly, dynamic solution for personalized content creation.



## Installation

#### Create a Virtual Environment
```bash
python -m venv env

```

Activate the Virtual Environment

Windows
```bash
.\env\Scripts\activate

```

Linux
```bash
source env/bin/activate

```
    
#### nstall Requirements

Linux
```bash
pip install -r requirements.txt

```
##### (Note: If there is no requirements.txt file, create one with the necessary dependencies for your project.)

#### Install FFmpeg

Download FFmpeg from https://ffmpeg.org/download.html

Install FFmpeg and add it to your system's PATH.

#### Set Up Environment Variables

Ensure that FFmpeg is added to your system's PATH.

#### Run the Project

Linux
```bash
uvicorn main:app --reload

```
## API Documentation

The API documentation is available at:

#### [Swagger UI](http://127.0.0.1:8000/docs)
#### [ReDoc](http://127.0.0.1:8000/redoc)

