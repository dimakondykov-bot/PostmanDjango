import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler #
from django_apscheduler.jobstores import DjangoJobStore
from mailing.services import send_mail, send_mailing_task


class Command(BaseCommand):
    help = 'Запускает планировщик рассылок'

    def handle(self, *args, **options): # это точка входа
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE) # беру часовой поиск прямо из настроек settings.py
        scheduler.add_jobstore(DjangoJobStore(), 'default') # Это заставит планировщик записывать данные о задачах бд
        scheduler.add_job(
            send_mailing_task,
            trigger='interval',
            seconds=60,
            id='send_mailing_task',
            max_instances=1,
            replace_existing=True,
        )
        scheduler.start()