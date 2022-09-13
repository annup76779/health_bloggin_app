from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(BlogPost)
admin.site.register(Comments)
admin.site.register(ReplyOfComments)
admin.site.register(Vote)
admin.site.register(Categories)