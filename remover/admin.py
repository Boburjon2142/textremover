from django.contrib import admin
from .models import AccessLog, RemoveWord


@admin.register(RemoveWord)
class RemoveWordAdmin(admin.ModelAdmin):
    list_display = ("word", "active", "updated_at")
    list_editable = ("active",)
    search_fields = ("word",)


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ("ip_address", "input_length", "output_length", "created_at")
    search_fields = ("ip_address", "user_agent")
    readonly_fields = (
        "ip_address",
        "user_agent",
        "input_length",
        "output_length",
        "created_at",
    )
