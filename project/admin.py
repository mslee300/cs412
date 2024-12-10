from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, University, Region, Post, Comment, Reply


# Custom User Admin
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_superuser', 'university', 'region')
    list_filter = ('is_staff', 'is_superuser', 'university', 'region')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('university', 'region')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'university', 'region', 'is_staff', 'is_superuser'),
        }),
    )


# Register other models
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'region')
    search_fields = ('name', 'short_name')


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'university', 'region', 'created_at')
    search_fields = ('title', 'author__email')
    list_filter = ('university', 'region', 'created_at')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'created_at')
    search_fields = ('post__title', 'author__email', 'content')


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('comment', 'author', 'content', 'created_at')
    search_fields = ('comment__content', 'author__email', 'content')


# Register models with the admin site
admin.site.register(User, UserAdmin)
admin.site.register(University, UniversityAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
