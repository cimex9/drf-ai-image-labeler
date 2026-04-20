from __future__ import annotations

import base64
import logging
from io import BytesIO

from django.conf import settings

from app.services.vlm_provider import ImageFormat, VLMProvider

logger = logging.getLogger(__name__)

_vlm_service_instance = None


def get_vlm_service() -> VLMClientService:
    """Get or create the VLM client service (lazy singleton)."""
    global _vlm_service_instance
    if _vlm_service_instance is None:
        logger.info(
            f"Initializing VLM service with provider={settings.VLM_PROVIDER}, "
            f"model={settings.VLM_MODEL}"
        )
        _vlm_service_instance = VLMClientService(
            settings.VLM_PROVIDER,
            settings.VLM_MODEL,
        )
        logger.info("VLM service initialized successfully")
    return _vlm_service_instance


class VLMClientService:
    def __init__(self, provider_name: str, model_name: str):
        self.provider = self._create_provider(provider_name, model_name)

    def _create_provider(self, provider_name: str, model_name: str) -> VLMProvider:
        logger.debug(f"Creating VLM provider: {provider_name}")
        if provider_name == 'ollama':
            logger.debug(f"Using Ollama provider with server={settings.OLLAMA_SERVER_URL}")
            from app.services.providers.ollama import OllamaProvider
            return OllamaProvider(
                server_url=settings.OLLAMA_SERVER_URL,
                model_name=model_name,
            )
        else:
            logger.error(f"Unknown VLM provider: {provider_name}")
            raise ValueError(f"Unknown VLM provider: {provider_name}")

    def generate_labels(self, question: str, image: bytes) -> str:
        logger.info(f"Generating labels for image (size={len(image)} bytes)")
        logger.debug(f"Question: {question}")
        target_format = self.provider.supported_formats[0]
        logger.debug(f"Converting image to format: {target_format}")
        formatted_image = self._convert_format(image, target_format)
        logger.debug("Image format conversion complete")
        result = self.provider.generate_labels(question, formatted_image)
        logger.info("Labels generated successfully")
        return result

    def _convert_format(self, image_bytes: bytes, target_format: ImageFormat):
        """Convert image bytes to provider's preferred format."""
        logger.debug(f"Converting image to {target_format.name}")
        try:
            match target_format:
                case ImageFormat.BASE64:
                    logger.debug("Encoding image as base64")
                    return base64.b64encode(image_bytes).decode('utf-8')
                case ImageFormat.BYTES:
                    logger.debug("Using raw bytes format")
                    return image_bytes
                case ImageFormat.PIL_IMAGE:
                    logger.debug("Converting to PIL Image")
                    from PIL import Image
                    return Image.open(BytesIO(image_bytes))
                case _:
                    logger.error(f"Unknown format: {target_format}")
                    raise ValueError(f"Unknown format: {target_format}")
        except Exception as e:
            logger.error(f"Error converting image format: {e}", exc_info=True)
            raise
