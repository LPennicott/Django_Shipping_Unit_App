from django.contrib import admin
from .models import Record

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'age', 'created_at')
    list_filter = ('active', 'competitive', 'level')
    search_fields = ('name', 'email', 'phone')