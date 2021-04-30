from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    message = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.user.username
        
