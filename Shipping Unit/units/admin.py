from django.contrib import admin
from .models import Shipping_Units, InboundUnits
# Register your models here.
class UnitAdmin(admin.ModelAdmin):
    list_display = ('on_hand', 'client', 'create_date',)
    ordering = ('on_hand',)

class InboundUnitAdmin(admin.ModelAdmin):
    list_display = ('unit_count', 'date_received',)
    ordering = ('date_received',)

admin.site.register(Shipping_Units, UnitAdmin)
admin.site.register(InboundUnits, InboundUnitAdmin)