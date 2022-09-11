from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BlogPostForm, UserForm
from .models import *
from django.contrib.auth.models import User


# Create your views here.

def view_blog(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    # comments = Comments.objects.get(post=blog.id)
    print({comment: [reply for reply in comment.replyofcomments_set.all()] for comment in blog.comments_set.all()})
    return render(request, "app/view_blog.html", {
            'blog': blog, 
            "user" : request.user, 
            "comments": {
                comment: [reply for reply in comment.replyofcomments_set.all()] for comment in blog.comments_set.all()
                },
            "upvotes": Vote.objects.get()
            }
        )

def post_blog(request):
    form  = BlogPostForm()
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/view_blog")
        else:
            return HttpResponse("Gadbad h re vaba")
    context = {"form":form}
    return render(request, "app/blog_post.html", context)


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if not User.objects.filter(username = cleaned_data["username"]).exists():
                user = User.objects.create_user(**cleaned_data)
                user.save()
            else:
                pass
    return render(request, "app/register.html", {"form": UserForm()})


def vote(request, post_id, vote_type):
    if request.user.is_authenticated:
        user = request.user
        post = BlogPost.objects.get(id = post_id)
        vote = Vote.objects.filter(user = user, post = post)
        if not vote.exists():
            vote = Vote(user = user, post = post, vote_type=vote_type)
            vote.save()
        else:
            vote = vote.get()
            vote.vote_type = vote_type
            vote.save()

        return redirect("view_blog", post_id)
    else:
        return redirect("login_user")


def comment_post(request, post_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            try:
                is_reply_box = bool(request.POST.get("is_reply_box"))
            except ValueError:
                is_reply_box = False
            comment_id_box = request.POST.get("comment_id_box")
            actual_comment = request.POST.get("actual_comment")
            if actual_comment.strip() == "":
                return redirect("view_blog", post_id)
            if is_reply_box:
                reply = ReplyOfComments(user = request.user, comment = Comments.objects.get(id=comment_id_box), reply=actual_comment)
                reply.save()
            else:
                comment = Comments(user = request.user, post = BlogPost.objects.get(id=post_id), comment = actual_comment)
                comment.save()
            return redirect("view_blog", post_id)
        else:
            return HttpResponse("Method not allowed")
    else:
        return redirect("login_user")