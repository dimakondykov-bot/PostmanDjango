from django.db import models


class Recipient(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='Ф.И.О')
    email = models.EmailField(unique=True, verbose_name='email')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f'({self.full_name}) ({self.email})'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'





