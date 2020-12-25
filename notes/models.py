from django.db import models


class Note(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    content = models.CharField(max_length=280)

    def __str__(self):
        return self.content
