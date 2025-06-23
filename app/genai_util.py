import os
from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig
from config import GEMINI_FLASH_MODEL
from models import FabricAnalysis, FABRIC_RESPONSE_SCHEMA

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

    def analyze(self, image_data: bytes, image_mime_type="image/jpeg") -> dict:
        input_parts = [
            types.Part(text=(
                "Analyze this fabric image and provide detailed information about: "
                "material composition, color palette (including secondary colors), "
                "pattern characteristics, texture properties, structural elements, and style context. "
            )),
            types.Part(
            inline_data=genai.types.Blob(
                mime_type=image_mime_type,
                data=image_data
            )
        )
        ]

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=input_parts,
            config=GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=FABRIC_RESPONSE_SCHEMA)
        )

        import json
        try:
            response_obj = json.loads(response.text)
        except json.JSONDecodeError:
            raise ValueError("Gemini response was not valid JSON")

        fabric_analysis = FabricAnalysis.parse_obj(response_obj)
        return fabric_analysis.dict()

    def analyze_fabrics(self, images: list[dict]) -> list[dict]:
        print("inside analyze_fabrics")
        results = []
        for img in images:
            print(img)
            result = self.analyze(image_data=img["data"], image_mime_type=img.get("mime_type"))
            results.append(result)
        return results


    def get_joke(self):
        input_parts = [types.Part(text="Tell me a short, funny joke.")]
        response = self.client.models.generate_content(
            model=GEMINI_FLASH_MODEL,
            contents=input_parts,
            config=self.generation_config
        )
        return response.text.strip()
