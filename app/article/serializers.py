from rest_framework import serializers

from app.account.serializers import UserSerializer
from .models import (
    Category,
    Tags,
    Article,
    Content,
    Comment
    )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'title']


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)
    category = CategorySerializer()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'category', 'tags', 'slug', 'image', 'created_date']


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'content', 'is_quotes']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'parent', 'top_level_comment_id', 'massage', 'created_date']


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'parent', 'massage', 'created_date']
        
    def create(self, validated_data):
        request = self.context.get('request')
        article_id = self.context['article_id']
        author_id = request.user.id
        validated_data['author_id'] = author_id
        validated_data['article_id'] = article_id
        return super().create(validated_data)

