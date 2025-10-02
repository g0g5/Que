from .base import TranslatorProvider
from google import genai
from google.genai import types


class GeminiProvider(TranslatorProvider):
    def __init__(self, api_key: str, model: str):
        super().__init__()
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def translate(self, lang: str, content: str) -> str:
        system_instruction = f"You are a translator. You translate the text wrapped in xml tag <text>...</text> into {lang} in user's input. Output translated text wrapped in xml tag <translated lang=\"{lang}\">...</translated>. Your reply starts with <translated lang=\"{lang}\">."
        
        response = self.client.models.generate_content(
            model=self.model,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0),
                system_instruction=system_instruction,
            ),
            contents= f"<text>{content}</text>"
        )

        try:
            translated_text = response.text.split("<translated lang=\"")[1].split(">")[1].split("</translated")[0]
            return translated_text
        except:
            return ""