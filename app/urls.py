from django.urls import path
from . import views

urlpatterns = [
    path("view_blog/<int:blog_id>", views.view_blog, name="view_blog"),
    path("post_blog/", views.post_blog, name="post_blog"),
    path("register/", views.register, name="register"),
    path("downvote/<int:post_id>/<str:vote_type>", views.vote, name="vote"),
    path("downvote/<int:post_id>", views.comment_post, name="comment_post"),
]