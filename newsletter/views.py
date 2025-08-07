from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.cache import patch_cache_control
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from newsletter.forms import MailingForm, MessageForm
from newsletter.models import AttemptMailing, Client, Mailing, Message
from newsletter.services import MailingService

# Create your views here.


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "newsletter/client_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return qs
        return qs.filter(owner=self.request.user)


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
        qs = super().get_queryset()
        if self.request.user.groups.filter(name="Менеджеры").exists():
            return qs
        return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            mailings = Mailing.objects.all()
            clients = Client.objects.all()
        else:
            mailings = Mailing.objects.filter(owner=user)
            clients = Client.objects.filter(owner=user)

        context.update(
            {
                "total_mailings": mailings.count(),
                "active_mailings": mailings.filter(status="started").count(),
                "unique_clients": clients.count(),
                "can_change_mailing": user.has_perm("newsletter.change_mailing"),
            }
        )
        return context


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "newsletter/mailing_detail.html"

    def get_object(self):
        obj = get_object_or_404(Mailing, pk=self.kwargs["pk"])
        if obj.owner != self.request.user and not self.request.user.groups.filter(name="Менеджеры").exists():
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "newsletter/mailing_form.html"
    success_url = reverse_lazy("newsletter:mailing_list")

    def get_object(self):
        obj = get_object_or_404(Mailing, pk=self.kwargs["pk"])
        if obj.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этой рассылки.")
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "newsletter/mailing_confirm_delete.html"
    success_url = reverse_lazy("newsletter:mailing_list")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user

        if obj.owner != user and not user.is_superuser:
            raise Http404("Вы не можете редактировать или удалять чужую рассылку.")
        return super().dispatch(request, *args, **kwargs)


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


@login_required
def send_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    if mailing.owner != request.user:
        return HttpResponseForbidden("Вы можете отправлять только свои рассылки.")

    now = timezone.now()
    if mailing.last_sending and now < mailing.last_sending:
        messages.warning(request, f"Повторная отправка возможна не ранее чем {mailing.last_sending:%d.%m.%Y %H:%M}")
        return redirect("newsletter:mailing_detail", pk=pk)

    if not mailing.first_sending:
        mailing.first_sending = now
    mailing.status = Mailing.STATUS_CHOICES[1][0]
    mailing.save(update_fields=["first_sending", "status"])

    stats = MailingService.process_mailing(mailing)
    messages.success(request, f"Готово: отправлено {stats['sent']}, ошибок {stats['failed']}.")
    return redirect("newsletter:mailing_stats")


@permission_required("newsletter.change_mailing", raise_exception=True)
def stop_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.status = "completed"
    mailing.last_sending = timezone.now()
    mailing.save()
    messages.success(request, "Рассылка успешно завершена.")
    return redirect("newsletter:mailing_list")


class MailingStatsView(LoginRequiredMixin, TemplateView):
    template_name = "newsletter/mailing_stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_manager = user.groups.filter(name="Менеджеры").exists()

        if is_manager:
            mailings = Mailing.objects.all()
            attempts = AttemptMailing.objects.all()
            clients = Client.objects.all()
        else:
            mailings = Mailing.objects.filter(owner=user)
            attempts = AttemptMailing.objects.filter(mailing__owner=user)
            clients = Client.objects.filter(owner=user)

        context.update(
            {
                "total_mailings": mailings.count(),
                "total_clients": clients.count(),
                "successful_attempts": attempts.filter(status="success").count(),
                "failed_attempts": attempts.filter(status="failed").count(),
                "mailings": mailings,
            }
        )
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        patch_cache_control(response, private=True, max_age=300)
        return response
