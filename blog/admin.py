from django.contrib import admin

from blog.models import Bookmark, Category, Comment, Like, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "view_count", "reading_time", "created_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "content", "seo_title", "seo_description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    readonly_fields = ("view_count", "reading_time", "summary", "created_at", "updated_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "parent", "created_at")
    search_fields = ("content", "user__username", "post__title")
    list_filter = ("created_at",)


admin.site.register(Like)
admin.site.register(Bookmark)
