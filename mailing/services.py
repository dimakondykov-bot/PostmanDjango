from django.core.mail import send_mail
from django.conf import settings
from mailing.models import Mailing, MailingLog



def send_mailing_task():
    print("Проверка рассылок началась...")
    mailings = Mailing.objects.filter(status__in=['created', 'started'])  # Получаем все рассылки, которые нужно отправить

    for mailing in mailings:
        mailing.status = 'started'  # Меняем статус на 'started', чтобы никто другой её не подхватил
        mailing.save()

        emails = [client.email for client in
                  mailing.recipients.all()]  # Собираем список email-адресов всех получателей этой рассылки

        try:
            send_mail(
                subject=mailing.message.subject,  # Тема письма
                message=mailing.message.body,  # Тело письма
                from_email=settings.DEFAULT_FROM_EMAIL,  # Отправитель
                recipient_list=emails,  # Список получателей
                fail_silently=False,  # Если письмо не отправится, Django выдаст ошибку
            )

            MailingLog.objects.create(
                status='success', mailing=mailing)  # Если всё хорошо — создаем лог успеха и завершаем рассылку
            mailing.status = 'completed'  # Мы меняем статус самой рассылки

        except Exception as e:
            MailingLog.objects.create(
                status='failure',  # Записываем в журнал, что произошел сбой
                server_response=str(e),  # Превращаем эту ошибку в строку str(e) и сохраняем в базу текст ошибки
                mailing=mailing
            )

        mailing.save()