from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import datetime, csv

from .models import Shipping_Units, InboundUnits
from .forms import InboundForm


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'


class UnitListView(LoginRequiredMixin, ListView):
    model = Shipping_Units
    context_object_name = 'unit_list'
    template_name = 'units/unit_list.html'
    ordering = ['-on_hand']
    login_url = 'account_login'


class UnitDetailView(LoginRequiredMixin, DetailView):
    model = Shipping_Units
    context_object_name = 'unit'
    template_name = 'units/unit_detail.html'
    login_url = 'account_login'


class UnitUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Shipping_Units
    fields = (
        'client', 'sub_client', 'width', 'length',
        'height', 'gross_weight', 'purpose',
    )
    template_name = 'units/unit_edit.html'
    login_url = 'account_login'
    permission_required = ('units.can_modify')


class UnitDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Shipping_Units
    template_name = 'units/unit_delete.html'
    success_url = reverse_lazy('unit_list')
    login_url = 'account_login'
    permission_required = ('units.can_modify')


class UnitCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Shipping_Units
    template_name = 'units/unit_new.html'
    fields = (
        'client', 'sub_client', 'width', 'length',
        'height', 'gross_weight', 'purpose',
    )
    login_url = 'account_login'
    permission_required = ('units.can_add_shipment')


class UnitReleaseView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Shipping_Units
    login_url = 'account_login'
    permission_required = ('units.can_modify')

    def get(self, *args, **kwargs):
        unit = self.get_object()
        unit.release_date = datetime.datetime.today()
        unit.save()
        return redirect('unit_detail', unit.pk)


class UnitReleasePage(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Shipping_Units
    context_object_name = 'unit_list'
    template_name = 'units/units_release.html'
    queryset = Shipping_Units.objects.filter(release_date=None)
    login_url = 'account_login'
    permission_required = ('units.can_modify')


class UnitsReleaseView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Shipping_Units
    login_url = 'account_login'
    permission_required = ('units.can_modify')

    def post(self, request, *args, **kwargs):
        units = request.POST.getlist('onhands[]')
        Shipping_Units.objects.filter(on_hand__in=units)\
            .update(release_date=datetime.datetime.today())
        return redirect('unit_list')


class ExportListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Shipping_Units
    context_object_name = 'unit'
    queryset = Shipping_Units.objects.filter(
        release_date=datetime.datetime.today())
    login_url = 'account_login'
    permission_required = ('units.can_modify')

    def render_to_response(self, context, **response_kwargs):
        unit = context.get('unit')
        units = unit.values_list(
            'client',
            'width',
            'length',
            'height',
            'gross_weight',
            'purpose',
        )
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename = "units.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Client',
            'Width',
            'Length',
            'Height',
            'Gross Weight',
            'Purpose'
        ])
        for unit in units:
            writer.writerow(unit)
        return response


class SearchResultsListView(LoginRequiredMixin, ListView):
    model = Shipping_Units
    context_object_name = 'unit_list'
    template_name = 'units/search_results.html'
    ordering = ['-on_hand']
    login_url = 'account_login'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Shipping_Units.objects.filter(
            Q(client__icontains=query) | Q(on_hand__contains=query) | Q(purpose__icontains=query) |\
            Q(mawb__icontains=query) | Q(hawb__icontains=query)
        )


class CreateConsolView(LoginRequiredMixin, ListView):
    model = Shipping_Units
    context_object_name = 'unit_list'
    template_name = 'units/consolidation.html'
    queryset = Shipping_Units.objects.exclude(release_date=None)\
    .filter(mawb=None, purpose='Export')
    login_url = 'account_login'


class Consolidation(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Shipping_Units
    login_url = 'account_login'
    permission_required = ('units.can_edit_delivery')

    def post(self, request, *args, **kwargs):
        units = request.POST.getlist('onhands[]')
        mawb = request.POST.get('mawb')
        hawb = request.POST.get('hawb')
        Shipping_Units.objects.filter(on_hand__in=units).update(mawb=mawb)
        Shipping_Units.objects.filter(on_hand__in=units).update(hawb=hawb)
        return redirect('unit_list')


@login_required
def delivery_list(request):
    deliveries = InboundUnits.objects.order_by('-date_received', 'pk')
    return render(
        request,
        'inbound/delivery_list.html',
        {'deliveries': deliveries}
    )


@permission_required('units.can_add_delivery')
@login_required
def new_delivery(request):
    if request.method == 'POST':
        form = InboundForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/inbound/delivery_list/')
    else:
        form = InboundForm()
    return render(request, 'inbound/new_delivery.html', {'form': form})


@permission_required('units.can_edit_delivery')
@login_required
def edit_delivery(request, pk):
    record = get_object_or_404(InboundUnits, pk=pk)
    if request.method == 'POST':
        form = InboundForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('/inbound/delivery_list/')
    else:
        form = InboundForm(instance=record)
    return render(
        request,
        'inbound/edit_delivery.html',
        {'form': form, 'record': record}
    )


@permission_required('units.can_edit_delivery')
@login_required
def email_delivery(request):
    total = InboundUnits.objects.filter(
        date_received=datetime.datetime.today()).aggregate(Sum('unit_count')
    )
    sum_delivery = total['unit_count__sum']
    subject = f'Pallets Received {datetime.datetime.today().strftime("%Y-%m-%d")}'
    message = f'Good Afternoon,\n\nWe received {sum_delivery} pallets today.'
    email_from = 'ACPShipping_Unit@aircitypost.com'
    recipient_list = [
        'lpennicott@aircitypost.com',
        'JRalph@aircitypost.com',
        'SMasterson@aircitypost.com',
        'NCraigen@aircitypost.com'
    ]
    send_mail(subject, message, email_from, recipient_list)
    return redirect('/inbound/delivery_list/')
