from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
import time
import json
from .models import AIModel, InferenceRequest, ModelFeedback, AIModelCategory


class AIModelCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModelCategory
        fields = ['id', 'name', 'slug', 'description', 'color']


class AIModelSerializer(serializers.ModelSerializer):
    category = AIModelCategorySerializer(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    success_rate = serializers.ReadOnlyField()
    
    class Meta:
        model = AIModel
        fields = [
            'id', 'name', 'slug', 'description', 'model_type', 'category',
            'version', 'framework', 'accuracy', 'precision', 'recall', 'f1_score',
            'input_format', 'output_format', 'max_input_length', 'batch_size',
            'status', 'is_public', 'created_by', 'success_rate',
            'total_inferences', 'successful_inferences', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_by', 'total_inferences', 'successful_inferences']


class InferenceRequestSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source='model.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = InferenceRequest
        fields = [
            'id', 'model', 'model_name', 'user', 'user_name',
            'input_data', 'parameters', 'status', 'result',
            'error_message', 'processing_time', 'memory_usage',
            'created_at', 'started_at', 'completed_at'
        ]
        read_only_fields = ['user', 'status', 'result', 'error_message', 'processing_time', 'memory_usage']


class ModelFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelFeedback
        fields = ['id', 'inference_request', 'feedback_type', 'comment', 'rating', 'created_at']
        read_only_fields = ['user']


@api_view(['GET'])
def model_list(request):
    """List all available AI models"""
    models = AIModel.objects.filter(is_public=True, status='ready')
    serializer = AIModelSerializer(models, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def model_detail(request, slug):
    """Get details of a specific AI model"""
    model = get_object_or_404(AIModel, slug=slug, is_public=True)
    serializer = AIModelSerializer(model)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_inference(request, model_id):
    """Run inference on an AI model"""
    model = get_object_or_404(AIModel, id=model_id, is_public=True, status='ready')
    
    # Validate input data
    input_data = request.data.get('input_data')
    parameters = request.data.get('parameters', {})
    
    if not input_data:
        return Response(
            {'error': 'input_data is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create inference request
    inference_request = InferenceRequest.objects.create(
        model=model,
        user=request.user,
        input_data=input_data,
        parameters=parameters,
        status='pending'
    )
    
    try:
        # Update status to processing
        inference_request.status = 'processing'
        inference_request.started_at = timezone.now()
        inference_request.save()
        
        # Simulate model inference (replace with actual model loading and inference)
        start_time = time.time()
        
        # This is where you would load your actual model and run inference
        # For now, we'll simulate the process
        result = simulate_model_inference(model, input_data, parameters)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Update inference request with results
        inference_request.result = result
        inference_request.status = 'completed'
        inference_request.processing_time = processing_time
        inference_request.completed_at = timezone.now()
        inference_request.save()
        
        # Update model statistics
        model.increment_inference_count(success=True)
        
        serializer = InferenceRequestSerializer(inference_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        # Handle inference errors
        inference_request.status = 'failed'
        inference_request.error_message = str(e)
        inference_request.completed_at = timezone.now()
        inference_request.save()
        
        model.increment_inference_count(success=False)
        
        return Response(
            {'error': f'Inference failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_feedback(request, inference_id):
    """Submit feedback for an inference result"""
    inference_request = get_object_or_404(InferenceRequest, id=inference_id)
    
    # Check if user already provided feedback
    existing_feedback = ModelFeedback.objects.filter(
        inference_request=inference_request,
        user=request.user
    ).first()
    
    if existing_feedback:
        return Response(
            {'error': 'Feedback already submitted for this inference'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = ModelFeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(
            inference_request=inference_request,
            user=request.user
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_inference_history(request):
    """Get user's inference history"""
    inferences = InferenceRequest.objects.filter(user=request.user).order_by('-created_at')
    serializer = InferenceRequestSerializer(inferences, many=True)
    return Response(serializer.data)


def simulate_model_inference(model, input_data, parameters):
    """
    Simulate model inference - replace this with actual model loading and inference
    This is a placeholder that returns mock results based on model type
    """
    if model.model_type == 'text_classification':
        return {
            'predictions': [
                {'label': 'positive', 'confidence': 0.85},
                {'label': 'negative', 'confidence': 0.15}
            ],
            'predicted_class': 'positive'
        }
    elif model.model_type == 'sentiment_analysis':
        return {
            'sentiment': 'positive',
            'confidence': 0.78,
            'scores': {
                'positive': 0.78,
                'negative': 0.22
            }
        }
    elif model.model_type == 'text_generation':
        return {
            'generated_text': 'This is a generated response based on the input.',
            'tokens_generated': 15
        }
    elif model.model_type == 'image_classification':
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
            'model_type': model.model_type
        }
