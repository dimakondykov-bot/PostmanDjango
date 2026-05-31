from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailing.models import Mailing, MailingLog


def send_mailing_task():
    """Фоновая задача для проверки и автоматической отправки активных рассылок."""
    print("Проверка рассылок началась...")

    now = timezone.now()

    # Получаем все рассылки, которые активны и подходят по времени
    mailings = Mailing.objects.filter(
        is_active=True, start_time__lte=now, end_time__gte=now
    )

    for mailing in mailings:
        # Собираем список email-адресов получателей этой рассылки
        emails = [client.email for client in mailing.recipients.all()]

        if not emails:
            print(f"У рассылки №{mailing.id} нет получателей. Пропускаем.")
            continue

        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails,
                fail_silently=False,
            )

            # Если всё хорошо — создаем лог успеха
            MailingLog.objects.create(
                status="success",
                server_response="Письма успешно отправлены",
                mailing=mailing,
            )
            print(f"Рассылка номер {mailing.id} успешно отправлена.")

        except Exception as e:
            # Записываем в журнал, что произошел сбой
            MailingLog.objects.create(
                status="failure",
                server_response=str(e),
                mailing=mailing,
            )
            print(f"Ошибка при отправке рассылки №{mailing.id}: {e}")
