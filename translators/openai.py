import openai
from .base import TranslatorProvider


class OpenAIProvider(TranslatorProvider):
    def __init__(self, base_url: str, api_key: str, model: str):
        super().__init__()
        self.client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model = model

    def translate(self, lang: str, content: str) -> str:
        system_instruction = f"You are a translator. You translate ALL user inputs wrapped in <text> </text> into {lang}. Output translated text wrapped in <translated lang=\"{lang}\"> </translated>. Your reply starts with <translated lang=\"{lang}\">."
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_instruction,
                },
                {
                    "role": "user",
                    "content": f"<text>{content}</text>",
                }
            ],
            model=self.model,
        )
        
        response_text = chat_completion.choices[0].message.content
        # Parse the response_text, extract the translated text with string split like gemini
        try:
            translated_text = response_text.split("<translated lang=\"")[1].split(">")[1].split("</translated")[0]
            return translated_text
        except:
            return ""