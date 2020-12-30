from django.db import models
from django.conf import settings


class Note(models.Model):
    timestamp = models.DateTimeField(auto_now=True, blank=True)
    content = models.CharField(max_length=280)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
