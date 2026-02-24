from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создаёт или обновляет группу 'Менеджеры' с нужными правами"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Менеджеры")

        required_permissions = [
            # Попытка отправки
            "view_all_attempts",
            # Клиенты
            "view_client",
            "view_all_clients",
            # Рассылки
            "view_mailing",
            "view_all_mailings",
            "change_mailing",
            # Пользователи
            "view_user",
            "view_all_users",
            "can_deactivate_user",
        ]

        perms = Permission.objects.filter(codename__in=required_permissions)
        group.permissions.set(perms)

        self.stdout.write(self.style.SUCCESS(f"Группа 'Менеджеры' обновлена ({perms.count()} прав назначено)."))
