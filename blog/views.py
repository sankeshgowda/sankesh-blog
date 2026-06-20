from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from blog.forms import CommentForm
from blog.models import Bookmark, Category, Comment, Like, Post, Tag
from newsletter.forms import NewsletterSubscriberForm


def _paginate(request, queryset, per_page=9):
    return Paginator(queryset, per_page).get_page(request.GET.get("page"))


def home(request):
    posts = Post.published.select_related("author", "category").prefetch_related("tags")
    context = {
        "featured_posts": posts[:5],
        "trending_posts": posts.order_by("-view_count", "-created_at")[:6],
        "latest_posts": posts[:9],
        "popular_categories": Category.objects.annotate(post_total=Count("posts")).order_by("-post_total")[:8],
        "newsletter_form": NewsletterSubscriberForm(),
    }
    return render(request, "home.html", context)


def blog_list(request):
    posts = Post.published.select_related("author", "category").prefetch_related("tags")
    return render(request, "blog/blog_list.html", {"page_obj": _paginate(request, posts)})


def blog_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related("author", "category").prefetch_related("tags"), slug=slug)
    if not post.is_live and (not request.user.is_authenticated or request.user != post.author):
        messages.warning(request, "This article is not published yet.")
        return redirect("blog:list")

    Post.objects.filter(pk=post.pk).update(view_count=post.view_count + 1)
    post.view_count += 1

    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment posted.")
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    related_posts = (
        Post.published.filter(Q(category=post.category) | Q(tags__in=post.tags.all()))
        .exclude(pk=post.pk)
        .distinct()[:4]
    )
    comments = post.comments.filter(parent__isnull=True).select_related("user").prefetch_related("replies__user")
    context = {
        "post": post,
        "comment_form": form,
        "comments": comments,
        "related_posts": related_posts,
        "liked": request.user.is_authenticated and Like.objects.filter(post=post, user=request.user).exists(),
        "bookmarked": request.user.is_authenticated and Bookmark.objects.filter(post=post, user=request.user).exists(),
    }
    return render(request, "blog/blog_detail.html", context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.published.filter(category=category).select_related("author", "category")
    return render(request, "blog/blog_list.html", {"page_obj": _paginate(request, posts), "heading": category.name})


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.published.filter(tags=tag).select_related("author", "category")
    return render(request, "blog/blog_list.html", {"page_obj": _paginate(request, posts), "heading": f"#{tag.name}"})


def search(request):
    query = request.GET.get("q", "").strip()
    posts = Post.published.none()
    if query:
        posts = Post.published.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()
    return render(request, "blog/blog_list.html", {"page_obj": _paginate(request, posts), "query": query, "heading": "Search"})


def categories(request):
    return render(request, "blog/categories.html", {"categories": Category.objects.annotate(post_total=Count("posts"))})


def tags(request):
    return render(request, "blog/tags.html", {"tags": Tag.objects.annotate(post_total=Count("posts"))})


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def author_profile(request, username):
    author = get_object_or_404(get_user_model(), username=username)
    posts = Post.published.filter(author__username=username).select_related("category", "author")
    return render(request, "blog/author_profile.html", {"author_obj": author, "page_obj": _paginate(request, posts)})


@login_required
@require_POST
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    obj, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        obj.delete()
    return redirect(post.get_absolute_url())


@login_required
@require_POST
def toggle_bookmark(request, slug):
    post = get_object_or_404(Post, slug=slug)
    obj, created = Bookmark.objects.get_or_create(post=post, user=request.user)
    if not created:
        obj.delete()
    return redirect(post.get_absolute_url())
