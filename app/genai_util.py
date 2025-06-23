import os
from google import genai
from google.genai import types
from config import GEMINI_FLASH_MODEL

class GeminiClient:
    def __init__(self, temperature=0.2, top_p=1.0, top_k=1, candidate_count=1, api_key=None):
        self.parameters = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "candidate_count": candidate_count,
        }
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)

        self.generation_config = types.GenerateContentConfig(
            temperature=self.parameters["temperature"],
            top_p=self.parameters["top_p"],
            top_k=self.parameters["top_k"],
            candidate_count=self.parameters["candidate_count"],
            safety_settings=[
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                ),
            ],
        )

    def generate(self, prompt: str, images: list[dict] = None):
        input_parts = [types.Part(text=prompt)]

        if images:
            for image in images:
                input_parts.append(
                    types.Part.from_data(
                        data=image["data"],
                        mime_type=image["mime_type"]
                    )
                )

        response = self.client.models.generate_content(
            model=GEMINI_FLASH_MODEL,
            contents=input_parts,
            config=self.generation_config
        )
        return response.text.strip()

    def get_joke(self):
        input_parts = [types.Part(text="Tell me a short, funny joke.")]
        response = self.client.models.generate_content(
            model=GEMINI_FLASH_MODEL,
            contents=input_parts,
            config=self.generation_config
        )
        return response.text.strip()
