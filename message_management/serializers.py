from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор для модели сообщений."""

    class Meta:
        model = Message
        fields = "__all__"
