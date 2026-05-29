from datetime import timezone

from django.core.mail import send_mail
from django.conf import settings
from mailing.models import Mailing, MailingLog


def send_mailing_task():
    print("Проверка рассылок началась...")

    now = timezone.now()  # Получаем текущее время с учетом часового пояса

    mailings = Mailing.objects.filter(
        is_active=True,
        start_time__lte=now,
        end_time__gte=now
    )  # Получаем все рассылки, которые нужно отправить

    for mailing in mailings:

        emails = [client.email for client in
                  mailing.recipients.all()]  # Собираем список email-адресов всех получателей этой рассылки

        if not emails:
            continue

        try:
            send_mail(
                subject=mailing.message.subject,  # Тема письма
                message=mailing.message.body,  # Тело письма
                from_email=settings.DEFAULT_FROM_EMAIL,  # Отправитель
                recipient_list=emails,  # Список получателей
                fail_silently=False,  # Если письмо не отправится, Django выдаст ошибку
            )

            MailingLog.objects.create(
                status='success',
                server_response='Письма успешно отправлены',
                mailing=mailing
            )  # Если всё хорошо — создаем лог успеха и завершаем рассылку

            print(f'Рассылка номер {mailing.id} успешно отправлена.')

        except Exception as e:

            MailingLog.objects.create(
                status='failure',  # Записываем в журнал, что произошел сбой
                server_response=str(e),  # Превращаем эту ошибку в строку str(e) и сохраняем в базу текст ошибки
                mailing=mailing
            )

            print(f"Ошибка при отправке рассылки №{mailing.id}: {e}")
