import math
import re

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify, striptags
from django.urls import reverse
from django.utils import timezone


def unique_slug_for(instance, value, slug_field="slug"):
    base_slug = slugify(value)[:220] or "post"
    slug = base_slug
    counter = 2
    model = instance.__class__
    queryset = model.objects.filter(**{slug_field: slug})
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)
    while queryset.exists():
        suffix = f"-{counter}"
        slug = f"{base_slug[:220 - len(suffix)]}{suffix}"
        queryset = model.objects.filter(**{slug_field: slug})
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)
        counter += 1
    return slug


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        return (
            super()
            .get_queryset()
            .filter(status=Post.Status.PUBLISHED)
            .filter(models.Q(scheduled_publish_date__isnull=True) | models.Q(scheduled_publish_date__lte=now))
        )


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_for(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"slug": self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_for(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:tag", kwargs={"slug": self.slug})


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    featured_image = models.ImageField(upload_to="posts/%Y/%m/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    scheduled_publish_date = models.DateTimeField(blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)
    reading_time = models.PositiveIntegerField(default=1)
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedPostManager()

    class Meta:
        ordering = ["-scheduled_publish_date", "-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["status", "scheduled_publish_date"]),
            models.Index(fields=["created_at"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_for(self, self.title)
        plain_text = striptags(self.content or "")
        word_count = len(re.findall(r"\w+", plain_text))
        self.reading_time = max(1, math.ceil(word_count / 220))
        if not self.summary:
            self.summary = self.generate_summary(plain_text)
        if not self.seo_title:
            self.seo_title = self.title[:70]
        if not self.seo_description:
            self.seo_description = self.generate_seo_description(plain_text)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    @property
    def is_live(self):
        return self.status == self.Status.PUBLISHED and (
            self.scheduled_publish_date is None or self.scheduled_publish_date <= timezone.now()
        )

    @staticmethod
    def generate_summary(text):
        clean = " ".join(text.split())
        return clean[:260] + ("..." if len(clean) > 260 else "")

    @staticmethod
    def generate_seo_description(text):
        clean = " ".join(text.split())
        return clean[:155] + ("..." if len(clean) > 155 else "")

    def seo_suggestions(self):
        suggestions = []
        if len(self.title) < 35:
            suggestions.append("Consider a more descriptive title around 45-60 characters.")
        if not self.featured_image:
            suggestions.append("Add a featured image for stronger social previews.")
        if self.reading_time < 2:
            suggestions.append("Short posts can work, but add examples if search intent needs depth.")
        if not self.tags.exists():
            suggestions.append("Add focused tags to improve discovery.")
        return suggestions or ["SEO basics look good."]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["post", "user"], name="unique_post_like")]

    def __str__(self):
        return f"{self.user} likes {self.post}"


class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmarks")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["post", "user"], name="unique_post_bookmark")]

    def __str__(self):
        return f"{self.user} bookmarked {self.post}"
