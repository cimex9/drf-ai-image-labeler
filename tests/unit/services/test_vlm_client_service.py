from io import BytesIO
from unittest.mock import Mock

import pytest
from PIL import Image

from app.services.vlm_client_service import VLMClientService, get_vlm_service
from app.services.vlm_provider import ImageFormat


class TestVLMClientServiceFactory:
    @pytest.fixture(autouse=True)
    def setup(self, settings):
        settings.VLM_PROVIDER = 'ollama'
        settings.VLM_MODEL = 'moondream:1.8b'
        settings.OLLAMA_SERVER_URL = 'http://localhost:11434'

    def test_create_ollama_provider(self):
        service = VLMClientService('ollama', 'moondream:1.8b')
        assert service.provider is not None
        assert service.provider.supported_formats == [ImageFormat.BASE64]

    def test_create_unknown_provider_raises_error(self):
        with pytest.raises(ValueError, match="Unknown VLM provider"):
            VLMClientService('unknown_provider', 'model:latest')


class TestFormatConversion:
    @pytest.fixture(autouse=True)
    def setup(self, settings):
        settings.VLM_PROVIDER = 'ollama'
        settings.VLM_MODEL = 'moondream:1.8b'
        settings.OLLAMA_SERVER_URL = 'http://localhost:11434'

    @pytest.fixture
    def service(self):
        return VLMClientService('ollama', 'moondream:1.8b')

    def test_convert_to_base64(self, service):
        result = service._convert_format(b"fake image data", ImageFormat.BASE64)
        assert isinstance(result, str)
        assert result == "ZmFrZSBpbWFnZSBkYXRh"

    def test_convert_to_bytes(self, service):
        image_bytes = b"fake image data"
        result = service._convert_format(image_bytes, ImageFormat.BYTES)
        assert result == image_bytes

    def test_convert_to_pil_image(self, service):
        img = Image.new('RGB', (10, 10), color='red')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        image_bytes = img_bytes.getvalue()

        result = service._convert_format(image_bytes, ImageFormat.PIL_IMAGE)
        assert isinstance(result, Image.Image)

    def test_convert_unknown_format_raises_error(self, service):
        mock_format = type('MockFormat', (), {'value': 'unknown', 'name': 'unknown'})()
        with pytest.raises(ValueError, match="Unknown format"):
            service._convert_format(b"data", mock_format)


class TestGenerateLabels:
    @pytest.fixture(autouse=True)
    def setup(self, settings):
        settings.VLM_PROVIDER = 'ollama'
        settings.VLM_MODEL = 'moondream:1.8b'
        settings.OLLAMA_SERVER_URL = 'http://localhost:11434'

    @pytest.fixture
    def service(self):
        return VLMClientService('ollama', 'moondream:1.8b')

    @pytest.fixture
    def mock_provider(self):
        provider = Mock()
        provider.supported_formats = [ImageFormat.BASE64]
        provider.generate_labels.return_value = "cat"
        return provider

    def test_with_raw_bytes(self, service, mock_provider):
        service.provider = mock_provider
        result = service.generate_labels("What is this?", b"image data")

        assert result == "cat"
        call_args = mock_provider.generate_labels.call_args
        assert call_args[0][0] == "What is this?"
        assert isinstance(call_args[0][1], str)

    def test_end_to_end(self, service, mock_provider):
        service.provider = mock_provider
        result = service.generate_labels("What is this?", b"image data")

        assert result == "cat"
        mock_provider.generate_labels.assert_called_once()
        call_args = mock_provider.generate_labels.call_args
        assert call_args[0][0] == "What is this?"
        assert isinstance(call_args[0][1], str)
