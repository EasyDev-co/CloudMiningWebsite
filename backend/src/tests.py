from faker import Faker
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from src.reviews.models import Review


User = get_user_model()


fake = Faker()


class CreateUsersTestCase(TestCase):

    def setUp(self):
        self.users = {}
        for index in range(1, 5):
            profile = fake.simple_profile()
            username = profile.get('username')
            password = fake.password()
            email = fake.email()
            User.objects.create(
                username=username,
                email=email,
                password=make_password(
                    password=password
                ),
                is_confirm=True
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
                path=reverse('login'),
                data=user_data
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('data', response.json().keys())
            self.assertIn('tokens', response.json().get('data').keys())
            tokens = response.json().get('data').get('tokens')
            self.users[key].update({'token': tokens.get('access')})
            self.assertEqual(['refresh', 'access'], list(tokens.keys()))

    def create_data_for_review(self):
        self.create_token()
        users = self.users
        for key, user in users.items():
            username = user.get('username')
            token = user.get('token')
            user = User.objects.get(username=username)
            profile = fake.simple_profile()
            full_name = profile.get('name').split(' ')
            first_name = full_name[0]
            last_name = full_name[1]
            self.users[key].update({'first_name': first_name})
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            auth_data = {
                'Authorization': f'Bearer {token}'
            }

            response = self.client.get(
                path=reverse('user'),
                headers=auth_data
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('data', response.json().keys())
            user_data = response.json().get('data')
            self.assertEqual(user_data.get('first_name'), first_name)
            self.assertEqual(user_data.get('last_name'), last_name)
            self.users[key].update({'first_name': first_name})
            self.users[key].update({'last_name': last_name})

    def create_phone_number(self):
        self.create_token()
        users = self.users
        for key, user in users.items():
            username = user.get('username')
            token = user.get('token')
            user = User.objects.get(username=username)
            phone_number = '8' + fake.msisdn()
            user.phone_number = phone_number
            user.save()

            auth_data = {
                'Authorization': f'Bearer {token}'
            }

            response = self.client.get(
                path=reverse('user'),
                headers=auth_data
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('data', response.json().keys())
            user_data = response.json().get('data')
            self.assertEqual(user_data.get('phone_number'), phone_number)
            self.users[key].update({'phone_number': phone_number})

    def published_reviews(self):
        reviews = Review.objects.all()
        for review in reviews:
            review.is_published = True
            review.save()
