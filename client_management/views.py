from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Recipient
from .serializers import RecipientSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, cache_control


class ClientViewSet(viewsets.ModelViewSet):
    """ Автоматический CRUD для клиентов (получателей) с ограничением доступа по ролям """

    serializer_class = RecipientSerializer
    permission_classes = [IsAuthenticated]  # Защищаем весь контроллер (доступ только авторизованным)

    @method_decorator(cache_page(300))
    @method_decorator(cache_control(private=True, max_age=3600))
    def list(self, request, *args, **kwargs):
        """ Этот метод отвечает за выдачу списка всех клиентов """
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """ Этот метод определяет, какие именно строки из базы данных увидит пользователь. """

        user = self.request.user

        # Если это менеджер или администратор сайта — возвращаем ВСЕХ клиентов системы
        if user.is_manager or user.is_staff:
            return Recipient.objects.all()

        # Если это обычный пользователь — возвращаем ТОЛЬКО его собственных клиентов
        return Recipient.objects.filter(owner=user)

    def perform_create(self, serializer):
        """ Этот метод срабатывает автоматически в момент создания нового клиента. """

        # Записываем текущего пользователя в поле 'owner' и закрепляем клиента именно за ним
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """ Этот метод срабатывает автоматически при попытке изменить данные клиента. """

        # Достаем объект конкретного клиента, которого пытаются отредактировать
        recipient = self.get_object()

        # Если редактировать пытается НЕ владелец этого клиента — выдаем отказ в доступе
        if recipient.owner != self.request.user:
            raise PermissionDenied("Менеджерам и посторонним пользователям запрещено редактировать чужих клиентов.")

        # Если проверку прошел — сохраняем изменения и подтверждаем владельца
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        """ Этот метод срабатывает автоматически при попытке удалить клиента. """

        if instance.owner != self.request.user:
            raise PermissionDenied("Запрещено удалять чужих клиентов.")

        # Если это владелец — удаляем объект клиента из базы данных
        instance.delete()
