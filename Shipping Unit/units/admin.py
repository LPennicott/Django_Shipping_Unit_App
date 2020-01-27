from django.contrib import admin
from .models import Shipping_Units
# Register your models here.
class UnitAdmin(admin.ModelAdmin):
    list_display = ('on_hand', 'client', 'create_date',)
    ordering = ('on_hand',)

admin.site.register(Shipping_Units, UnitAdmin)