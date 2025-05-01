from django import template
from django.db.models import Sum
from ..models import Shipping_Units, InboundUnits

import datetime

register = template.Library()

@register.simple_tag
def unit_count():
    return Shipping_Units.objects.filter(release_date = None).count()

@register.simple_tag
def released_count():
    return Shipping_Units.objects.exclude(release_date = None).count()

@register.simple_tag
def in_house_weight():
	total_weight = Shipping_Units.objects.filter(release_date = None).aggregate(Sum('gross_weight'))
	return total_weight['gross_weight__sum']

@register.simple_tag
def today_delivery():
    total = InboundUnits.objects.filter(date_received = datetime.datetime.today()).aggregate(Sum('unit_count'))
    return total['unit_count__sum']