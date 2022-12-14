import json

from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View

from .forms import BlogPostForm, UserForm
from .models import *
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    blogs = BlogPost.objects.all()
    categories = Categories.objects.all()
    return render(request, "app/homepage.html",
                  {'blogs': blogs, "user": request.user, "top_10_blogs": blogs[:10], "categories": categories})

class BlogView(View):
    def get(self, request, blog_id):
        try:
            blog = BlogPost.objects.get(id=blog_id)
            top_blogs = BlogPost.objects.all().order_by('date_created')[:10]
            categories = Categories.objects.all()
            return render(request, "app/view_blog.html", {
                'blog': blog,
                "user": request.user,
                "top_10_blogs": top_blogs,
                "comments": {
                    comment: [reply for reply in comment.replyofcomments_set.filter(isApproved=True).all()] for comment in
                    blog.comments_set.filter(isApproved=True).all()
                },
                "upvotes": Vote.objects.filter(post=blog, vote_type="upvote").count(),
                "downvotes": Vote.objects.filter(post=blog, vote_type="downvote").count(),
                "categories": categories
            }
                          )
        except:
            return redirect("home")


def post_blog(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form = BlogPostForm()
        if request.method == "POST":
            form = BlogPostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect("home")
            else:
                return HttpResponse("Gadbad h re vaba")
        context = {"form": form, "user": request.user, }
        return render(request, "app/blog_post.html", context)
    else:
        return HttpResponse("Login as Super User.<a href='/login/login_user/'>Login</a>")


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if not User.objects.filter(username=cleaned_data["username"]).exists():
                user = User.objects.create_user(**cleaned_data)
                user.save()
                return redirect("login_user")
            else:
                pass
    return render(request, "app/register.html", {"form": UserForm()})


class VoteView(View):
    def get(self, request, post_id, vote_type):
        if request.user.is_authenticated:
            user = request.user
            post = BlogPost.objects.get(id=post_id)
            vote = Vote.objects.filter(user=user, post=post)
            if not vote.exists():
                vote = Vote(user=user, post=post, vote_type=vote_type)
                vote.save()
            else:
                vote = vote.get()
                vote.vote_type = vote_type
                vote.save()
            return JsonResponse(data={"status": True})
        else:
            return JsonResponse(data=dict(status=False, msg="You need to login to continue."))


class CommentBlog(View):
    def post(self, request, post_id):
        if request.user.is_authenticated:
            if request.method == "POST":
                try:
                    is_reply_box = bool(request.POST.get("is_reply_box"))
                except ValueError:
                    # if the is_reply_box flag is not set then it is considered to be a normal comment
                    is_reply_box = False
                comment_id_box = request.POST.get("comment_id_box")
                actual_comment = request.POST.get("actual_comment").strip()
                try:
                    User.objects.get(username=actual_comment[1:])
                    messages.warning(request, "Reply section cannot be empty, you must put some message there.")
                    return redirect("view_blog", post_id)
                except User.DoesNotExist:
                    # don't need to do anything where there is any error
                    pass
                if actual_comment == "":
                    messages.error(request, "Comment section cannot be empty, you must put some message there.")
                    return redirect("view_blog", post_id)
                if is_reply_box:
                    reply = ReplyOfComments(user=request.user, comment=Comments.objects.get(id=comment_id_box),
                                            reply=actual_comment)
                    reply.save()
                else:
                    comment = Comments(user=request.user, post=BlogPost.objects.get(id=post_id), comment=actual_comment)
                    comment.save()
                return redirect("view_blog", post_id)
            else:
                return HttpResponse("Method not allowed")
        else:
            return redirect("login_user")


class ByCategoryView(View):
    def get(self, request, *args, **kwargs):
        try:
            category = int(request.GET.get("category"))
        except ValueError:
            redirect("home")
        blogPost_with_given_category = BlogPost.objects.filter(category=category).all()
        top_blogs = BlogPost.objects.all().order_by('date_created')[:10]
        categories = Categories.objects.all()
        return render(request, "app/homepage.html",
                      {'blogs': blogPost_with_given_category, "user": request.user, "top_10_blogs": top_blogs,
                       "categories": categories})
