from django.urls import path

from .views import (
        HomePageView,
        UnitListView,
        UnitReleasePage,
        UnitUpdateView,
        UnitDeleteView,
        UnitCreateView,
        UnitDetailView,
        UnitReleaseView,
        UnitsReleaseView,
        ExportListView,
        SearchResultsListView,
        CreateConsolView,
        Consolidation,
    )

urlpatterns = [
    path('', HomePageView.as_view(), name = 'home'),
    path('units/', UnitListView.as_view(), name = 'unit_list'),
    path('units/release/', UnitReleasePage.as_view(), name = 'units_release'),
    path('units/<int:pk>/edit/', UnitUpdateView.as_view(), name = 'unit_edit'),
    path('units/<int:pk>/delete/', UnitDeleteView.as_view(), name = 'unit_delete'),
    path('units/new', UnitCreateView.as_view(), name = 'unit_new'),
    path('units/<int:pk>/', UnitDetailView.as_view(), name = 'unit_detail'),
    path('units/<int:pk>/release/', UnitReleaseView.as_view() , name = 'unit_release'),
    path('units/released/', UnitsReleaseView.as_view(), name ='units_released'),
    path('units/export/', ExportListView.as_view(), name = 'csv_units'),
    path('units/search/', SearchResultsListView.as_view(), name = 'search_results'),
    path('units/new_consol/', CreateConsolView.as_view(), name = 'create_consol'),
    path('units/consol/', Consolidation.as_view(), name = 'save_consol'),
]