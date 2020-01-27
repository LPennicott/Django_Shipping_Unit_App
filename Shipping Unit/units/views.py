from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse
import datetime, csv

from .models import Shipping_Units
# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

class UnitListView(ListView):
    model = Shipping_Units
    context_object_name = 'unit_list'
    template_name = 'units/unit_list.html'
    ordering = ['-on_hand']

class UnitDetailView(DetailView):
    model = Shipping_Units
    context_object_name = 'unit'
    template_name = 'units/unit_detail.html'

class UnitUpdateView(UpdateView):
    model = Shipping_Units
    fields = ('client', 'sub_client', 'width', 'length', 'height', 'gross_weight', 'purpose',)
    template_name = 'units/unit_edit.html'

class UnitDeleteView(DeleteView):
    model = Shipping_Units
    template_name = 'units/unit_delete.html'
    success_url = reverse_lazy('unit_list')

class UnitCreateView(CreateView):
    model = Shipping_Units
    template_name = 'units/unit_new.html'
    fields = ('client', 'sub_client', 'width', 'length', 'height', 'gross_weight', 'purpose',)

class UnitReleaseView(UpdateView):
    model = Shipping_Units
    def get(self, *args, **kwargs):
        unit = self.get_object()
        unit.release_date = datetime.datetime.today()
        unit.save()
        return redirect('unit_detail', unit.pk)

class UnitReleasePage(ListView):
    model = Shipping_Units
    context_object_name = 'unit_list'
    template_name = 'units/units_release.html'
    queryset = Shipping_Units.objects.filter(release_date = None)

class UnitsReleaseView(ListView):
    model = Shipping_Units
    def post(self, request, *args, **kwargs):
        units = request.POST.getlist('onhands[]')
        released_units = Shipping_Units.objects.filter(on_hand__in = units).update(release_date = datetime.datetime.today())
        return redirect('unit_list')

class ExportListView(ListView):
    model = Shipping_Units
    context_object_name = 'unit'

    def render_to_response(self, context, **response_kwargs):
        unit = context.get('unit')
        units = unit.values_list('client', 'width', 'length', 'height', 'gross_weight', 'purpose',)
        response = HttpResponse(content_type = 'text/csv')
        response['Content-Disposition'] = 'attachment; filename = "units.csv"'
        writer = csv.writer(response)
        writer.writerow(['Client', 'Width', 'Length', 'Height', 'Gross Weight', 'Purpose'])
        for unit in units:
            writer.writerow(unit)
        return response
