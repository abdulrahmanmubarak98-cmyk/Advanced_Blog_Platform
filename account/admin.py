from django.contrib import admin

from .models import Profile, Post, Category, Tag

admin.site.register([Profile, Post, Category, Tag])
