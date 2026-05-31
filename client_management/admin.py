from django.contrib import admin
from client_management.models import Recipient


@admin.register(Recipient)
class RecipienttAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "comment")
    list_filter = ("full_name", "email")
