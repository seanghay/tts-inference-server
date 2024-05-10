from io import BytesIO
from uuid import uuid4
from dataclasses import dataclass
from pydub import AudioSegment
from fastapi.responses import Response
from pydantic import BaseModel
from fastapi import FastAPI
from tts import text_to_audio

@dataclass
class TextToSpeechBody(BaseModel):
  text: str


def write_mp3(filename, data, sample_rate, sample_width):
  audio = AudioSegment(
    data, frame_rate=sample_rate, sample_width=sample_width, channels=1
  )
  audio.export(filename, format="mp3", bitrate="320k")


app = FastAPI()

@app.post("/text-to-speech")
def generate_tts(body: TextToSpeechBody):
  filename = f"audio-{str(uuid4())}.mp3"
  data = text_to_audio(body.text)
  
  with BytesIO() as fp:
    write_mp3(fp, data.tobytes(), 22050, data.dtype.itemsize)
    fp.seek(0)
    return Response(
      content=fp.read(),
      media_type="audio/mpeg",
      headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


