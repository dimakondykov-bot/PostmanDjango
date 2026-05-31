from rest_framework import serializers

from .models import Mailing, MailingLog


class MailingSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source="status")

    class Meta:
        model = Mailing
        fields = "__all__"
        read_only_fields = ("owner", "is_active")


class MailingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingLog
        fields = "__all__"
