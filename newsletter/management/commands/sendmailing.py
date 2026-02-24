from django.core.management.base import BaseCommand

from newsletter.models import Mailing
from newsletter.services import MailingService


class Command(BaseCommand):
    help = "Send active mailings to clients"

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status__in=["created", "started"])

        for mailing in mailings:
            stats = MailingService.process_mailing(mailing)
            self.stdout.write(f"Mailing #{mailing.pk}: {stats['sent']} sent, {stats['failed']} failed.")
