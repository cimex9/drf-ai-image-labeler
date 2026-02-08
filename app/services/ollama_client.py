import base64
from typing import Any

import requests
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile


class OllamaClient:
    def __init__(self) -> None:
        self._ollama_url = settings.OLLAMA_SERVER_URL
        self._model = settings.OLLAMA_MODEL

    def get_tags(self) -> dict[str, Any]:
        response = requests.get(self._ollama_url + '/api/tags')
        response.raise_for_status()
        return response.json()

    # TODO: don't use UploadedFile here
    def ask_with_image(self, question: str, image: UploadedFile) -> str:
        url = f"{self._ollama_url}/api/generate"
        with image.file.open('rb') as f:
            image_bytes = f.read()
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')

        payload = {
            'model': self._model,
            "prompt": question,
            "images": [image_b64],
            'stream': False,
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
