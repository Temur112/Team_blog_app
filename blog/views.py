from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Post, Tag, Comment
from .forms import PostForm, CommentForm, SearchForm, TagForm

def home(request):
    """Homepage with recent posts"""
    posts = Post.objects.filter(status='published').select_related('author')
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'featured_posts': posts.filter(featured_image__isnull=False)[:3],
    }
    return render(request, 'blog/home.html', context)

def post_list(request):
    """List all published posts"""
    posts = Post.objects.filter(status='published').select_related('author')
    
    # Search functionality
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
    
    # Tag filtering
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'all_tags': Tag.objects.all(),
        'current_tag': tag_slug,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    """Display a single post"""
    post = get_object_or_404(Post, slug=slug, status='published')
    post.increment_views()
    
    # Handle comments
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid() and request.user.is_authenticated:
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comment_form': comment_form,
        'comments': post.comments.filter(is_approved=True),
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def create_post(request):
    """Create a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Post created successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Create'})

@login_required
def edit_post(request, slug):
    """Edit an existing post"""
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Edit', 'post': post})

@login_required
def delete_post(request, slug):
    """Delete a post"""
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('blog:home')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def user_profile(request, username):
    """Display user profile with their posts"""
    from django.contrib.auth.models import User
    
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user, status='published')
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile_user': user,
        'page_obj': page_obj,
        'total_posts': posts.count(),
    }
    return render(request, 'accounts/profile.html', context)

def tag_posts(request, slug):
    """Display posts for a specific tag"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published')
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'blog/tag_posts.html', context)

def our_work(request):
    """Display posts tagged with 'Our Work' or 'Our'"""
    # Get posts tagged with 'Our Work' or any tag containing 'our'
    posts = Post.objects.filter(
        tags__name__icontains='our',
        status='published'
    ).distinct().select_related('author')
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'title': 'Our Work',
        'description': 'Showcasing our team\'s projects, research, and achievements'
    }
    
    return render(request, 'blog/our_work.html', context)

@login_required
def create_tag(request):
    """Create a new tag"""
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            messages.success(request, f'Tag "{tag.name}" has been created successfully!')
            return redirect('blog:post_list')
    else:
        form = TagForm()
    
    context = {
        'form': form,
        'title': 'Create New Tag'
    }
    
    return render(request, 'blog/tag_form.html', context)

# AJAX endpoints for enhanced functionality
@login_required
def upload_image(request):
    """Handle image uploads via AJAX"""
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        # Process and save image
        # This is handled by markdownx, but we can add custom logic here
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})