from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from newsletter.models import Mailing, Message, Client


class Command(BaseCommand):
    help = "Create Managers group"

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Менеджеры")
        perms = Permission.objects.filter(
            codename__in=["view_mailing", "view_message", "view_client", "view_attemptmailing", "view_user", "change_mailing"]
        )
        group.permissions.set(perms)
        self.stdout.write("Group 'Менеджеры' initialized")
