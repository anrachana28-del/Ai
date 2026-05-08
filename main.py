from fastapi import FastAPI, UploadFile, File
import uuid, subprocess
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator
import edge_tts

app=FastAPI()
model=WhisperModel("base")

@app.post("/video-dub")
async def video_dub(file:UploadFile=File(...)):

    uid=str(uuid.uuid4())

    video=f"/tmp/{uid}.mp4"
    audio=f"/tmp/{uid}.mp3"
    voice=f"/tmp/{uid}_voice.mp3"
    silent=f"/tmp/{uid}_silent.mp4"
    output=f"/tmp/{uid}_final.mp4"

    # save video
    with open(video,"wb") as f:
        f.write(await file.read())

    # extract audio
    subprocess.call([
        "ffmpeg","-y","-i",video,
        "-vn",audio
    ])

    # speech to text
    segments,_=model.transcribe(audio)
    text=" ".join([s.text for s in segments])

    # translate Khmer
    khmer=GoogleTranslator("auto","km").translate(text)

    # AI voice
    tts=edge_tts.Communicate(khmer,"km-KH-PisethNeural")
    await tts.save(voice)

    # remove original audio
    subprocess.call([
        "ffmpeg","-y","-i",video,
        "-an",silent
    ])

    # merge new voice into video
    subprocess.call([
        "ffmpeg","-y",
        "-i",silent,
        "-i",voice,
        "-c:v","copy",
        "-map","0:v:0",
        "-map","1:a:0",
        output
    ])

    return{
        "original_text":text,
        "khmer_text":khmer,
        "video":output
    }