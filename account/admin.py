from django.contrib import admin

from .models import Profile, Post, Category, Tag, Like, Bookmark
from comments.models import Comment

admin.site.register(Comment)

admin.site.register([Profile, Post, Category, Tag, Like, Bookmark])
