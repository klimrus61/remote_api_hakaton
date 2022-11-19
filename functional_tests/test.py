
from django.test import TestCase
from web_app.models import User
from web_app.models import ElectroCar

class HomeApiTest(TestCase):

    def test_ok_response_home_api(self):
        """Проверяю апи токен"""
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        response = self.client.post('/token/', data={
            'email': 'lennon@thebeatles.com',
            'username': 'john',
            'password': 'johnpassword',
        })
        print(response.json())
        self.assertEqual(response.status_code, 200)

    def test_give_list_untracked_cars(self):
        '''Список машин для обработки админестратору'''

        tesla = ElectroCar.objects.create(car_model='telsa', car_number="Д110ДД12")
        mazda = ElectroCar.objects.create(car_model='mazda', car_number="Д228MAZ12")

        cars_count = ElectroCar.objects.count()

        self.assertEqual(cars_count, 2)

    def test_change_car_status(self):
        '''Проверка смены статуса заявки'''
        tesla = ElectroCar.objects.create(car_model='telsa', car_number="Д110ДД12")

        self.assertEqual(tesla.is_cheking, 1)

        tesla.is_cheking = 0
        tesla.is_registered = 1
        tesla.save()

        self.assertEqual(tesla.is_registered, 1)

    def test_api_registation_new_user(self):
        '''тест: регистрации по api нового пользователя'''

        response = self.client.post('api/users/', data={
            "user": {
        "username": "user1",
        "email": "user1@user.user",
        "password": "qweasdzxc"
        }})
        print(response.content)
