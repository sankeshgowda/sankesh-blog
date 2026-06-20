from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render

from blog.forms import PostForm
from blog.models import Bookmark, Post


@login_required
def dashboard_home(request):
    posts = Post.objects.filter(author=request.user)
    context = {
        "post_count": posts.count(),
        "published_count": posts.filter(status=Post.Status.PUBLISHED).count(),
        "draft_count": posts.filter(status=Post.Status.DRAFT).count(),
        "total_views": posts.aggregate(total=Sum("view_count"))["total"] or 0,
        "recent_posts": posts[:5],
        "chart_labels": [post.title[:18] for post in posts.order_by("-view_count")[:6]],
        "chart_values": [post.view_count for post in posts.order_by("-view_count")[:6]],
    }
    return render(request, "dashboard/dashboard.html", context)


@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).select_related("category").prefetch_related("tags")
    return render(request, "dashboard/my_posts.html", {"posts": posts})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_tags(post)
            form.save_m2m()
            messages.success(request, "Post saved.")
            return redirect("dashboard:my_posts")
    else:
        form = PostForm()
    return render(request, "dashboard/post_form.html", {"form": form, "title": "Create Post"})


@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated.")
            return redirect("dashboard:my_posts")
    else:
        form = PostForm(instance=post)
    return render(request, "dashboard/post_form.html", {"form": form, "post": post, "title": "Edit Post"})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("dashboard:my_posts")
    return render(request, "dashboard/post_confirm_delete.html", {"post": post})


@login_required
def bookmarks(request):
    saved = Bookmark.objects.filter(user=request.user).select_related("post", "post__author", "post__category")
    return render(request, "dashboard/bookmarks.html", {"bookmarks": saved})


@login_required
def analytics(request):
    posts = Post.objects.filter(author=request.user).annotate(like_total=Count("likes"), comment_total=Count("comments"))
    return render(request, "dashboard/analytics.html", {"posts": posts})
