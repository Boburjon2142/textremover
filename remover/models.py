from django.db import models


class RemoveWord(models.Model):
    word = models.CharField(max_length=10000, unique=True)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.word
