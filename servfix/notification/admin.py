from django.contrib import admin

from .models import *

admin.site.register(Post)
admin.site.register(PostNews)
admin.site.register(PostForSpecificProvider)
admin.site.register(ImmediateNotification)