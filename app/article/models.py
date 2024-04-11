from django.db import models
from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='articles/author')
    bio = models.TextField()

    def __str__(self):
        return self.name


class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
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
    content = RichTextField(blank=True, null=True)
    is_quotes = models.BooleanField(default=False)


class Comment(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    top_level_comment_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='articles/comment', null=True, blank=True)
    massage = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def children(self):
        if not self.parent:
            return Comment.objects.filter(top_level_comment_id=self.id)
        return None

    def get_image(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}" target="_blank"><img src="{self.image.url}"  /></a>')
        return '-'


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