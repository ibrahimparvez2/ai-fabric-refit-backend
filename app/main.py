from fastapi import FastAPI, UploadFile, File, Form
from typing import List, Optional
from genai_util import GeminiClient
import os
import traceback

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

gemini = GeminiClient(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/")
def health_check():
    return {"status": "ok"}


from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List

app = FastAPI()

@app.post("/analyze_fabrics")
async def analyze_fabrics(images: List[UploadFile] = File(...)):
    print(f"Received files: {[file.filename for file in images]}")
    try:
        image_payloads = []
        for image in images:
            image_data = await image.read()
            image_payloads.append({
                "data": image_data,
                "mime_type": image.content_type
            })

        results = gemini.analyze_fabrics(image_payloads)
        return results
    except Exception as e:
        tb = traceback.format_exc()
        print(f"[ERROR] Failed to analyze fabric batch: {e}\n{tb}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "traceback": tb.splitlines()[-10:]  # last few lines of traceback for clarity
        }
        )


@app.get("/joke")
async def joke():
    joke_text = gemini.get_joke()
    return {"joke": joke_text}