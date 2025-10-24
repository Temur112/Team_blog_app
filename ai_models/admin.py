from django.contrib import admin
from django.utils.html import format_html
from .models import AIModelCategory, AIModel


@admin.register(AIModelCategory)
class AIModelCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color_display', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def color_display(self, obj):
        return format_html(
            '<span style="color: {};">●</span> {}',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Color'


@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'version', 'model_type', 'status', 'is_public', 
        'success_rate_display', 'total_inferences', 'created_by', 'created_at'
    ]
    list_filter = ['status', 'model_type', 'is_public', 'framework', 'created_at']
    search_fields = ['name', 'description', 'created_by__username']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['team_members']
    readonly_fields = ['total_inferences', 'successful_inferences', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'version', 'model_type', 'category')
        }),
        ('Model Files', {
            'fields': ('model_file', 'config_file', 'framework')
        }),
        ('Performance Metrics', {
            'fields': ('accuracy', 'precision', 'recall', 'f1_score')
        }),
        ('Configuration', {
            'fields': ('input_format', 'output_format', 'max_input_length', 'batch_size')
        }),
        ('Status & Permissions', {
            'fields': ('status', 'is_public', 'created_by', 'team_members')
        }),
        ('Statistics', {
            'fields': ('total_inferences', 'successful_inferences'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_trained'),
            'classes': ('collapse',)
        }),
    )
    
    def success_rate_display(self, obj):
        rate = obj.success_rate
        color = 'green' if rate >= 90 else 'orange' if rate >= 70 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color,
            rate
        )
    success_rate_display.short_description = 'Success Rate'


# Inference-related admin classes removed - functionality disabled