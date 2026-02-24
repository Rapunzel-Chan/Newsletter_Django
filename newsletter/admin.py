from django.contrib import admin

# Register your models here.
from .models import AttemptMailing, Client, Mailing, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name")
    search_fields = ("email", "full_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("theme",)
    search_fields = ("theme",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "first_sending", "last_sending")
    list_filter = ("status",)
    search_fields = ("status",)
    filter_horizontal = ("clients",)


@admin.register(AttemptMailing)
class AttemptMailingAdmin(admin.ModelAdmin):
    list_display = ("mailing", "created_at", "status")
    list_filter = ("status",)
    search_fields = ("mailing__id",)
