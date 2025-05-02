import csv
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Record
from .forms import RecordForm


class RecordHomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        records = Record.objects.all()
        context["records"] = records
        context["total_records"] = records.count()
        context["active_count"] = records.filter(active=True).count()
        context["competitive_count"] = records.filter(competitive=True).count()
        return context


class RecordListView(ListView):
    model = Record
    template_name = 'records/record_list.html'
    context_object_name = 'records'

    def get_queryset(self):
        qs = super().get_queryset()

        active = self.request.GET.get('active')
        competitive = self.request.GET.get('competitive')

        if active == 'true':
            qs = qs.filter(active=True)
        elif active == 'false':
            qs = qs.filter(active=False)

        if competitive == 'true':
            qs = qs.filter(competitive=True)
        elif competitive == 'false':
            qs = qs.filter(competitive=False)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context["total_records"] = qs.count()
        context["active_count"] = qs.filter(active=True).count()
        context["competitive_count"] = qs.filter(competitive=True).count()
        return context


class RecordDetailView(DetailView):
    model = Record
    context_object_name = 'record'
    template_name = 'records/record_detail.html'


class RecordCreateView(CreateView):
    model = Record
    form_class = RecordForm
    template_name = 'records/record_form.html'


class RecordUpdateView(UpdateView):
    model = Record
    form_class = RecordForm
    template_name = 'records/record_form.html'


class RecordDeleteView(DeleteView):
    model = Record
    template_name = 'records/record_confirm_delete.html'
    success_url = reverse_lazy('home')


def export_records_csv(request):
    active = request.GET.get('active')
    competitive = request.GET.get('competitive')

    records = Record.objects.all()

    if active == 'true':
        records = records.filter(active=True)
    elif active == 'false':
        records = records.filter(active=False)

    if competitive == 'true':
        records = records.filter(competitive=True)
    elif competitive == 'false':
        records = records.filter(competitive=False)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_records.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Name', 'Email', 'Phone', 'Age', 'Active', 'Competitive',
        'Level', 'Challenges', 'Resources', 'Recommendations', 'Created At'
    ])

    for record in records:
        writer.writerow([
            record.name,
            record.email,
            record.phone,
            record.age,
            record.active,
            record.competitive,
            record.level,
            record.challenges,
            record.resources,
            record.recommendations,
            record.created_at.strftime('%Y-%m-%d %H:%M'),
        ])

    return response
