from django_filters import rest_framework
from rest_framework import filters
from rest_framework import generics

from .models import (
    Category,
    Tags,
    Article,
    Content,
    Comment
    )
from .serializers import (
    CategorySerializer,
    TagsSerializer,
    ArticleSerializer,
    ContentSerializer,
    CommentSerializer,
    CommentPostSerializer
    )


class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class TagsAPIView(generics.ListAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class ArticleAPIView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tags', 'category']
    search_fields = ('title', 'author__username')


class ContentAPIView(generics.ListAPIView):
    # article/{article_id}/content
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        article_id = self.kwargs.get('article_id')
        qs = qs.filter(id=article_id)
        return qs


class CommentAPIView(generics.ListCreateAPIView):
    # article/{article_id}/comment
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    serializer_post_class = CommentPostSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        article_id = self.kwargs.get('article_id')
        qs = qs.filter(id=article_id)
        return qs

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.serializer_post_class
        return self.serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()
        article_id = self.kwargs.get('article_id')
        context["article_id"] = article_id
        return context
