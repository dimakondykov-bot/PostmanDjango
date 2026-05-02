from rest_framework import serializers
from .models import Recipient


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = '__all__'