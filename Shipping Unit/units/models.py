from django.db import models
from django.urls import reverse
from django.shortcuts import redirect
import datetime
# Create your models here.

class Shipping_Units(models.Model):
    on_hand = models.AutoField(
        primary_key = True,
        editable = False,
    )
    client = models.CharField(max_length = 50)
    sub_client = models.CharField(max_length = 50, null = True, blank = True)
    width = models.PositiveIntegerField()
    length = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    gross_weight = models.PositiveIntegerField()
    purpose = models.CharField(max_length = 50)
    create_date = models.DateField(auto_now_add = True)
    release_date = models.DateField(null = True, blank = True)
    hawb = models.CharField(max_length = 50, null = True, blank = True)
    mawb = models.CharField(max_length = 50, null = True, blank = True)

    class Meta:
        ordering = ('release_date',)

    def __str__(self):
        return self.client

    def get_absolute_url(self):
        return reverse('unit_detail', args = [str(self.on_hand)])
