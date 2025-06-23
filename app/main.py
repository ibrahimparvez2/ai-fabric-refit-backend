from fastapi import FastAPI, UploadFile, File, Form
from typing import List, Optional
from genai_util import GeminiClient
import os

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

gemini = GeminiClient(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/generate")
async def generate_with_images(
    prompt: str = Form(...),
    images: Optional[List[UploadFile]] = File(None),
):
    image_parts = []

    if images:
        for image in images:
            content = await image.read()
            image_parts.append({
                "mime_type": image.content_type,
                "data": content,
            })

    result = gemini.generate(prompt=prompt, images=image_parts)
    return {"result": result}

@app.get("/joke")
async def joke():
    joke_text = gemini.get_joke()
    return {"joke": joke_text}