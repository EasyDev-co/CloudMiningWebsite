from faker import Faker
from src.tests import CreateUsersTestCase
from src.reviews.models import Review
from django.urls import reverse


fake = Faker()


def search(id, lst):
    return next((a for a in lst if a['author']['username'] == id), None)


class ReviewTestCase(CreateUsersTestCase):

    def setUp(self):
        result = super().setUp()
        self.create_token()
        return result

    def test_create_reviews_and_get_all_reviews(self):
        users = self.users
        for user in users.values():
            token = user.get('token')
            text = fake.text()
            auth_data = {
                'Authorization': f'Bearer {token}'
            }
            review_data = {
                'text': text
            }
            response = self.client.post(
                path=reverse('review-add'),
                headers=auth_data,
                data=review_data
            )
            new_review = response.json()
            self.assertEqual(response.status_code, 201)
            self.assertEqual(new_review.get('author').get(
                'username'), user.get('username'))
            self.assertEqual(new_review.get(
                'author').get('email'), user.get('email'))
            self.assertEqual(new_review.get('text'), text)

        reviews = Review.objects.all()
        for review in reviews:
            review.is_published = True
            review.save()

        response = self.client.get(path=reverse('reviews'))
        all_reviews = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(all_reviews.get('count'), len(users))
        for user in users.values():
            self.assertContains(response, text=user.get('username'), count=1)
            self.assertContains(response, text=text, count=1)