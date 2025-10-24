from django import template
from django.contrib.auth.models import User
from blog.models import Tag
import hashlib

register = template.Library()

@register.filter
def md5(email):
    """Generate MD5 hash for Gravatar"""
    return hashlib.md5(email.lower().encode('utf-8')).hexdigest()

@register.simple_tag
def get_all_tags():
    """Get all tags for dropdown"""
    return Tag.objects.all()[:10]  # Limit to 10 most popular tags

@register.filter
def pluralize(value, arg='s'):
    """Simple pluralize filter"""
    try:
        if int(value) != 1:
            return arg
        return ''
    except (ValueError, TypeError):
        return arg