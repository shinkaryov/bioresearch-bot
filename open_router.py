import os
import requests


class LLMOpenRouter:
    def __init__(self, api_key: str = None, model: str = "meta-llama/llama-3.3-70b-instruct:free"):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is not set")
        self.model = model
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Title": "bioresearch-bot"
        }

    def summarize(self, title: str, abstract: str, max_tokens: int = 300) -> str:
        prompt = (
            "Оціни наукову новизну та важливість наступної публікації."
            " Ігноруй символи, розділові знаки та технічні особливості тексту."
            " Якщо стаття не містить нових гіпотез, важливих знахідок або інновацій, напиши: ❌ Відхилено."
            " Інакше — коротко перекажи суть публікації українською."
            "\n\nНазва: " + title + "\nТекст: " + abstract
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "Ти асистент з оцінки наукових медичних публікацій."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3
        }

        response = requests.post(self.url, headers=self.headers, json=payload)
        if response.status_code != 200:
            raise RuntimeError(f"OpenRouter API error: {response.text}")

        return response.json()["choices"][0]["message"]["content"]
