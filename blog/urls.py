from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('our-work/', views.our_work, name='our_work'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<slug:slug>/', views.edit_post, name='edit_post'),
    path('delete/<slug:slug>/', views.delete_post, name='delete_post'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    path('create-tag/', views.create_tag, name='create_tag'),
    
    # AJAX endpoints
    path('upload-image/', views.upload_image, name='upload_image'),
]