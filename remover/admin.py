from django.contrib import admin
from .models import RemoveWord


@admin.register(RemoveWord)
class RemoveWordAdmin(admin.ModelAdmin):
    list_display = ("word", "active", "updated_at")
    list_editable = ("active",)
    search_fields = ("word",)
