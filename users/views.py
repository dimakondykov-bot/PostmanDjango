import secrets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer

User = get_user_model()


class RegisterAPIView(APIView):
    """API-контроллер для регистрации нового пользователя"""

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            code = secrets.token_hex(4)
            user.verification_code = code
            user.save()

            try:
                send_mail(
                    subject='Код верификации Почтальон API',
                    message=f'Здравствуйте! Ваш код для подтверждения регистрации: {code}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Ошибка отправки письма: {e}")

            return Response(
                {"message": "Пользователь успешно зарегистрирован. Код верификации отправлен на email."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(APIView):
    """API-контроллер для проверки кода верификации"""

    def post(self, request):
        entered_code = request.data.get('code')
        print("я тут")
        if not entered_code:
            return Response({"error": "Поле 'code' обязательно для заполнения."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(verification_code=entered_code)

            user.is_verified = True
            user.verification_code = None
            user.save()

            return Response({"message": "Email успешно подтвержден! Теперь вы можете войти."},
                            status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Неверный код верификации."}, status=status.HTTP_400_BAD_REQUEST)
