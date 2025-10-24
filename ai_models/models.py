from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import json


class AIModelCategory(models.Model):
    """Categories for organizing AI models"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff')  # Hex color
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "AI Model Categories"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class AIModel(models.Model):
    """AI models trained by the team"""
    MODEL_TYPES = [
        ('text_classification', 'Text Classification'),
        ('text_generation', 'Text Generation'),
        ('image_classification', 'Image Classification'),
        ('object_detection', 'Object Detection'),
        ('sentiment_analysis', 'Sentiment Analysis'),
        ('named_entity_recognition', 'Named Entity Recognition'),
        ('machine_translation', 'Machine Translation'),
        ('question_answering', 'Question Answering'),
        ('summarization', 'Text Summarization'),
        ('custom', 'Custom Model'),
    ]
    
    STATUS_CHOICES = [
        ('training', 'Training'),
        ('ready', 'Ready'),
        ('deployed', 'Deployed'),
        ('maintenance', 'Maintenance'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    model_type = models.CharField(max_length=50, choices=MODEL_TYPES)
    category = models.ForeignKey(AIModelCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='models')
    
    # Model metadata
    version = models.CharField(max_length=20, default='1.0')
    framework = models.CharField(max_length=50, default='PyTorch')  # PyTorch, TensorFlow, etc.
    model_file = models.FileField(upload_to='ai_models/%Y/%m/', blank=True, null=True)
    config_file = models.FileField(upload_to='ai_models/config/%Y/%m/', blank=True, null=True)
    
    # Model performance metrics
    accuracy = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)
    f1_score = models.FloatField(null=True, blank=True)
    
    # Model configuration
    input_format = models.JSONField(default=dict, help_text="Expected input format and parameters")
    output_format = models.JSONField(default=dict, help_text="Output format specification")
    max_input_length = models.PositiveIntegerField(default=512)
    batch_size = models.PositiveIntegerField(default=1)
    
    # Status and permissions
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='training')
    is_public = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_ai_models')
    team_members = models.ManyToManyField(User, blank=True, related_name='team_ai_models')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_trained = models.DateTimeField(null=True, blank=True)
    
    # Usage statistics (kept for future use)
    total_inferences = models.PositiveIntegerField(default=0)
    successful_inferences = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['model_type']),
            models.Index(fields=['is_public']),
        ]
    
    def __str__(self):
        return f"{self.name} v{self.version}"
    
    def get_absolute_url(self):
        return reverse('ai_models:model_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.version}")
        super().save(*args, **kwargs)
    
    @property
    def success_rate(self):
        """Calculate success rate of inferences"""
        if self.total_inferences == 0:
            return 0
        return (self.successful_inferences / self.total_inferences) * 100


# Inference-related models removed - functionality disabled