from unittest.mock import Mock, patch

import pytest

from app.services.vlm_client_service import VLMClientService
from app.services.vlm_provider import ImageFormat


@pytest.fixture
def ollama_settings(settings):
    settings.VLM_PROVIDER = 'ollama'
    settings.VLM_MODEL = 'moondream:1.8b'
    settings.OLLAMA_SERVER_URL = 'http://localhost:11434'
    return settings


class TestVLMClientServiceFlows:
    """Tests for the full VLM processing flow."""

    def test_full_flow_bytes_to_ollama(self, ollama_settings):
        with patch('app.services.providers.ollama.ChatOllama'):
            service = VLMClientService('ollama', 'moondream:1.8b')

            mock_message = Mock()
            mock_message.content = 'golden retriever'
            service.provider.client.invoke.return_value = mock_message

            result = service.generate_labels("What breed?", b"fake jpeg data")

            assert result == 'golden retriever'

    def test_full_flow_bytes_to_base64_conversion(self, ollama_settings):
        with patch('app.services.providers.ollama.ChatOllama'):
            service = VLMClientService('ollama', 'moondream:1.8b')

            mock_message = Mock()
            mock_message.content = 'test response'
            service.provider.client.invoke.return_value = mock_message

            service.generate_labels("Describe this", b"image content")

            service.provider.client.invoke.assert_called_once()
            call_args = service.provider.client.invoke.call_args
            messages = call_args[0][0]

            assert len(messages) == 1
            assert messages[0].content[1]["type"] == "image_url"
            base64_url = messages[0].content[1]["image_url"]["url"]
            assert base64_url == "data:image/jpeg;base64,aW1hZ2UgY29udGVudA=="

    def test_full_flow_preserves_question(self, ollama_settings):
        with patch('app.services.providers.ollama.ChatOllama'):
            service = VLMClientService('ollama', 'moondream:1.8b')

            mock_message = Mock()
            mock_message.content = 'answer'
            service.provider.client.invoke.return_value = mock_message

            question = "What is in this image?"
            service.generate_labels(question, b"test")

            call_args = service.provider.client.invoke.call_args
            messages = call_args[0][0]

            assert messages[0].content[0]["text"] == question

    def test_full_flow_with_file_object(self, ollama_settings):
        with patch('app.services.providers.ollama.ChatOllama'):
            service = VLMClientService('ollama', 'moondream:1.8b')

            mock_message = Mock()
            mock_message.content = 'result'
            service.provider.client.invoke.return_value = mock_message

            result = service.generate_labels("Query", b"file content")

            assert result == 'result'

    def test_full_flow_with_raw_bytes(self, ollama_settings):
        with patch('app.services.providers.ollama.ChatOllama'):
            service = VLMClientService('ollama', 'moondream:1.8b')

            mock_message = Mock()
            mock_message.content = 'result'
            service.provider.client.invoke.return_value = mock_message

            result = service.generate_labels("Query", b"raw bytes")

            assert result == 'result'

    def test_full_flow_error_propagation(self, ollama_settings):
        with patch('app.services.providers.ollama.ChatOllama'):
            service = VLMClientService('ollama', 'moondream:1.8b')
            service.provider.client.invoke.side_effect = RuntimeError("Connection error")

            with pytest.raises(RuntimeError, match="Connection error"):
                service.generate_labels("Query", b"data")


class TestSingletonInitialization:
    def test_get_vlm_service_creates_instance(self, ollama_settings):
        from app.services import vlm_client_service

        vlm_client_service._vlm_service_instance = None

        with patch('app.services.providers.ollama.ChatOllama'):
            service = vlm_client_service.get_vlm_service()
            assert service is not None
            assert service.provider is not None
            assert service.provider.model_name == 'moondream:1.8b'

    def test_get_vlm_service_returns_singleton(self, ollama_settings):
        from app.services import vlm_client_service

        vlm_client_service._vlm_service_instance = None

        with patch('app.services.providers.ollama.ChatOllama'):
            service1 = vlm_client_service.get_vlm_service()
            service2 = vlm_client_service.get_vlm_service()

            assert service1 is service2

    def test_get_vlm_service_uses_correct_settings(self, ollama_settings):
        from app.services import vlm_client_service

        vlm_client_service._vlm_service_instance = None

        with patch('app.services.providers.ollama.ChatOllama'):
            service = vlm_client_service.get_vlm_service()

            assert service.provider.server_url == 'http://localhost:11434'
            assert service.provider.model_name == 'moondream:1.8b'


class TestFormatConversionInFlow:
    def test_format_conversion_base64_in_flow(self, ollama_settings):
        """Test that format conversion to BASE64 happens in the flow."""
        service = VLMClientService('ollama', 'moondream:1.8b')

        assert service.provider.supported_formats == [ImageFormat.BASE64]

        image_bytes = b"test image"
        formatted = service._convert_format(image_bytes, ImageFormat.BASE64)

        assert isinstance(formatted, str)
        assert formatted == "dGVzdCBpbWFnZQ=="

    def test_provider_receives_correct_format(self, ollama_settings):
        service = VLMClientService('ollama', 'moondream:1.8b')

        mock_provider = Mock()
        mock_provider.supported_formats = [ImageFormat.BASE64]
        mock_provider.generate_labels.return_value = "label"
        service.provider = mock_provider

        service.generate_labels("Question", b"test")

        # provider should be called with BASE64 string
        call_args = mock_provider.generate_labels.call_args
        assert call_args[0][0] == "Question"
        # second argument should be BASE64 string
        assert isinstance(call_args[0][1], str)
