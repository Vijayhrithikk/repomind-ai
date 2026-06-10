from google import genai

from app.core.config import (
    GEMINI_API_KEY,
)


class GeminiClient:

    _cache = {}

    def __init__(self):

        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate(
        self,
        prompt: str,
    ) -> str:

        if prompt in self._cache:

            print("Cache hit")

            return self._cache[prompt]

        response = (
            self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
        )

        text = response.text

        self._cache[prompt] = text

        return text