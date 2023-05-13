from faker import Faker
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


fake = Faker()


class CreateUsersTestCase(TestCase):

    def setUp(self):
        self.users = {}
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
        for index in range(1, 3):
            self.users[f'user_{index}'] = {
                'username': username,
                'password': password,
                'email': email
            }
