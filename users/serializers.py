from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    """ Сериализатор для регистрации нового пользователя через API. """

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'email', 'password')

    def create(self, validated_data):
        """ Здесь мы создаем пользователя и правильно шифруем его пароль, метод вызывается автоматически"""

        password = validated_data.pop('password') # Извлекаем пароль из проверенных данных
        user = User(**validated_data)  # Создаем объект пользователя, email и другие поля, если они есть
        user.set_password(password)  # Хэшируем (шифруем) пароль с помощью встроенного метода
        user.is_verified = False
        user.save()

        return user