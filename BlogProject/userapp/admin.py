from django.contrib import admin
from .models import UserProfile,loginTable,UserPosts,BlogPost, BlogComment, BlockedUsers
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(loginTable)
admin.site.register(UserPosts)
admin.site.register(BlogPost)
admin.site.register(BlogComment)
admin.site.register(BlockedUsers)
