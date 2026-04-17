import pytest

from app.services.vlm_provider import ImageFormat, VLMProvider


def test_image_format_enum_values():
    assert ImageFormat.BASE64.value == "base64"
    assert ImageFormat.BYTES.value == "bytes"
    assert ImageFormat.PIL_IMAGE.value == "pil_image"


def test_vision_language_model_is_abstract():
    """VisionLanguageModel cannot be instantiated directly."""
    with pytest.raises(TypeError):
        VLMProvider()


class ConcreteTestProvider(VLMProvider):
    @property
    def supported_formats(self):
        return [ImageFormat.BASE64]

    def generate_labels(self, question, image):
        return "test response"


def test_concrete_provider_can_be_instantiated():
    provider = ConcreteTestProvider()
    assert provider is not None


def test_concrete_provider_implements_interface():
    """Concrete provider implements required methods."""
    provider = ConcreteTestProvider()
    assert hasattr(provider, 'supported_formats')
    assert hasattr(provider, 'generate_labels')
    assert provider.supported_formats == [ImageFormat.BASE64]
    assert provider.generate_labels("test", b"image") == "test response"
