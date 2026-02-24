from django.core.mail import send_mail
from django.utils import timezone

from newsletter.models import AttemptMailing, Mailing


class MailingService:
    @staticmethod
    def process_mailing(mailing: Mailing) -> dict:
        """
        Отправляет сообщения по рассылке.
        Возвращает статистику: {'sent': int, 'failed': int}.
        """
        now = timezone.now()
        stats = {"sent": 0, "failed": 0}

        if mailing.status == "created":
            mailing.status = "started"
            mailing.first_sending = mailing.first_sending or now
            mailing.save(update_fields=["status", "first_sending"])

        for client in mailing.clients.all():
            try:
                send_mail(
                    subject=mailing.message.theme or "Без темы",
                    message=mailing.message.content or "",
                    from_email=None,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                AttemptMailing.objects.create(mailing=mailing, status="success", response="OK")
                stats["sent"] += 1
            except Exception as exc:
                AttemptMailing.objects.create(mailing=mailing, status="failed", response=str(exc)[:200])
                stats["failed"] += 1

        mailing.last_sending = timezone.now()
        mailing.save(update_fields=["status", "last_sending"])
        return stats
