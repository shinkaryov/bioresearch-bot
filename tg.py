import os
import requests


class TelegramNotifier:
    def __init__(self, token: str = None, chat_id: str = None):
        self.token = token or os.getenv("TG_TOKEN")
        if not self.token:
            raise ValueError("TG_TOKEN is not set")

        self.chat_id = chat_id or os.getenv("TG_CHAT_ID")
        if not self.chat_id:
            raise ValueError("TG_CHAT_ID is not set")

        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, text: str):
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text
        }

        response = requests.post(url, data=payload)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to send message: {response.text}")
        return response.json()

