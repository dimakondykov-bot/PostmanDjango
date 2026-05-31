from rest_framework import serializers

from .models import Recipient


class RecipientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели получателей рассылки."""

    class Meta:
        model = Recipient
        fields = "__all__"
