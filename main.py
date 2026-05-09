from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/video-dub")
async def video_dub(file: UploadFile = File(...)):

    content = await file.read()

    return {
        "original_text": "test",
        "khmer_text": "សាកល្បង",
        "video": "output.mp4"
    }
