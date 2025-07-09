from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from newsletter.models import Client, Message, Mailing


# Create your views here.


class ClientListView(ListView):
    model = Client
    template_name = 'clients/client_list.html'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/client_detail.html'


class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('clients:client_list')

class MessageListView(ListView):
    model = Message
    template_name = 'messages/message_list.html'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'messages/message_detail.html'


class MessageCreateView(CreateView):
    model = Message
    fields = '__all__'
    template_name = 'messages/message_form.html'
    success_url = reverse_lazy('messages:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = '__all__'
    template_name = 'messages/message_form.html'
    success_url = reverse_lazy('messages:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'messages/message_confirm_delete.html'
    success_url = reverse_lazy('messages:message_list')


class MailingListView(ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'


class MailingCreateView(CreateView):
    model = Mailing
    fields = '__all__'
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = '__all__'
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')
