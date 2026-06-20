from django.urls import path

from dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_home, name="home"),
    path("posts/", views.my_posts, name="my_posts"),
    path("posts/create/", views.post_create, name="post_create"),
    path("posts/<slug:slug>/edit/", views.post_update, name="post_update"),
    path("posts/<slug:slug>/delete/", views.post_delete, name="post_delete"),
    path("bookmarks/", views.bookmarks, name="bookmarks"),
    path("analytics/", views.analytics, name="analytics"),
]
