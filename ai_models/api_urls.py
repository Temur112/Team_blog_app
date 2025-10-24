from django.urls import path
from . import api_views

# API endpoints
urlpatterns = [
    path('models/', api_views.model_list, name='api_model_list'),
    path('models/<slug:slug>/', api_views.model_detail, name='api_model_detail'),
]
