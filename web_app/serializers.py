from rest_framework import serializers
from web_app.models import ElectroCar, Person


class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    car_model = serializers.CharField()
    car_number = serializers.CharField()
    is_cheking = serializers.IntegerField()
    is_registered = serializers.IntegerField()

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
        return instance

class PersonSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, allow_blank=True, max_length=100)
    class Meta:
        model = Person
        fields = ['id', 'full_name', 'list_cars', 
        'avatar', 'birth', 'gender', 'user', 'phone']
