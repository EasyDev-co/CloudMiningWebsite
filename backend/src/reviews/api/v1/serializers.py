from rest_framework import serializers
from src.reviews.models import Review
from django.contrib.auth import get_user_model
from src.users.api.v1.constants import PHONE_NUMBER_PATTERN
from django.core.validators import RegexValidator

User = get_user_model()


class ShowAuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User

        fields = [
            'id',
            'username',
            'email'
        ]


class ReviewsSerializer(serializers.ModelSerializer):
    author = ShowAuthorSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'author',
            'text',
            'created_at',
        ]


class AddReviewForAnonymousAndWithoutDataUsersSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(validators=[RegexValidator(
        regex=PHONE_NUMBER_PATTERN,
        message='Incorrect phone number. The number must consist of digits'
    ), ],
        min_length=8,
        max_length=15
    )

    class Meta:
        model = Review
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'text'
        ]


class AddReviewForAuthenticatedUsersWithDataSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(validators=[RegexValidator(
        regex=PHONE_NUMBER_PATTERN,
        message='Incorrect phone number. The number must consist of digits'
    ), ],
        min_length=8,
        max_length=15
    )

    class Meta:
        model = Review
        fields = [
            'phone_number',
            'text'
        ]
