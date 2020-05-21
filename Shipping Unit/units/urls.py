from django.urls import path

from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('units/', UnitListView.as_view(), name='unit_list'),
    path('units/release/', UnitReleasePage.as_view(), name='units_release'),
    path('units/<int:pk>/edit/', UnitUpdateView.as_view(), name='unit_edit'),
    path('units/<int:pk>/delete/', UnitDeleteView.as_view(), name='unit_delete'),
    path('units/new', UnitCreateView.as_view(), name='unit_new'),
    path('units/<int:pk>/', UnitDetailView.as_view(), name='unit_detail'),
    path('units/<int:pk>/release/', UnitReleaseView.as_view(), name='unit_release'),
    path('units/released/', UnitsReleaseView.as_view(), name='units_released'),
    path('units/export/', ExportListView.as_view(), name='csv_units'),
    path('units/search/', SearchResultsListView.as_view(), name='search_results'),
    path('units/new_consol/', CreateConsolView.as_view(), name='create_consol'),
    path('units/consol/', Consolidation.as_view(), name='save_consol'),
    path('inbound/new_delivery/', new_delivery, name='new_delivery'),
    path('inbound/delivery_list/', delivery_list, name='delivery_list'),
    path('inbound/edit_delivery/<int:pk>/', edit_delivery, name='delivery_edit'),
    path('inbound/email/', email_delivery, name='email'),
]