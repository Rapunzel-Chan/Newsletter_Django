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

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# @method_decorator(cache_page(60 * 15), name='dispatch')
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

        context.update({
            "total_mailings": mailings.count(),
            "active_mailings": mailings.filter(status="started").count(),
            "unique_clients": clients.count(),
            "can_change_mailing": user.has_perm("newsletter.change_mailing")
        })
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

    # def get_object(self):
    #     obj = get_object_or_404(Mailing, pk=self.kwargs["pk"])
    #     if obj.owner != self.request.user:
    #         raise Http404("Вы не являетесь владельцем этой рассылки.")
    #     return obj
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user

        if obj.owner != user and not user.is_superuser:
            # даже менеджер не может
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


from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.utils import timezone

from newsletter.models import Mailing


# @login_required
# def send_mailing(request, pk):
#     if request.method != "POST":
#         return redirect("newsletter:mailing_list")
#
#     mailing = get_object_or_404(Mailing, pk=pk)
#     if mailing.owner != request.user:
#         raise Http404("Нет доступа")
#
#     now = timezone.now()
#     if mailing.first_sending is None:
#         mailing.first_sending = now
#     mailing.status = "started"
#     mailing.save(update_fields=["status", "first_sending"])
#
#     sent, errors = 0, 0
#     for client in mailing.clients.all():
#         try:
#             send_mail(
#                 subject=mailing.message.theme or "No Subject",
#                 message=mailing.message.content or "",
#                 from_email=None,
#                 recipient_list=[client.email],
#                 fail_silently=False,
#             )
#             AttemptMailing.objects.create(mailing=mailing, status = "success", response="OK")
#             sent += 1
#         except Exception as e:
#             AttemptMailing.objects.create(mailing=mailing, status = "failed", response=str(e))
#             errors += 1
#
#     if mailing.last_sending is not None and now < mailing.last_sending:
#         messages.warning(request, "Отправку нельзя запускать ранее предыдущей")
#         return redirects
#     else:
#         mailing.status = "completed"
#         mailing.save()
#         mailing.mark_completed()
#     return redirect("newsletter:mailing_detail", pk=pk)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.http import HttpResponseForbidden

from newsletter.models import Mailing, AttemptMailing

@login_required
def send_mailing(request, pk):
    if request.method != "POST":
        return redirect("newsletter:mailing_list")

    mailing = get_object_or_404(Mailing, pk=pk)
    user = request.user

    # — только владелец может запускать рассылку
    if mailing.owner_id != user.id:
        return HttpResponseForbidden("Вы можете отправлять только свои рассылки.")

    now = timezone.now()
    if mailing.last_sending and now < mailing.last_sending:
        messages.warning(request,
                         f"Повторная отправка возможна не ранее чем {mailing.last_sending:%d.%m.%Y %H:%M}")
        return redirect("newsletter:mailing_detail", pk=pk)

    # первая отправка
    if not mailing.first_sending:
        mailing.first_sending = now
    mailing.status = Mailing.STATUS_CHOICES[1][0]  # "started"
    mailing.save(update_fields=["first_sending", "status"])

    sent = failed = 0
    for client in mailing.clients.all():
        try:
            send_mail(
                subject=mailing.message.theme or "Без темы",
                message=mailing.message.content or "",
                from_email=None,  # используется DEFAULT_FROM_EMAIL
                recipient_list=[client.email],
                fail_silently=False,
            )
        except Exception as exc:
            AttemptMailing.objects.create(
                mailing=mailing,
                status='failed',
                response=str(exc)[: 200]  # обрезаем слишком длинный ответ
            )
            failed += 1
        else:
            AttemptMailing.objects.create(
                mailing=mailing,
                status='success',
                response="OK"
            )
            sent += 1

    # пост‑обработка
    # mailing.status = Mailing.STATUS_CHOICES[2][0]  # "completed"
    mailing.last_sending = timezone.now()
    mailing.save(update_fields=["status", "last_sending"])

    # mailing.mark_completed()  # также сохраняет status + last_sending
    messages.success(request, f"Готово: отправлено {sent}, ошибок {failed}.")

    return redirect("newsletter:mailing_stats", pk=pk)



from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages, redirects
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

from django.views.generic import DetailView
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Mailing, AttemptMailing

# class MailingStatsView(LoginRequiredMixin, DetailView):
#     model = Mailing
#     template_name = "newsletter/mailing_stats.html"
#     context_object_name = "mailing"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mailing = self.get_object()
#
#         if mailing.owner != self.request.user and not self.request.user.groups.filter(name="Менеджеры").exists():
#             raise Http404
#         else:
#
#             stats = AttemptMailing.objects.filter(mailing=mailing).aggregate(
#             total=Count("id"),
#             success=Count("id", filter=Q(status="success")),
#             failed=Count("id", filter=Q(status="failed")),
#         )
#             context["stats"] = stats
#             context["attempts"] = AttemptMailing.objects.filter(mailing=mailing).order_by("-created_at")
#             return context

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.http import condition
from django.views.generic import TemplateView
from django.utils.cache import patch_cache_control

# @method_decorator(cache_page(60 * 5), name='dispatch')
# class NewsletterStatisticsView(TemplateView):
#     template_name = "newsletter/statistics.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['total_subscribers'] = Subscriber.objects.count()
#         context['sent_emails'] = SentEmail.objects.count()
#         return context
#
#     def render_to_response(self, context, **response_kwargs):
#         response = super().render_to_response(context, **response_kwargs)
#         patch_cache_control(response, public=True, max_age=300)  # клиентское кеширование на 5 минут
#         return response
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page

from newsletter.models import Mailing, AttemptMailing, Client


from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from newsletter.models import Mailing, AttemptMailing, Client

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

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

        context.update({
            "total_mailings": mailings.count(),
            "total_clients": clients.count(),
            "successful_attempts": attempts.filter(status="success").count(),
            "failed_attempts": attempts.filter(status="failed").count(),
            "mailings": mailings,
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        # Кешируем клиентски на 5 минут (300 секунд), только в браузере (private)
        patch_cache_control(response, private=True, max_age=300)
        return response
