from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import AIModel, AIModelCategory
from .forms import AIModelForm, AIModelCategoryForm


def model_list_view(request):
    """Display list of available AI models"""
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')
    model_type = request.GET.get('type')
    
    models = AIModel.objects.filter(is_public=True, status='ready')
    
    # Filter by category
    if category_slug:
        models = models.filter(category__slug=category_slug)
    
    # Filter by model type
    if model_type:
        models = models.filter(model_type=model_type)
    
    # Search functionality
    if search_query:
        models = models.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(models, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories and model types for filters
    categories = AIModelCategory.objects.all()
    model_types = AIModel.MODEL_TYPES
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'model_types': model_types,
        'current_category': category_slug,
        'current_type': model_type,
        'search_query': search_query,
    }
    
    return render(request, 'ai_models/model_list.html', context)


def model_detail_view(request, slug):
    """Display detailed view of an AI model"""
    model = get_object_or_404(AIModel, slug=slug, is_public=True)
    
    # Get recent inference requests for this model
    recent_inferences = InferenceRequest.objects.filter(
        model=model
    ).order_by('-created_at')[:10]
    
    context = {
        'model': model,
        'recent_inferences': recent_inferences,
    }
    
    return render(request, 'ai_models/model_detail.html', context)


# Inference functionality disabled - views removed


@login_required
def user_dashboard_view(request):
    """User dashboard showing their model management"""
    # Get user's created models
    user_models = AIModel.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Pagination for user's models
    paginator = Paginator(user_models, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_models = user_models.count()
    public_models = user_models.filter(is_public=True).count()
    ready_models = user_models.filter(status='ready').count()
    
    context = {
        'page_obj': page_obj,
        'total_models': total_models,
        'public_models': public_models,
        'ready_models': ready_models,
    }
    
    return render(request, 'ai_models/user_dashboard.html', context)


@login_required
def create_model_view(request):
    """Create a new AI model"""
    if request.method == 'POST':
        form = AIModelForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            model = form.save()
            messages.success(request, f'AI model "{model.name}" has been created successfully!')
            return redirect('ai_models:model_detail', slug=model.slug)
    else:
        form = AIModelForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Create New AI Model'
    }
    
    return render(request, 'ai_models/model_form.html', context)


@login_required
def edit_model_view(request, slug):
    """Edit an existing AI model"""
    model = get_object_or_404(AIModel, slug=slug)
    
    # Check if user can edit this model
    if not (request.user == model.created_by or request.user in model.team_members.all() or request.user.is_staff):
        messages.error(request, 'You do not have permission to edit this model.')
        return redirect('ai_models:model_detail', slug=slug)
    
    if request.method == 'POST':
        form = AIModelForm(request.POST, request.FILES, instance=model, user=request.user)
        if form.is_valid():
            model = form.save()
            messages.success(request, f'AI model "{model.name}" has been updated successfully!')
            return redirect('ai_models:model_detail', slug=model.slug)
    else:
        form = AIModelForm(instance=model, user=request.user)
    
    context = {
        'form': form,
        'model': model,
        'title': f'Edit {model.name}'
    }
    
    return render(request, 'ai_models/model_form.html', context)


@login_required
def create_category_view(request):
    """Create a new AI model category"""
    if request.method == 'POST':
        form = AIModelCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" has been created successfully!')
            return redirect('ai_models:model_list')
    else:
        form = AIModelCategoryForm()
    
    context = {
        'form': form,
        'title': 'Create New Category'
    }
    
    return render(request, 'ai_models/category_form.html', context)


@login_required
def my_models_view(request):
    """Display user's created models"""
    models = AIModel.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(models, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'title': 'My AI Models'
    }
    
    return render(request, 'ai_models/my_models.html', context)


# Mock inference function removed - inference functionality disabled