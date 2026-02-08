from typing import Any

import requests
from django.conf import settings


class OllamaClient:
    def __init__(self) -> None:
        self._ollama_url = settings.OLLAMA_SERVER_URL

    def get_tags(self) -> dict[str, Any]:
        response = requests.get(self._ollama_url + '/api/tags')
        response.raise_for_status()
        return response.json()

    def ask_with_image(self, question: str) -> str:
        raise NotImplementedError
