from rest_framework import serializers
from .models import Mailing, MailingLog


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = '__all__'

class MailingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingLog
        fields = '__all__'