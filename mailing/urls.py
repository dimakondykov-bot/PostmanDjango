from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MailingViewSet

router = DefaultRouter()
router.register(r"mailing", MailingViewSet, basename="client")

urlpatterns = [
    path("", include(router.urls)),
]
