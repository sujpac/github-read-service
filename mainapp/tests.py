from rest_framework.test import APITestCase, force_authenticate
from django.contrib.auth.models import User

class MainAppTest(APITestCase):
    def setUp(self):
        self.username = 'test_user'
        self.password = 'test_password123'
        self.user = User.objects.create(username=self.username, password=self.password)
        self.client.force_authenticate(user=self.user)

    def test_github_proxy1(self):
        response = self.client.get('/zen/', {}, format='json')
        self.assertEqual(response.status_code, 200)
