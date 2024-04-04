from django.contrib import admin

from .models import Post,PostNews

admin.site.register(Post)
admin.site.register(PostNews)