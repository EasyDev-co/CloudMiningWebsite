from faker import Faker
from djoser.email import PasswordResetEmail
from rest_framework.response import Response
from django.contrib.auth.models import User
from src.tests import CreateUsersTestCase
from src.users.api.v1.views import CustomUserViewSet
from django.urls import reverse


fake = Faker()


def test_reset_password(self, request, *args, **kwargs):
    """The function simulates a password reset procedure
    without sending an email"""

    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.get_user()
    if user:
        context = {
            'user_id': user.id,
            'domain': request.get_host(),
            'protocol': 'https' if request.is_secure() else 'http',
            'site_name': request.get_host()
        }
        context['user'] = User.objects.get(id=context.get('user_id'))
        result = PasswordResetEmail(context=context).get_context_data()
    return Response(
        status=200,
        data={'uid': result.get('uid'),
              'token': result.get('token')
              })


class UserTestCase(CreateUsersTestCase):
    def test_create_user(self):
        """Testing user registration"""

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
        """Testing user registration with unequal passwords"""

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
            new_user.get('password_confirm')[
                0], 'The passwords entered do not match'
        )

    def test_create_user_with_exist_username(self):
        """Testing the registration of a user with an existing username"""

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
            new_user.get('username')[0],
            'A user with that username already exists.'
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
        """Testing token generation"""

        self.create_token()

    def test_reset_password(self):
        """Test resetting the password and creating a new password"""

        # Monkey patching
        CustomUserViewSet.reset_password = test_reset_password
        email = self.users.get('user_1').get('email')
        username = self.users.get('user_1').get('username')
        new_password = fake.password()
        user_data = {
            'email': email
        }
        response = self.client.post(
            path=reverse('user-reset-password'),
            data=user_data
        )
        reset_data = response.json()
        self.assertEqual(response.status_code, 200)
        uid = reset_data.get('uid')
        token = reset_data.get('token')
        new_password_data = {
            'uid': uid,
            'token': token,
            'new_password': new_password,
            'repeat_new_password': new_password
        }
        response = self.client.post(
            path=reverse('user-reset-password-confirm'),
            data=new_password_data
        )
        self.assertEqual(response.status_code, 204)
        user_data = {
            'username': username,
            'password': new_password
        }
        response = self.client.post(
            path=reverse('jwt-create'),
            data=user_data
        )
        auth_user = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(['refresh', 'access'], list(auth_user.keys()))
