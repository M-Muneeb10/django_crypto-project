from django.contrib import admin
from .models import Post, Category, Comment # Import Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author', 'category')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

# ADD THIS NEW ADMIN REGISTRATION
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments', 'disapprove_comments'] # Add custom actions

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
        self.message_user(request, "Selected comments have been approved.")
    approve_comments.short_description = "Approve selected comments"

    def disapprove_comments(self, request, queryset):
        queryset.update(active=False)
        self.message_user(request, "Selected comments have been disapproved.")
    disapprove_comments.short_description = "Disapprove selected comments"