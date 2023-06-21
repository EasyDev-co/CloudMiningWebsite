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
            phone_number = int(fake.msisdn()) - index
            User.objects.create(
                username=username,
                email=email,
                password=make_password(
                    password=password
                ),
                phone_number=phone_number,
                is_confirm=True
            )
            self.users[f'user_{index}'] = {
                'username':  username,
                'password': password,
                'email': email,
                'phone_number': str(phone_number)
            }

    def create_token(self):
        users = self.users
        for key, user in users.items():
            user_data = {
                'username': user.get('username'),
                'password': user.get('password')
            }
            response = self.client.post(
                path=reverse('login'),
                data=user_data
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('data', response.json().keys())
            self.assertIn('tokens', response.json().get('data').keys())
            tokens = response.json().get('data').get('tokens')
            self.users[key].update({'token': tokens.get('access')})
            self.assertEqual(['refresh', 'access'], list(tokens.keys()))
