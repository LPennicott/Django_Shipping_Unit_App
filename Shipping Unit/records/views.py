from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Record
from .forms import RecordForm

class RecordListView(ListView):
    model = Record
    context_object_name = 'records'
    template_name = 'records/record_list.html'

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
    success_url = reverse_lazy('record_list')