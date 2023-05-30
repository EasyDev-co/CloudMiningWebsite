from faker import Faker
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()


fake = Faker()


class CreateUsersTestCase(TestCase):

    def setUp(self):
        self.users = {}
        for index in range(1, 3):
            profile = fake.simple_profile()
            username = profile.get('username')
            password = fake.password()
            email = fake.email()
            User.objects.create(
                username=username,
                email=email,
                password=make_password(
                    password=password
                )
            )
            self.users[f'user_{index}'] = {
                'username':  username,
                'password': password,
                'email': email
            }

    def create_token(self):
        users = self.users
        for key, user in users.items():
            user_data = {
                'username': user.get('username'),
                'password': user.get('password')
            }
            response = self.client.post(
                path=reverse('jwt-create'),
                data=user_data
            )
            auth_user = response.json()
            self.assertEqual(response.status_code, 200)
            self.users[key].update({'token': auth_user.get('access')})
            self.assertEqual(['refresh', 'access'], list(auth_user.keys()))
