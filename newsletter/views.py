from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
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


@method_decorator(login_required, name="dispatch")
class NewsletterHomeView(TemplateView):
    template_name = "newsletter/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "total_mailings": Mailing.objects.filter(owner=self.request.user).count(),
                "active_mailings": Mailing.objects.filter(owner=self.request.user, status="started").count(),
                "unique_clients": Client.objects.filter(owner=self.request.user).count(),
            }
        )
        return context


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "newsletter/client_list.html"

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "newsletter/client_detail.html"

    def get_object(self):
        obj = get_object_or_404(Client, pk=self.kwargs["pk"])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "newsletter/client_form.html"
    success_url = reverse_lazy("newsletter:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "newsletter/client_form.html"
    success_url = reverse_lazy("newsletter:client_list")

    def get_object(self):
        obj = get_object_or_404(Client, pk=self.kwargs["pk"])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "newsletter/client_confirm_delete.html"
    success_url = reverse_lazy("newsletter:client_list")

    def get_object(self):
        obj = get_object_or_404(Client, pk=self.kwargs["pk"])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "newsletter/message_list.html"

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "newsletter/message_detail.html"

    def get_object(self):
        obj = get_object_or_404(Message, pk=self.kwargs["pk"])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "newsletter/message_form.html"
    success_url = reverse_lazy("newsletter:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ["theme", "content"]
    template_name = "newsletter/message_form.html"
    success_url = reverse_lazy("newsletter:message_list")

    def get_object(self):
        obj = get_object_or_404(Message, pk=self.kwargs["pk"])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "newsletter/message_confirm_delete.html"
    success_url = reverse_lazy("newsletter:message_list")

    def get_object(self):
        obj = get_object_or_404(Message, pk=self.kwargs["pk"])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "newsletter/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.filter(owner=self.request.user).count()
        context["active_mailings"] = Mailing.objects.filter(owner=self.request.user, status="started").count()
        context["unique_clients"] = Client.objects.filter(owner=self.request.user).count()
        context["can_change_mailing"] = self.request.user.has_perm("newsletter.change_mailing")  # добавлено
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "newsletter/mailing_detail.html"

    def get_object(self):
        obj = get_object_or_404(Mailing, pk=self.kwargs["pk"])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletter/mailing_form.html"
    success_url = reverse_lazy("newsletter:mailing_list")

    def form_valid(self, form):
        form.instance.status = "created"
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = ["theme", "content"]
    template_name = "newsletter/mailing_form.html"
    success_url = reverse_lazy("newsletter:mailing_list")

    def get_object(self):
        obj = get_object_or_404(Mailing, pk=self.kwargs["pk"])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "newsletter/mailing_confirm_delete.html"
    success_url = reverse_lazy("newsletter:mailing_list")

    def get_object(self):
        obj = get_object_or_404(Mailing, pk=self.kwargs["pk"])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj


class AttemptMailingListView(LoginRequiredMixin, ListView):
    model = AttemptMailing
    template_name = "newsletter/attempt_list.html"
    context_object_name = "attempts"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return AttemptMailing.objects.all()
        return AttemptMailing.objects.filter(mailing__owner=user)


class AttemptMailingDetailView(LoginRequiredMixin, DetailView):
    model = AttemptMailing
    template_name = "newsletter/attempt_detail.html"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return AttemptMailing.objects.all()
        return AttemptMailing.objects.filter(mailing__owner=user)


from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone

from newsletter.models import Mailing


@login_required
def send_mailing(request, pk):
    if request.method != "POST":
        return redirect("newsletter:mailing_list")

    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.owner != request.user:
        raise Http404("Нет доступа")

    now = timezone.now()
    if mailing.first_sending is None:
        mailing.first_sending = now
    mailing.status = "started"
    mailing.save()

    sent, errors = 0, 0
    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.message.theme or "No Subject",
                message=mailing.message.content or "",
                from_email=None,
                recipient_list=[client.email],
                fail_silently=False,
            )
            AttemptMailing.objects.create(mailing=mailing, is_successful=True, response="OK")
            sent += 1
        except Exception as e:
            AttemptMailing.objects.create(mailing=mailing, is_successful=False, response=str(e))
            errors += 1

    if now >= mailing.last_sending:
        mailing.status = "completed"
        mailing.save()

    return redirect("newsletter:mailing_detail", pk=pk)


from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Mailing


@permission_required("newsletter.change_mailing", raise_exception=True)
def stop_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.status = "completed"
    mailing.last_sending = timezone.now()
    mailing.save()
    messages.success(request, "Рассылка успешно завершена.")
    return redirect("newsletter:mailing_list")
