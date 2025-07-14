from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from newsletter.forms import MailingForm, MessageForm
from newsletter.models import Client, Message, Mailing, AttemptMailing


# Create your views here.


# class NewsletterHomeView(TemplateView):
#     template_name = 'newsletter/home.html'


class ClientListView(ListView):
    model = Client
    template_name = 'newsletter/client_list.html'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'newsletter/client_detail.html'


class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'newsletter/client_form.html'
    success_url = reverse_lazy('newsletter:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'newsletter/client_form.html'
    success_url = reverse_lazy('newsletter:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'newsletter/client_confirm_delete.html'
    success_url = reverse_lazy('newsletter:client_list')

class MessageListView(ListView):
    model = Message
    template_name = 'newsletter/message_list.html'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'newsletter/message_detail.html'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'newsletter/message_form.html'
    success_url = reverse_lazy('newsletter:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = '__all__'
    template_name = 'newsletter/message_form.html'
    success_url = reverse_lazy('newsletter:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'newsletter/message_confirm_delete.html'
    success_url = reverse_lazy('newsletter:message_list')


class MailingListView(ListView):
    model = Mailing
    template_name = 'newsletter/mailing_list.html'
    context_object_name = 'mailings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.count()
        context['active_mailings'] = Mailing.objects.filter(status='started').count()
        context['unique_clients'] = Client.objects.count()
        return context


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'newsletter/mailing_detail.html'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'newsletter/mailing_form.html'
    success_url = reverse_lazy('newsletter:mailing_list')

    def form_valid(self, form):
        form.instance.status = 'created'
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = '__all__'
    template_name = 'newsletter/mailing_form.html'
    success_url = reverse_lazy('newsletter:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'newsletter/mailing_confirm_delete.html'
    success_url = reverse_lazy('newsletter:mailing_list')


class AttemptMailingListView(ListView):
    model = AttemptMailing
    template_name = 'newsletter/attempt_list.html'
    context_object_name = 'attempts'


class AttemptMailingDetailView(DetailView):
    model = AttemptMailing
    template_name = 'newsletter/attempt_detail.html'
