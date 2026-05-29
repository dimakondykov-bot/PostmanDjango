from .models import Message
from .serializers import MessageSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control
from rest_framework import viewsets



class MessageViewSet(viewsets.ModelViewSet):
    """ Автоматический CRUD для сообщений с ограничением доступа по ролям """

    serializer_class = MessageSerializers
    permission_classes = [IsAuthenticated] # Защищаем весь контроллер.

    @method_decorator(cache_page(900))
    @method_decorator(cache_control(private=True, max_age=3600), name='dispatch')
    def list(self, request, *args, **kwargs):
        """ Этот метод отвечает за выдачу списка всех сообщений (GET-запрос на /api/message/) """
        return super().list(request, *args, **kwargs)


    def get_queryset(self):
        """ Этот метод определяет, какие именно строки из базы данных увидит пользователь. """

        user = self.request.user

        # Если это менеджер или администратор сайта — возвращаем ВСЕ сообщения
        if user.is_manager or user.is_staff:
            return Message.objects.all()

        # Если это обычный пользователь — возвращаем ТОЛЬКО его собственные сообщения
        return Message.objects.filter(owner=user)

    def perform_create(self, serializer):
        """ Этот метод срабатывает автоматически в момент создания нового сообщения. """

        # записываем текущего пользователя в поле 'owner' и закрепляет сообщение именно за ним
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """ Этот метод срабатывает автоматически при попытке изменить сообщение. """

        # Достаем объект сообщения, который пытаются отредактировать
        message = self.get_object()

        if message.owner != self.request.user:
            raise PermissionDenied("Менеджерам и посторонним пользователям запрещено редактировать чужие сообщения.")

        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        """ Этот метод срабатывает автоматически при попытке удалить сообщение. """

        if instance.owner != self.request.user:
            raise PermissionDenied("Запрещено удалять чужие сообщения.")

        # Если это владелец — удаляем объект из базы данных
        instance.delete()
