from django.db import models
from base.models import BaseModel


class ContactMessage(BaseModel):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} - {self.full_name} <{self.email}>"
