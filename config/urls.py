from django.contrib import admin
from django.urls import path, include
import client_management
import mailing
import message_management


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clients/', include("client_management.urls")),
    path('api/message/', include("message_management.urls")),
    path('api/mailing/', include("mailing.urls")),
]
