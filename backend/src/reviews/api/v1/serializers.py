from rest_framework import serializers, exceptions
from src.reviews.models import Review
from src.users.api.v1.constants import PHONE_NUMBER_PATTERN
from django.core.validators import RegexValidator


class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'text',
            'created_at',
        ]


class AddReviewSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField(validators=[RegexValidator(
        regex=PHONE_NUMBER_PATTERN,
        message='Incorrect phone number. The number must consist of digits'
    ), ],
        min_length=8,
        max_length=15
    )
    rating = serializers.IntegerField()

    class Meta:
        model = Review
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'rating',
            'text'
        ]

    def validate_rating(self, value):
        print(value)
        if not isinstance(value, int):
            raise exceptions.ValidationError(
                detail='A rating should be an integer number'
            )
        else:
            if value < 1 or value > 5:
                raise exceptions.ValidationError(
                    detail='A rating should be a number between 1 and 5'
                )
            return value
