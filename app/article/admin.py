from django.contrib import admin

from .models import (
    Category,
    Tags,
    Article,
    Comment,
    Content,
)


class ContentAdminTabularInline(admin.TabularInline):
    model = Content
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = (ContentAdminTabularInline,)
    list_display = ('id', 'author', 'title', 'slug', 'created_date')
    search_fields = ('title', 'author__username')
    list_filter = ('created_date',)
    autocomplete_fields = ('author',)
    date_hierarchy = 'created_date'
    filter_horizontal = ('tags',)
    readonly_fields = ('slug', 'created_date', 'modified_date')
    list_per_page = 7


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'article', 'top_level_comment_id', 'created_date')
    list_per_page = 7

