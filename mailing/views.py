from rest_framework import viewsets
from .models import Mailing
from .serializers import MailingSerializer


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
