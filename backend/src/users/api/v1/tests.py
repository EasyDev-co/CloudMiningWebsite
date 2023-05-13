from faker import Faker
from src.tests import CreateUsersTestCase
from django.urls import reverse


fake = Faker()


class UserTestCase(CreateUsersTestCase):
    def test_create_user(self):
        profile = fake.simple_profile()
        password = fake.password()
        username = profile.get('username')
        email = fake.email()
        new_user = {
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': password
        }
        response = self.client.post(
            path=reverse('user-list'),
            data=new_user
        )
        new_user = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(new_user.get('username'), username)
        self.assertEqual(new_user.get('email'), email)

    def test_create_user_non_equal_passwords(self):
        profile = fake.simple_profile()
        username = profile.get('username')
        email = fake.email()
        new_user = {
            'username': username,
            'email': email,
            'password': fake.password(),
            'password_confirm': fake.password()
        }
        response = self.client.post(
            path=reverse('user-list'),
            data=new_user
        )
        new_user = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            new_user.get('password')[0], 'The passwords entered do not match'
        )
        self.assertEqual(
            new_user.get('password_confirm')[0], 'The passwords entered do not match'
        )

    def test_create_user_with_exist_username(self):
        username = self.users.get('user_1').get('username')
        email = fake.email()
        password = fake.password()
        new_user = {
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': password
        }
        response = self.client.post(
            path=reverse('user-list'),
            data=new_user
        )
        new_user = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            new_user.get('username')[0], 'A user with that username already exists.'
        )

    # def test_create_user_with_exist_email(self):
    #     profile = fake.simple_profile()
    #     username = profile.get('username')
    #     email = self.users.get('user_2').get('email')
    #     password = fake.password()
    #     new_user = {
    #         'username': username,
    #         'email': email,
    #         'password': password,
    #         'password_confirm': password
    #     }
    #     response = self.client.post(
    #         path=reverse('user-list'),
    #         data=new_user
    #     )
    #     new_user = response.json()
    #     print(new_user)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(
    #         new_user.get('username')[0], 'A user with that username already exists.'
    #    )

    def test_create_token(self):
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