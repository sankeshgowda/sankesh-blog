from django.urls import path

from blog import views

app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),
    path("blog/", views.blog_list, name="list"),
    path("blog/<slug:slug>/", views.blog_detail, name="detail"),
    path("blog/<slug:slug>/like/", views.toggle_like, name="like"),
    path("blog/<slug:slug>/bookmark/", views.toggle_bookmark, name="bookmark"),
    path("categories/", views.categories, name="categories"),
    path("categories/<slug:slug>/", views.category_detail, name="category"),
    path("tags/", views.tags, name="tags"),
    path("tags/<slug:slug>/", views.tag_detail, name="tag"),
    path("search/", views.search, name="search"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("author/<str:username>/", views.author_profile, name="author"),
]
