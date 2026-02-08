from django.http import JsonResponse

from app.services import OllamaClient


def tags_view(request):
    # temp view
    client = OllamaClient()
    return JsonResponse(client.get_tags())
