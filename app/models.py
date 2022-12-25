from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
import os

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    return "%s_blog_post_image.%s"%(str(uuid4()), ext)


class Categories(models.Model):
    name = models.CharField(max_length=100, unique=True) # no repeated value will be placed here ever.
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "%s"%self.name

# Create your models here.
class BlogPost(models.Model):
    """
        CREATE TABLE IF EXISTS blog_post(
            ID INTEGER PRIMARY KEY AUTOINCREMENT
            `title` VARCHAR(300),
            `body` TEXT,
            `image` VARCHAR(50),
            `date_created` DATETIME
        )
    """
    title = models.CharField(max_length=300)
    category = models.ForeignKey(Categories, on_delete = models.CASCADE)
    body = models.TextField()
    image = models.ImageField(null=True, blank = True, upload_to=get_file_path)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return "%d %s"%(self.id ,self.title)


class Comments(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment = models.TextField()
    isApproved = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "%d %s"%(self.id, self.comment)


class ReplyOfComments(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    comment= models.ForeignKey(Comments, on_delete=models.CASCADE)
    reply = models.TextField()
    isApproved = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "%d %s"%(self.id, self.reply)


class Vote(models.Model):
    # it is advised to use tuple instead of dict and list.
    VOTE_TYPE = (
            ("upvote", "Upvote"),
            ("downvote", "Downvote"),
        )
    post= models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length = 10,choices=VOTE_TYPE)
 