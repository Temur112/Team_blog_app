from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import AIModel, AIModelCategory, InferenceRequest, ModelFeedback
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


@login_required
def inference_interface_view(request, slug):
    """Interface for running inference on a model"""
    model = get_object_or_404(AIModel, slug=slug, is_public=True)
    
    if request.method == 'POST':
        try:
            input_data = request.POST.get('input_data')
            parameters = request.POST.get('parameters', '{}')
            
            if not input_data:
                messages.error(request, 'Input data is required.')
                return redirect('ai_models:inference_interface', slug=slug)
            
            # Parse parameters if provided
            try:
                parameters_dict = json.loads(parameters) if parameters else {}
            except json.JSONDecodeError:
                parameters_dict = {}
            
            # Create inference request
            inference_request = InferenceRequest.objects.create(
                model=model,
                user=request.user,
                input_data=input_data,
                parameters=parameters_dict,
                status='pending'
            )
            
            # For now, we'll simulate the inference process
            # In a real implementation, this would be handled by Celery or similar
            inference_request.status = 'processing'
            inference_request.save()
            
            # Simulate processing
            import time
            time.sleep(1)  # Simulate processing time
            
            # Mock result based on model type
            result = get_mock_result(model.model_type, input_data)
            
            inference_request.result = result
            inference_request.status = 'completed'
            inference_request.save()
            
            model.increment_inference_count(success=True)
            
            messages.success(request, 'Inference completed successfully!')
            return redirect('ai_models:inference_result', inference_id=inference_request.id)
            
        except Exception as e:
            messages.error(request, f'Error running inference: {str(e)}')
    
    context = {
        'model': model,
    }
    
    return render(request, 'ai_models/inference_interface.html', context)


@login_required
def inference_result_view(request, inference_id):
    """Display inference result"""
    inference_request = get_object_or_404(InferenceRequest, id=inference_id, user=request.user)
    
    # Check if user has already provided feedback
    existing_feedback = ModelFeedback.objects.filter(
        inference_request=inference_request,
        user=request.user
    ).first()
    
    if request.method == 'POST':
        feedback_type = request.POST.get('feedback_type')
        comment = request.POST.get('comment', '')
        rating = request.POST.get('rating')
        
        if not existing_feedback and feedback_type:
            ModelFeedback.objects.create(
                inference_request=inference_request,
                user=request.user,
                feedback_type=feedback_type,
                comment=comment,
                rating=int(rating) if rating else None
            )
            messages.success(request, 'Thank you for your feedback!')
            return redirect('ai_models:inference_result', inference_id=inference_id)
    
    context = {
        'inference_request': inference_request,
        'existing_feedback': existing_feedback,
    }
    
    return render(request, 'ai_models/inference_result.html', context)


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


def get_mock_result(model_type, input_data):
    """Generate mock results for different model types"""
    if model_type == 'text_classification':
        return {
            'predictions': [
                {'label': 'positive', 'confidence': 0.85},
                {'label': 'negative', 'confidence': 0.15}
            ],
            'predicted_class': 'positive'
        }
    elif model_type == 'sentiment_analysis':
        return {
            'sentiment': 'positive',
            'confidence': 0.78,
            'scores': {
                'positive': 0.78,
                'negative': 0.22
            }
        }
    elif model_type == 'text_generation':
        return {
            'generated_text': 'This is a generated response based on your input. The model has processed your request and provided this output.',
            'tokens_generated': 25
        }
    elif model_type == 'image_classification':
        return {
            'predictions': [
                {'label': 'cat', 'confidence': 0.92},
                {'label': 'dog', 'confidence': 0.08}
            ],
            'predicted_class': 'cat'
        }
    else:
        return {
            'result': 'Model inference completed successfully',
            'input_processed': True,
            'model_type': model_type,
            'processed_input': input_data[:100] + '...' if len(str(input_data)) > 100 else input_data
        }