import jwt
from datetime import datetime, timedelta
from django.conf import settings 
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.contrib.auth.models import User

class UserManager(BaseUserManager):
    """
    Класс Manager для кастомного юзера 
    """

    def create_user(self, username, email, password=None):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Дополнительный поля, необходимые Django
    # при указании кастомной модели пользователя.
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.email

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.username

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.username

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

class ElectroCar(models.Model):
    """Таблица электрокара"""
    car_model = models.TextField()
    car_number = models.TextField()
    is_cheking = models.IntegerField(default=1)
    is_registered = models.IntegerField(default=0)
    sts = models.ImageField(upload_to='sts', blank=True, null=True)
    pts = models.ImageField(upload_to='pts', blank=True, null=True)

    def __str__(self):
        return self.car_number

class Person(models.Model):
    "Таблица пользователя"
    SEX = (
        ('Mужской', 'Мужской'),
        ('Женский', 'Женский')
    )
    full_name = models.TextField()
    list_cars = models.ManyToOneRel(ElectroCar, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars')
    birth = models.DateField()
    gender = models.CharField(max_length=10, choices=SEX)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=50)
    nick = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name

# фио, модель машины, номер машины, год рж, пол
