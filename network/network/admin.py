from django.contrib import admin
from .models import *

# Register your models here.

class FollowAdmin(admin.ModelAdmin):
    list_display = ('following_user_id', 'followed_user_id', 'created_at')
    search_fields = ('following_user_id__username', 'followed_user_id__username')

class PostAdmin(admin.ModelAdmin):
    list_display = ('poster', 'content', 'created_at')
    search_fields = ('poster__username', 'content')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('liking_user_id', 'liked_postid', 'created_at')
    search_fields = ('liking_user_id__username', 'liked_postid__content')

admin.site.register(User)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)