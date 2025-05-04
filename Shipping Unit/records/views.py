import csv
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
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
    template_name = 'records/record_list_with_edit_modal.html'
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
        context["form"] = RecordForm()
        return context


class RecordDetailView(DetailView):
    model = Record
    template_name = 'records/partials/detail_modal.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(self.template_name, {
                                    'record': self.object}, request=request)
            return JsonResponse({'html': html})
        return super().get(request, *args, **kwargs)


class RecordCreateView(CreateView):
    model = Record
    form_class = RecordForm
    template_name = 'records/record_form_modal.html'  # fallback
    success_url = reverse_lazy('record_list')

    def get(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data()

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                'records/partials/create_form.html', context, request=request)
            return JsonResponse({'html': html})

        return self.render_to_response(context)

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({'success': True})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                'records/partials/create_form.html', {'form': form}, request=self.request)
            return JsonResponse({'success': False, 'html': html})
        return super().form_invalid(form)


class RecordUpdateView(UpdateView):
    model = Record
    form_class = RecordForm
    template_name = 'records/record_form_modal.html'
    success_url = reverse_lazy('records:record_list')


class RecordDeleteView(DeleteView):
    model = Record
    success_url = reverse_lazy('records:record_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True, "id": self.object.pk})

        return super().delete(request, *args, **kwargs)


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
