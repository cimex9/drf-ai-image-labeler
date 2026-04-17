from abc import ABC, abstractmethod
from enum import Enum


class ImageFormat(Enum):
    """Image formats providers can request."""
    BASE64 = "base64"
    BYTES = "bytes"
    PIL_IMAGE = "pil_image"


class VLMProvider(ABC):
    @property
    @abstractmethod
    def supported_formats(self) -> list[ImageFormat]:
        """Image formats this provider accepts. The first supported format is used."""

    @abstractmethod
    def generate_labels(self, question: str, image) -> str: ...
