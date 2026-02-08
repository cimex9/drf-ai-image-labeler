from django.urls import path
from . import views


urlpatterns = [
    path("tags/", views.tags_view, name="tags"),  # temp endpoint
]
