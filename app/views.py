from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from app.filters import LabelFilter
from app.models import Image, Label
from app.serializers import AskWithImageSerializer, LabelSerializer
from app.services import OllamaClient


class LabelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "created_at"]
    filterset_class = LabelFilter
    ordering_fields = ["created_at"]


class AskWithImageAPIView(APIView):
    @swagger_auto_schema(request_body=AskWithImageSerializer)
    def post(self, request):
        serializer = AskWithImageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image_id = serializer.validated_data['image_id']
        question = serializer.validated_data['question']

        try:
            image_instance = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response(
                {"error": f"Image with id {image_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        client = OllamaClient()
        try:
            response_text = client.ask_with_image(question, image_instance.file)
            image_instance.processed_at = timezone.now()
            image_instance.save()
        except Exception as e:
            return Response(
                {"error": f"Ollama request failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            "question": question,
            "response": response_text,
            "image_id": image_instance.id
        })
