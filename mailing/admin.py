from django.contrib import admin
from mailing.models import Mailing, MailingLog

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('started_at', 'status', 'message')
    list_filter = ('status',)

@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'status', 'attempt_at')
    readonly_fields = ('attempt_at',)
