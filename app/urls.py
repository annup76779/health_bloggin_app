from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("view_blog/<int:blog_id>", views.BlogView.as_view(), name="view_blog"),
    path("by_category/", views.ByCategoryView.as_view(), name="by_category"),
    path("post_blog/", views.post_blog, name="post_blog"),
    path("register/", views.register, name="register"),
    path("downvote/<int:post_id>/<str:vote_type>", views.VoteView.as_view(), name="vote"),
    path("comment/<int:post_id>", views.CommentBlog.as_view(), name="comment_post"),
]