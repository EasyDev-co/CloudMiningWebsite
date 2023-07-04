from faker import Faker
from src.tests import CreateUsersTestCase
from django.urls import reverse


fake = Faker()


class ReviewTestCase(CreateUsersTestCase):

    def setUp(self):
        result = super().setUp()
        self.create_token()
        return result

    def test_create_review_by_user_with_all_data(self):
        """
        Проверяет добавление отзыва пользователем,
        у которого есть имя, фамилия и номер телефона
        """
        self.create_phone_number()
        self.create_data_for_review()
        users = self.users
        for key, user in users.items():
            token = user.get('token')
            text = fake.text(max_nb_chars=60)
            auth_data = {
                'Authorization': f'Bearer {token}'
            }
            review_data = {
                'text': text,
                'rating': 5
            }

            response = self.client.post(
                path=reverse('review-add'),
                headers=auth_data,
                data=review_data
            )
            self.assertEqual(response.status_code, 201)
            self.assertIn('data', response.json().keys())
            new_review = response.json().get('data')
            self.assertEqual(
                new_review.get('first_name'), user.get('first_name'))
            self.assertEqual(
                new_review.get('last_name'), user.get('last_name'))
            self.assertEqual(
                new_review.get('phone_number'), user.get('phone_number'))
            self.assertEqual(
                new_review.get('rating'), 5)
            self.assertEqual(new_review.get('text'), text)
            self.users[key].update({'text': text})

        # проверяем, что отзывы добавились
        self.published_reviews()
        response = self.client.get(path=reverse('reviews'))
        self.assertIn('data', response.json().keys())
        all_reviews = response.json().get('data')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(all_reviews.get('count'), len(users))
        for user in users.values():
            self.assertContains(
                response, text=user.get('first_name'), count=1
            )
            self.assertContains(
                response, text=user.get('last_name'), count=1
            )
            self.assertContains(
                response, text=user.get('phone_number'), count=1
            )
            self.assertContains(
                response, text=user.get('text'), count=1
            )

    def test_create_review_by_user_without_data_with_add_data(self):
        """
        Проверяет добавление отзыва пользователем,
        у которого нет нужных данных для добавления отзыва
        с передачей данных для отзывов
        """
        users = self.users
        for key, user in users.items():
            token = user.get('token')
            text = fake.text(max_nb_chars=60)
            auth_data = {
                'Authorization': f'Bearer {token}'
            }
            profile = fake.simple_profile()
            full_name = profile.get('name').split(' ')
            first_name = full_name[0]
            last_name = full_name[1]
            phone_number = '8' + fake.msisdn()
            text = fake.text(max_nb_chars=60)
            review_data = {
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'text': text,
                'rating': 5
            }

            response = self.client.post(
                path=reverse('review-add'),
                data=review_data,
                headers=auth_data
            )
            self.assertEqual(response.status_code, 201)
            self.assertIn('data', response.json().keys())
            new_review = response.json().get('data')
            self.assertEqual(
                new_review.get('first_name'), first_name)
            self.assertEqual(
                new_review.get('last_name'), last_name)
            self.assertEqual(
                new_review.get('phone_number'), phone_number)
            self.assertEqual(
                new_review.get('rating'), 5)
            self.assertEqual(new_review.get('text'), text)
            self.users[key].update({'text': text})
            self.users[key].update({'first_name': first_name})
            self.users[key].update({'last_name': last_name})
            self.users[key].update({'phone_number': phone_number})

            # проверяем что данные поменялись
            response = self.client.get(
                path=reverse('user'),
                headers=auth_data
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('data', response.json().keys())
            user_data = response.json().get('data')
            self.assertEqual(
                user_data.get('first_name'), user.get('first_name')
            )
            self.assertEqual(user_data.get('last_name'), user.get('last_name'))
            self.assertEqual(
                user_data.get('phone_number'), user.get('phone_number')
            )

        # проверяем, что отзывы добавились
        self.published_reviews()
        response = self.client.get(path=reverse('reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json().keys())
        all_reviews = response.json().get('data')
        self.assertEqual(all_reviews.get('count'), len(users))
        for user in users.values():
            self.assertContains(
                response, user.get('first_name'), count=1
            )
            self.assertContains(
                response, user.get('last_name'), count=1
            )
            self.assertContains(
                response, user.get('phone_number'), count=1
            )
            self.assertContains(
                response, user.get('text'), count=1
            )

    def test_create_review_by_anonimus_user(self):
        """
        Проверяет добавление отзыва пользователем,
        который не авторизирован
        """
        users = self.users
        for key in users.keys():
            profile = fake.simple_profile()
            full_name = profile.get('name').split(' ')
            first_name = full_name[0]
            last_name = full_name[1]
            phone_number = '8' + fake.msisdn()
            text = fake.text(max_nb_chars=60)
            review_data = {
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'text': text,
                'rating': 5
            }

            response = self.client.post(
                path=reverse('review-add'),
                data=review_data
            )
            self.assertEqual(response.status_code, 201)
            self.assertIn('data', response.json().keys())
            new_review = response.json().get('data')
            self.assertEqual(
                new_review.get('first_name'), first_name)
            self.assertEqual(
                new_review.get('last_name'), last_name)
            self.assertEqual(
                new_review.get('phone_number'), phone_number)
            self.assertEqual(
                new_review.get('rating'), 5)
            self.assertEqual(new_review.get('text'), text)
            self.users[key].update({'text': text})
            self.users[key].update({'first_name': first_name})
            self.users[key].update({'last_name': last_name})
            self.users[key].update({'phone_number': phone_number})

        # проверяем что отзывы добавились
        self.published_reviews()
        response = self.client.get(path=reverse('reviews'))
        self.assertIn('data', response.json().keys())
        all_reviews = response.json().get('data')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(all_reviews.get('count'), len(users))
        for user in users.values():
            self.assertContains(
                response, user.get('first_name'), count=1
            )
            self.assertContains(
                response, user.get('last_name'), count=1
            )
            self.assertContains(
                response, user.get('phone_number'), count=1
            )
            self.assertContains(
                response, user.get('text'), count=1
            )

    def test_create_review_by_user_without_data_without_add_data(self):
        """
        Проверяет добавление отзыва пользователем,
        у которого нет нужных данных для добавления отзыва
        без передачи данных для отзывов
        """
        users = self.users
        for _, user in users.items():
            token = user.get('token')
            text = fake.text(max_nb_chars=60)
            auth_data = {
                'Authorization': f'Bearer {token}'
            }
            text = fake.text(max_nb_chars=60)
            review_data = {
                'text': text,
                'rating': 5
            }

            response = self.client.post(
                path=reverse('review-add'),
                data=review_data,
                headers=auth_data
            )
            self.assertEqual(response.status_code, 400)
            self.assertIn('errors', response.json().keys())
            errors = response.json().get('errors')
            self.assertEqual(
                errors.get('first_name')[0],
                'This field may not be blank.'
            )
            self.assertEqual(
                errors.get('last_name')[0],
                'This field may not be blank.'
            )
            self.assertEqual(
                errors.get('phone_number')[0],
                'This field may not be blank.'
            )

        # проверяем что отзывов нет
        self.published_reviews()
        response = self.client.get(path=reverse('reviews'))
        self.assertIn('data', response.json().keys())
        all_reviews = response.json().get('data')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(all_reviews.get('count'), len(users))

    def test_create_review_by_user_without_phone_number_without_add_data(self):
        """
        Проверяет добавление отзыва пользователем,
        у которого нет номера телефона для добавления отзыва
        без его передачи для отзыва
        """
        self.create_data_for_review()
        users = self.users
        for _, user in users.items():
            token = user.get('token')
            text = fake.text(max_nb_chars=60)
            auth_data = {
                'Authorization': f'Bearer {token}'
            }
            text = fake.text(max_nb_chars=60)
            review_data = {
                'text': text,
                'rating': 5
            }

            response = self.client.post(
                path=reverse('review-add'),
                data=review_data,
                headers=auth_data
            )
            self.assertEqual(response.status_code, 400)
            self.assertIn('errors', response.json().keys())
            errors = response.json().get('errors')
            self.assertEqual(
                errors.get('phone_number')[0],
                'This field may not be blank.'
            )

        # проверяем что отзывов нет
        self.published_reviews()
        response = self.client.get(path=reverse('reviews'))
        self.assertIn('data', response.json().keys())
        all_reviews = response.json().get('data')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(all_reviews.get('count'), len(users))

    def test_create_review_by_user_without_phone_number_with_add_data(self):
        """
        Проверяет добавление отзыва пользователем,
        у которого нет номера телефона для добавления отзыва
        и передаем его для добавление отзыва
        """
        self.create_data_for_review()
        users = self.users
        for key, user in users.items():
            token = user.get('token')
            text = fake.text(max_nb_chars=60)
            auth_data = {
                'Authorization': f'Bearer {token}'
            }
            text = fake.text(max_nb_chars=60)
            phone_number = '8' + fake.msisdn()
            review_data = {
                'text': text,
                'rating': 5,
                'phone_number': phone_number
            }

            response = self.client.post(
                path=reverse('review-add'),
                data=review_data,
                headers=auth_data
            )
            self.assertEqual(response.status_code, 201)
            self.assertIn('data', response.json().keys())
            new_review = response.json().get('data')
            self.assertEqual(
                new_review.get('first_name'), user.get('first_name'))
            self.assertEqual(
                new_review.get('last_name'), user.get('last_name'))
            self.assertEqual(
                new_review.get('phone_number'), phone_number)
            self.assertEqual(
                new_review.get('rating'), 5)
            self.assertEqual(new_review.get('text'), text)
            self.users[key].update({'text': text})
            self.users[key].update({'phone_number': phone_number})

            # проверяем что данные поменялись
            response = self.client.get(
                path=reverse('user'),
                headers=auth_data
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('data', response.json().keys())
            user_data = response.json().get('data')
            self.assertEqual(
                user_data.get('first_name'), user.get('first_name')
            )
            self.assertEqual(user_data.get('last_name'), user.get('last_name'))
            self.assertEqual(
                user_data.get('phone_number'), user.get('phone_number')
            )

        # проверяем что отзывы добавились
        self.published_reviews()
        response = self.client.get(path=reverse('reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json().keys())
        all_reviews = response.json().get('data')
        self.assertEqual(all_reviews.get('count'), len(users))
        for user in users.values():
            self.assertContains(
                response, user.get('first_name'), count=1
            )
            self.assertContains(
                response, user.get('last_name'), count=1
            )
            self.assertContains(
                response, user.get('phone_number'), count=1
            )
            self.assertContains(
                response, user.get('text'), count=1
            )
