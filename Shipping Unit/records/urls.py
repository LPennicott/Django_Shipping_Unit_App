from django.urls import path
from .views import *

urlpatterns = [
    path('', RecordListView.as_view(), name='home'),
    path('record/<int:pk>/', RecordDetailView.as_view(), name='record_detail'),
    path('record/new/', RecordCreateView.as_view(), name='record_new'),
    path('record/<int:pk>/edit/', RecordUpdateView.as_view(), name='record_edit'),
    path('record/<int:pk>/delete/',
         RecordDeleteView.as_view(), name='record_delete'),
    path('export/', export_records_csv, name='export_records_csv'),
]
