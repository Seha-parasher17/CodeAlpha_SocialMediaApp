from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.home, name="home"),
    path("post/new/", views.create_post, name="create_post"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/<int:pk>/like/", views.toggle_like, name="toggle_like"),
]
