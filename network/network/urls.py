
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("savepost", views.savepost, name="savepost"),
    path("posts", views.posts, name="posts"),
    path("profile", views.profile, name="profile"),
    path("checkauth", views.checkauth, name="checkauth"),
    path("followunfollow", views.followunfollow, name="followunfollow"),
    path("edit", views.edit, name="edit"),
    path("likeunlike", views.likeunlike, name="likeunlike"),
]
