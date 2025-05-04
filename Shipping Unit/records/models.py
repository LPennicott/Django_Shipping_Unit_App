from django.db import models
from django.urls import reverse


class Record(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    age = models.PositiveIntegerField(verbose_name="Child's Age")

    active = models.BooleanField(
        default=False, verbose_name="Is your child currently in gymnastics?")
    home_gym = models.CharField(max_length=100, verbose_name="Home Gym?")
    competitive = models.BooleanField(
        default=False, verbose_name="Do they compete in competitions?")
    level = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Competitive Level (Level/Xcel/IGH)"
    )

    challenges = models.CharField(
        max_length=255, blank=True, verbose_name="Challenges Faced")
    resources = models.CharField(
        max_length=255, blank=True, verbose_name="Helpful Resources")
    recommendations = models.CharField(
        max_length=255, blank=True, verbose_name="Recommendations")

    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("records:record_detail", args=[str(self.pk)])

    def __str__(self):
        return f"{self.name} ({self.email})"
