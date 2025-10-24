from django.urls import path
from . import views

app_name = 'ai_models'

# Regular Django views
urlpatterns = [
    path('', views.model_list_view, name='model_list'),
    path('create/', views.create_model_view, name='create_model'),
    path('my-models/', views.my_models_view, name='my_models'),
    path('create-category/', views.create_category_view, name='create_category'),
    path('model/<slug:slug>/', views.model_detail_view, name='model_detail'),
    path('model/<slug:slug>/edit/', views.edit_model_view, name='edit_model'),
    # Inference URLs disabled for now
    # path('model/<slug:slug>/inference/', views.inference_interface_view, name='inference_interface'),
    # path('inference/<int:inference_id>/', views.inference_result_view, name='inference_result'),
    path('dashboard/', views.user_dashboard_view, name='user_dashboard'),
]
