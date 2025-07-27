from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from newsletter.forms import MailingForm, MessageForm
from newsletter.models import Client, Message, Mailing, AttemptMailing


# Create your views here.


# class NewsletterHomeView(TemplateView):
#     template_name = 'newsletter/home.html'

@method_decorator(login_required, name='dispatch')
class NewsletterHomeView(TemplateView):
    template_name = 'newsletter/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_mailings': Mailing.objects.filter(owner=self.request.user).count(),
            'active_mailings': Mailing.objects.filter(owner=self.request.user, status='started').count(),
            'unique_clients': Client.objects.filter(owner=self.request.user).count(),
        })
        return context

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'newsletter/client_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'newsletter/client_detail.html'

    def get_object(self):
        obj = get_object_or_404(Client, pk=self.kwargs['pk'])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'newsletter/client_form.html'
    success_url = reverse_lazy('newsletter:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'newsletter/client_form.html'
    success_url = reverse_lazy('newsletter:client_list')

    def get_object(self):
        obj = get_object_or_404(Client, pk=self.kwargs['pk'])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'newsletter/client_confirm_delete.html'
    success_url = reverse_lazy('newsletter:client_list')

    def get_object(self):
        obj = get_object_or_404(Client, pk=self.kwargs['pk'])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'newsletter/message_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'newsletter/message_detail.html'

    def get_object(self):
        obj = get_object_or_404(Message, pk=self.kwargs['pk'])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'newsletter/message_form.html'
    success_url = reverse_lazy('newsletter:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = '__all__'
    template_name = 'newsletter/message_form.html'
    success_url = reverse_lazy('newsletter:message_list')

    def get_object(self):
        obj = get_object_or_404(Message, pk=self.kwargs['pk'])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'newsletter/message_confirm_delete.html'
    success_url = reverse_lazy('newsletter:message_list')

    def get_object(self):
        obj = get_object_or_404(Message, pk=self.kwargs['pk'])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'newsletter/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_mailings'] = Mailing.objects.filter(owner=self.request.user).count()
        context['active_mailings'] = Mailing.objects.filter(owner=self.request.user, status='started').count()
        context['unique_clients'] = Client.objects.filter(owner=self.request.user).count()
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'newsletter/mailing_detail.html'

    def get_object(self):
        obj = get_object_or_404(Mailing, pk=self.kwargs['pk'])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'newsletter/mailing_form.html'
    success_url = reverse_lazy('newsletter:mailing_list')

    def form_valid(self, form):
        form.instance.status = 'created'
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = '__all__'
    template_name = 'newsletter/mailing_form.html'
    success_url = reverse_lazy('newsletter:mailing_list')

    def get_object(self):
        obj = get_object_or_404(Mailing, pk=self.kwargs['pk'])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'newsletter/mailing_confirm_delete.html'
    success_url = reverse_lazy('newsletter:mailing_list')

    def get_object(self):
        obj = get_object_or_404(Mailing, pk=self.kwargs['pk'])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class AttemptMailingListView(LoginRequiredMixin, ListView):
    model = AttemptMailing
    template_name = 'newsletter/attempt_list.html'
    context_object_name = 'attempts'


class AttemptMailingDetailView(LoginRequiredMixin, DetailView):
    model = AttemptMailing
    template_name = 'newsletter/attempt_detail.html'
