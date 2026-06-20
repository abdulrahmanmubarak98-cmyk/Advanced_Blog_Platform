from django.contrib import admin

from .models import Profile, Post, Category, Tag, Comment, Like, Bookmark

admin.site.register([Profile, Post, Category, Tag, Comment, Like, Bookmark])
