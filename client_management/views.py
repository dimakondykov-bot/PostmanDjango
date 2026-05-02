from rest_framework import viewsets
from .models import Recipient
from .serializers import RecipientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer
