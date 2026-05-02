from django.db import models


class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    started_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время первой отправки')
    finished_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время окончания отправки')

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


class MailingLog(models.Model):
    STATUS_CHOICES = [
        ('success','Успешно'),
        ('failure','Ошибка')
    ]

    attempt_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='success', verbose_name='Статус')

    server_response = models.TextField(blank=True, null=True, verbose_name='Ответ сервера')

    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, related_name='logs', verbose_name='Рассылка')