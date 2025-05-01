from django.db import models
from django.urls import reverse

class Record(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    active = models.BooleanField(default=False)
    competitive = models.BooleanField(default=False)
    level = models.CharField(max_length=20, blank=True, null=True)
    challenges = models.TextField(blank=True, null=True)
    resources = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("record_detail", args=[str(self.pk)])

    def __str__(self):
        return f"{self.name} ({self.email})"