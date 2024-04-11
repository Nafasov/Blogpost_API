from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.utils import timezone

from app.account.models import User


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tags, )
    title = models.CharField(max_length=255)
    slug = models.SlugField(editable=True, )
    image = models.ImageField(upload_to='articles/', )
    modified_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Content(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True, related_name='contents')
    content = models.TextField()
    is_quotes = models.BooleanField(default=False)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    top_level_comment_id = models.IntegerField(null=True, blank=True)
    massage = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author

    @property
    def children(self):
        if not self.parent:
            return Comment.objects.filter(top_level_comment_id=self.id)
        return None


def pre_save_article(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title + '-' + str(timezone.now().date()))


pre_save.connect(pre_save_article, sender=Article)


def pre_save_comments(sender, instance, *args, **kwargs):
    if instance.parent:
        if instance.parent.top_level_comment_id:
            instance.top_level_comment_id = instance.parent.top_level_comment_id
        else:
            instance.top_level_comment_id = instance.parent.id


pre_save.connect(pre_save_comments, sender=Comment)
