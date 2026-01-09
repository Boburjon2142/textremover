from django.db import models


class RemoveWord(models.Model):
    word = models.CharField(max_length=10000, unique=True)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Remove phrase"
        verbose_name_plural = "Remove phrases"

    def __str__(self):
        return self.word


class AccessLog(models.Model):
    ip_address = models.CharField(max_length=45, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)
    input_length = models.PositiveIntegerField(default=0)
    output_length = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} @ {self.created_at}"
