from django.contrib import admin
from mailing.models import Mailing, MailingLog


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "end_time", "status", "message", "owner")
    list_filter = ("is_active", "start_time")


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ("mailing", "status", "attempt_at")
    readonly_fields = ("attempt_at",)
