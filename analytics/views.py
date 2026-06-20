from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils import timezone

from blog.models import Comment, Post


@staff_member_required
def overview(request):
    since = timezone.now() - timedelta(days=7)
    context = {
        "total_posts": Post.objects.count(),
        "total_views": Post.objects.aggregate(total=Sum("view_count"))["total"] or 0,
        "popular_posts": Post.objects.order_by("-view_count")[:10],
        "trending_posts": Post.published.filter(created_at__gte=since).order_by("-view_count")[:10],
        "comment_count": Comment.objects.count(),
    }
    return render(request, "dashboard/admin_analytics.html", context)
