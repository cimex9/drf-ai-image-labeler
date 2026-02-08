from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'labels', views.LabelViewSet)

urlpatterns = [
    path("tags/", views.tags_view, name="tags"),  # temp endpoint
    path("ask/", views.AskWithImageAPIView.as_view(), name="ask"),
    path("", include(router.urls)),
]
