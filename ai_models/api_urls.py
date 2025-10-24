from django.urls import path
from . import api_views

# API endpoints with separate namespace
urlpatterns = [
    path('models/', api_views.model_list, name='api_model_list'),
    path('models/<slug:slug>/', api_views.model_detail, name='api_model_detail'),
    # Inference API endpoints disabled for now
    # path('models/<int:model_id>/inference/', api_views.run_inference, name='api_run_inference'),
    # path('inference/<int:inference_id>/feedback/', api_views.submit_feedback, name='api_submit_feedback'),
    path('user/inferences/', api_views.user_inference_history, name='api_user_inferences'),
]
