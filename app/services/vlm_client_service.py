from __future__ import annotations

import base64
from io import BytesIO

from django.conf import settings

from app.services.vlm_provider import ImageFormat, VLMProvider

_vlm_service_instance = None


def get_vlm_service() -> VLMClientService:
    """Get or create the VLM client service (lazy singleton)."""
    global _vlm_service_instance
    if _vlm_service_instance is None:
        _vlm_service_instance = VLMClientService(
            settings.VLM_PROVIDER,
            settings.VLM_MODEL,
        )
    return _vlm_service_instance


class VLMClientService:
    def __init__(self, provider_name: str, model_name: str):
        self.provider = self._create_provider(provider_name, model_name)

    def _create_provider(self, provider_name: str, model_name: str) -> VLMProvider:
        if provider_name == 'ollama':
            from app.services.providers.ollama import OllamaProvider
            return OllamaProvider(
                server_url=settings.OLLAMA_SERVER_URL,
                model_name=model_name,
            )
        else:
            raise ValueError(f"Unknown VLM provider: {provider_name}")

    def generate_labels(self, question: str, image: bytes) -> str:
        target_format = self.provider.supported_formats[0]
        formatted_image = self._convert_format(image, target_format)
        return self.provider.generate_labels(question, formatted_image)

    def _convert_format(self, image_bytes: bytes, target_format: ImageFormat):
        """Convert image bytes to provider's preferred format."""
        match target_format:
            case ImageFormat.BASE64:
                return base64.b64encode(image_bytes).decode('utf-8')
            case ImageFormat.BYTES:
                return image_bytes
            case ImageFormat.PIL_IMAGE:
                from PIL import Image
                return Image.open(BytesIO(image_bytes))
            case _:
                raise ValueError(f"Unknown format: {target_format}")
