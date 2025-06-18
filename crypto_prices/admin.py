# myfirstproject/blog/admin.py

from django.contrib import admin
from .models import Post, Comment, Category
from tinymce.widgets import TinyMCE # ADD THIS IMPORT
from django.db import models # ADD THIS IMPORT if not already present

# Register your models here.

# Customize the PostAdmin to use TinyMCE
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

    # ADD THIS SECTION to enable TinyMCE for the 'body' field
    formfield_overrides = {
        models.HTMLField: {'widget': TinyMCE()},
    }

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Mark selected comments as approved"

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)