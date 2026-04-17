from unittest.mock import Mock, patch

import pytest

from app.services.providers.ollama import OllamaProvider
from app.services.vlm_provider import ImageFormat


@pytest.fixture
def ollama_provider():
    with patch('app.services.providers.ollama.ChatOllama'):
        return OllamaProvider(
            server_url="http://localhost:11434",
            model_name="moondream:1.8b"
        )


def test_ollama_supported_formats(ollama_provider):
    """Ollama provider requires BASE64 format."""
    assert ollama_provider.supported_formats == [ImageFormat.BASE64]


def test_ollama_generate_labels_success(ollama_provider):
    """Ollama provider successfully generates labels."""
    mock_message = Mock()
    mock_message.content = "a cat sitting on a desk"  # format should change with new implementations
    ollama_provider.client.invoke.return_value = mock_message

    result = ollama_provider.generate_labels(
        "What do you see?",
        "YWJjZGVmCg=="  # abcdef
    )

    assert result == "a cat sitting on a desk"


def test_ollama_generate_labels_calls_client_invoke(ollama_provider):
    """Ollama provider invokes LangChain client with correct message format."""
    mock_message = Mock()
    mock_message.content = "result"
    ollama_provider.client.invoke.return_value = mock_message

    ollama_provider.generate_labels("What?", "YWJjZGVmCg==")

    ollama_provider.client.invoke.assert_called_once()
    call_args = ollama_provider.client.invoke.call_args
    messages = call_args[0][0]

    assert len(messages) == 1
    assert messages[0].content[0]["type"] == "text"
    assert messages[0].content[0]["text"] == "What?"
    assert messages[0].content[1]["type"] == "image_url"
    assert messages[0].content[1]["image_url"]["url"] == "data:image/jpeg;base64,YWJjZGVmCg=="


def test_ollama_generate_labels_handles_client_error(ollama_provider):
    """Ollama provider propagates client errors."""
    ollama_provider.client.invoke.side_effect = RuntimeError("Connection refused")

    with pytest.raises(RuntimeError):
        ollama_provider.generate_labels("What?", "YWJjZGVmCg==")
