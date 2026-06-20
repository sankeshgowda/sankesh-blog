from django.urls import path

from newsletter import views

app_name = "newsletter"

urlpatterns = [path("subscribe/", views.subscribe, name="subscribe")]
