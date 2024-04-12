from django.urls import path
from .views import (
    CategoryAPIView,
    TagsAPIView,
    ArticleAPIView,
    ContentAPIView,
    CommentAPIView
    )

app_name = 'article'

urlpatterns = [
    path('category/', CategoryAPIView.as_view(), name='category'),
    path('tags/', TagsAPIView.as_view(), name='tags'),
    path('article/', ArticleAPIView.as_view(), name='article'),
    path('<int:article_id>/content/', ContentAPIView.as_view(), name='content'),
    path('<int:article_id>/comment/', CommentAPIView.as_view(), name='comment'),
]


'''
    Category
        -list
    Tags
        -list
    Article
        -list
    Content
        -list
    Comment
        -list
        -create
'''
