from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField


User = get_user_model()  # Получаем нашу кастомную модель пользователя

class UserRegisterForm(UserCreationForm):
    """  Форма для регистрации нового пользователя. """
    class Meta:
        model = User
        fields = {"email": EmailField} # поле email должно быть именно полем ввода почты

