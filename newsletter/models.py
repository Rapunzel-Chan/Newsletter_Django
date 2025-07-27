from django.db import models
from django.utils import timezone

from users.models import User


# Create your models here.


class Client(models.Model):
    email = models.EmailField(
        max_length=50, unique=True, verbose_name="Электронный адрес", help_text="Введите Ваш email"
    )
    full_name = models.CharField(
        max_length=100, verbose_name="Ф.И.О.", help_text="Введите Ваше Ф.И.О.", blank=True, null=True
    )
    comment = models.TextField(verbose_name="Комментарий", help_text="Введите Ваш комментарий", blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_set", null=True, blank=True)

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["email"]
        # permissions = [
        #     ("can_unpublish_blog", "Can unpublish blog"),
        # ]

    def __str__(self):
        return self.full_name or self.email


class Message(models.Model):
    theme = models.CharField(
        max_length=100, verbose_name="Тема письма", help_text="Введите тему Вашего письма", blank=True, null=True
    )
    content = models.TextField(
        verbose_name="Тело письма", help_text="Введите текст Вашего письма", blank=True, null=True
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_set", null=True, blank=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        # ordering = ["email"]
        # permissions = [
        #     ("can_unpublish_blog", "Can unpublish blog"),
        # ]

    def __str__(self):
        return self.theme or "Без темы"


class Mailing(models.Model):
    first_sending = models.DateTimeField(
        # verbose_name="Дата и время первой отправки рассылки",
        # help_text="Введите дату и время первой отправки рассылки"
    )
    last_sending = models.DateTimeField(
        null=True,
        blank=True,
        # verbose_name="Дата окончания отправки рассылки",
        # help_text="Введите дату и время последней отправки рассылки"
    )
    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("completed", "Завершена"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="created", verbose_name="Статус")
    message = models.ForeignKey(
        Message, verbose_name="Сообщение", help_text="Укажите Ваше сообщение", on_delete=models.CASCADE
    )
    clients = models.ManyToManyField(
        Client, verbose_name="Получатели", help_text="Укажите Получателей Вашего сообщения"
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mailing_set", null=True, blank=True)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        # ordering = ["email"]
        # permissions = [
        #     ("can_unpublish_blog", "Can unpublish blog"),
        # ]

    def __str__(self):
        return f"Рассылка №{self.pk} — {self.status}"

    def mark_completed(self):
        self.status = "completed"
        self.last_sending = timezone.now()
        self.save()


class AttemptMailing(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время первой попытки отправки рассылки",
        help_text="Введите дату и время первой попытки отправки рассылки",
    )
    is_successful = models.BooleanField(
        default=False, verbose_name="Успешно", help_text="Укажите, успешной ли была попытка отправки"
    )
    response = models.TextField(
        verbose_name="Ответ почтового сервера", help_text="Введите ответ почтового сервера", blank=True, null=True
    )
    mailing = models.ForeignKey(
        Mailing, verbose_name="Рассылка", help_text="Укажите текст рассылки", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Попытка отправки"
        verbose_name_plural = "Попытки отправки"

    def __str__(self):
        return f"Попытка #{self.pk} — {'Успешно' if self.is_successful else 'Не успешно'}"
