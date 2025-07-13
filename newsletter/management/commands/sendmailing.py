from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from newsletter.models import Mailing, AttemptMailing


class Command(BaseCommand):
    help = "Send active mailings to clients"

    def handle(self, *args, **options):
        now = timezone.now()
        mailings = Mailing.objects.filter(status__in=['created', 'started'], first_sending__lte=now,
                                          last_sending__gte=now)

        for mailing in mailings:
            if mailing.status == 'created':
                mailing.status = 'started'
                mailing.save()
                self.stdout.write(f"Mailing #{mailing.pk} started.")

            message = mailing.message
            for client in mailing.clients.all():
                try:
                    send_mail(
                        subject=message.theme or "No Subject",
                        message=message.content or "",
                        from_email=None,  # Используется DEFAULT_FROM_EMAIL
                        recipient_list=[client.email],
                        fail_silently=False,
                    )
                    AttemptMailing.objects.create(mailing=mailing, is_successful=True, response="OK")
                    self.stdout.write(f"Email sent to {client.email}")
                except Exception as e:
                    AttemptMailing.objects.create(mailing=mailing, is_successful=False, response=str(e))
                    self.stderr.write(f"Failed to send email to {client.email}: {e}")

            if now >= mailing.last_sending:
                mailing.status = 'completed'
                mailing.save()
                self.stdout.write(f"Mailing #{mailing.pk} completed.")
