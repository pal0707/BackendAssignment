from django.contrib import admin
from .models import User, Post

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name','last_name','username', 'is_active']

admin.site.register(User, UserAdmin)

class UserPoastAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content','author','created_at', 'is_active']

admin.site.register(Post, UserPoastAdmin)
