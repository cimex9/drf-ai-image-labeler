from typing import Any, Union, override

from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

from app.services.vlm_provider import ImageFormat, VLMProvider


class OllamaProvider(VLMProvider):
    def __init__(self, server_url: str, model_name: str):
        self.server_url = server_url
        self.model_name = model_name
        self.client = ChatOllama(
            base_url=server_url,
            model=model_name,
            temperature=0,
        )

    @property
    @override
    def supported_formats(self) -> list[ImageFormat]:
        return [ImageFormat.BASE64]

    @override
    def generate_labels(self, question: str, image: str) -> Union[list[Any], str]:
        message = HumanMessage(
            content=[
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}},
            ]
        )
        response = self.client.invoke([message])
        return response.content
