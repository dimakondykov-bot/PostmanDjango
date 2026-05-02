from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mailing.views import MailingViewSet
from .views import MessageViewSet


router = DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]