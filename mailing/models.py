from datetime import timezone

from django.db import models
from django.conf import settings


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Дата и время первой отправки')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания отправки')

    is_active = models.BooleanField(default=True, verbose_name='Активна')

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='Статус'
    )

    recipients = models.ManyToManyField(
        'client_management.Recipient',
        verbose_name='Получатели',
    )

    message = models.ForeignKey(
        'message_management.Message',
        on_delete=models.CASCADE,
        verbose_name='Сообщение'
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Владелец',
        blank=True, null=True
    )

    @property
    def status(self):
        now = timezone.now()

        if now > self.is_active:
            return 'Завершена менеджером'

        if now < self.start_time:
            return 'Создана'

        elif self.start_time <= now <= self.end_time:
            return 'Запущена'
        else:
            return 'Завершена'

    def __str__(self):
        return f'Рассылка номер: {self.id} {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

class MailingLog(models.Model):
    STATUS_CHOICES = [
        ('success','Успешно'),
        ('failure','Ошибка')
    ]

    attempt_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='success', verbose_name='Статус')
    server_response = models.TextField(blank=True, null=True, verbose_name='Ответ сервера')
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, related_name='logs', verbose_name='Рассылка')