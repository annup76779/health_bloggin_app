# Generated by Django 4.1.1 on 2022-09-11 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_upvote_alter_blogpost_image_alter_comments_user_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Upvote",
        ),
    ]
