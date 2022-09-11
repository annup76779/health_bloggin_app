from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    return "%s_blog_post_image.%s"%(str(uuid4()), ext)

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField()
    image = models.ImageField(null=True, blank = True, upload_to=get_file_path)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "%s %s"%(self.id ,self.title)


class Comments(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)


class ReplyOfComments(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    comment= models.ForeignKey(Comments, on_delete=models.CASCADE)
    reply = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)


class Vote(models.Model):
    VOTE_TYPE = (
            ("upvote", "upvote"),
            ("downvote", "downvote"),
        )
    post= models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length = 10,choices=VOTE_TYPE)
