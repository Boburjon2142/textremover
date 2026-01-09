from django.db import models


class RemoveWord(models.Model):
    word = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.word
