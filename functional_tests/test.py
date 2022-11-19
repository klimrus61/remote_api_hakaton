
from django.test import TestCase
from django.contrib.auth.models import User

class HomeApiTest(TestCase):

    def test_ok_response_home_api(self):
        """Проверяю апи токен"""
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        response = self.client.post('/token/', data={
            'username': 'john',
            'password': 'johnpassword'
        })
        print(response.json())
        self.assertEqual(response.status_code, 200)
