from blog.models import Category


def site_context(request):
    return {
        "site_name": "Sankesh Blog",
        "nav_categories": Category.objects.all()[:8],
    }
