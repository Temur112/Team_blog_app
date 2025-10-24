from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import AIModel, AIModelCategory


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


# Inference-related API endpoints removed - functionality disabled
