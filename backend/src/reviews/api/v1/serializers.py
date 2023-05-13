from rest_framework import serializers
from src.users.models import User
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
