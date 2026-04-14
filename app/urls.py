from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'labels', views.LabelViewSet)

urlpatterns = [
    path("ask/", views.AskWithImageAPIView.as_view(), name="ask"),
    path("", include(router.urls)),
]
