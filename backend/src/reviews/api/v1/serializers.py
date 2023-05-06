from rest_framework import serializers
from django.contrib.auth.models import User
from src.reviews.models import Review


class ShowAuthorSerializer(serializers.ModelSerializer):
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


# class AddReviewSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField('username', read_only=True)

#     class Meta:
#         model = Review
#         fields = [
#             'id',
#             'author',
#             'text',
#             'created_at',
#         ]
