from rest_framework import serializers
from web_app.models import ElectroCar, Person, User
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    # Убедитесь, что пароль содержит не менее 8 символов, не более 128,
    # и так же что он не может быть прочитан клиентской стороной
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # Клиентская сторона не должна иметь возможность отправлять токен вместе с
    # запросом на регистрацию. Сделаем его доступным только на чтение.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # Перечислить все поля, которые могут быть включены в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        # Использовать метод create_user, который мы
        # написали ранее, для создания нового пользователя.
        return User.objects.create_user(**validated_data)

class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    car_model = serializers.CharField()
    car_number = serializers.CharField()
    is_cheking = serializers.IntegerField()
    is_registered = serializers.IntegerField()
    pts = serializers.ImageField()
    sts = serializers.ImageField()

    def create(self, validated_data):
        """
        Создает и возвращает инстанс ElectroCar с учетом валидных данных
        """
        return ElectroCar.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.car_model = validated_data.get('car_model', instance.car_model)
        instance.number = validated_data.get('number', instance.number)
        instance.is_cheking = validated_data.get('is_cheking', instance.is_cheking)
        instance.is_registere = validated_data.get('is_registere', instance.is_registere)
        instance.pts = validated_data.get('pts', instance.pts)
        instance.sts = validated_data.get('sts', instance.sts)
        return instance

class PersonSerializer(serializers.ModelSerializer):
    '''Инстас пользователя'''
    phone = serializers.CharField(required=False, allow_blank=True, max_length=100)
    avatar = serializers.ImageField(required=False)
    class Meta:
        model = Person
        fields = ['id', 'full_name', 'list_cars', 
        'avatar', 'birth', 'gender', 'user', 'phone', 
        'email', 'nick', 'city']

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # В методе validate мы убеждаемся, что текущий экземпляр
        # LoginSerializer значение valid. В случае входа пользователя в систему
        # это означает подтверждение того, что присутствуют адрес электронной
        # почты и то, что эта комбинация соответствует одному из пользователей.
        email = data.get('email', None)
        password = data.get('password', None)

        # Вызвать исключение, если не предоставлена почта.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Вызвать исключение, если не предоставлен пароль.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # Метод authenticate предоставляется Django и выполняет проверку, что
        # предоставленные почта и пароль соответствуют какому-то пользователю в
        # нашей базе данных. Мы передаем email как username, так как в модели
        # пользователя USERNAME_FIELD = email.
        user = authenticate(username=email, password=password)

        # Если пользователь с данными почтой/паролем не найден, то authenticate
        # вернет None. Возбудить исключение в таком случае.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django предоставляет флаг is_active для модели User. Его цель
        # сообщить, был ли пользователь деактивирован или заблокирован.
        # Проверить стоит, вызвать исключение в случае True.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # Метод validate должен возвращать словать проверенных данных. Это
        # данные, которые передются в т.ч. в методы create и update.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }