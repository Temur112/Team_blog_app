from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Tag, Comment, PostImage

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    fields = ['image', 'alt_text']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at', 'views']
    list_filter = ['status', 'created_at', 'tags']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    inlines = [PostImageInline]
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'body', 'excerpt', 'featured_image')
        }),
        ('Metadata', {
            'fields': ('author', 'status', 'tags')
        }),
        ('SEO', {
            'fields': ('views',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'author__username']
    raw_id_fields = ['post', 'author']
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'alt_text', 'uploaded_at']
    search_fields = ['post__title', 'alt_text']