from django.db import models
from django.urls import reverse
# Create your models here.


class Shipping_Units(models.Model):
    STATUS_CHOICES = (
        ('Export', 'Export'),
        ('Domestic', 'Domestic'),
        ('Other', 'Other')
    )
    on_hand = models.AutoField(
        primary_key=True,
        editable=False,
    )
    client = models.CharField(max_length=50)
    sub_client = models.CharField(max_length=50, null=True, blank=True)
    width = models.PositiveIntegerField()
    length = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    gross_weight = models.PositiveIntegerField()
    purpose = models.CharField(max_length=10,
                               choices=STATUS_CHOICES,
                               default='Other')
    create_date = models.DateField(auto_now_add=True)
    release_date = models.DateField(null=True, blank=True)
    hawb = models.CharField(max_length=50, null=True, blank=True)
    mawb = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ('release_date',)
        permissions = (
                       ('can_add_shipment', 'Can add a shipping unit'),
                       ('can_modify', 'Can modify a shipment'),
                       ('can_release', 'Can release a shipment'),
                       ('can_delete', 'Can erase a shipment from existence')
                    )

    def __str__(self):
        return self.client

    def get_absolute_url(self):
        return reverse('unit_detail', args=[str(self.on_hand)])


class InboundUnits(models.Model):
    unit_count = models.PositiveIntegerField()
    date_received = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('date_received',)
        permissions = (
                       ('can_add_delivery', 'Can add delivery'),
                       ('can_edit_delivery', 'Can edit delivery')
                    )

    def __str__(self):
        return f'UPS {self.date_received} - {self.unit_count}'
