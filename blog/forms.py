from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from blog.models import Comment, Post, Tag


class PostForm(forms.ModelForm):
    tag_names = forms.CharField(
        required=False,
        help_text="Comma-separated tags",
        widget=forms.TextInput(attrs={"placeholder": "django, python, architecture"}),
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "featured_image",
            "category",
            "tag_names",
            "status",
            "scheduled_publish_date",
            "seo_title",
            "seo_description",
        ]
        widgets = {
            "content": CKEditor5Widget(config_name="default"),
            "scheduled_publish_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "seo_description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["tag_names"].initial = ", ".join(self.instance.tags.values_list("name", flat=True))

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            self.save_tags(post)
            self.save_m2m()
        return post

    def save_tags(self, post):
        names = [name.strip() for name in self.cleaned_data.get("tag_names", "").split(",") if name.strip()]
        post.tags.set([Tag.objects.get_or_create(name=name)[0] for name in names])


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "parent"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Join the discussion..."}),
            "parent": forms.HiddenInput(),
        }
