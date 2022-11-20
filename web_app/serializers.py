from rest_framework import serializers
from web_app.models import ElectroCar, Person, User
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ElectroCar
        fields = '__all__'
    
    def create(self, validated_data):
        return ElectroCar.objects.create(**validated_data)

    def validate(self, data):
        
        pts = data.get('pts', None)
        sts = data.get('sts', None)

        return {
            'pts': pts,
            'sts': sts
        }

class PersonSerializer(serializers.ModelSerializer):
    '''Инстас пользователя'''
    phone = serializers.CharField(required=False, allow_blank=True, max_length=100)
    
    class Meta:
        model = Person
        fields = '__all__'

    def create(self, validated_data):
        return ElectroCar.objects.create(**validated_data)

class LoginSerializer(serializers.Serializer):
    
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        # Вызвать исключение, если не предоставлена почта.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }