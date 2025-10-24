# AI Models Module for Team Blog App

This module provides a comprehensive AI model management and inference system for the Django blog application. It allows teams to upload, manage, and deploy AI models trained by the team, with a user-friendly interface for running inferences.

## Features

### 🚀 Core Features
- **Model Management**: Upload, version, and manage AI models
- **Inference Interface**: User-friendly UI for running model inferences
- **REST API**: Complete API for programmatic access
- **User Dashboard**: Track inference history and statistics
- **Feedback System**: Collect user feedback on model predictions
- **Performance Monitoring**: Track model performance and usage statistics

### 📊 Model Types Supported
- Text Classification
- Sentiment Analysis
- Text Generation
- Image Classification
- Object Detection
- Named Entity Recognition
- Machine Translation
- Question Answering
- Text Summarization
- Custom Models

### 🔧 Technical Features
- **Django REST Framework**: RESTful API endpoints
- **CORS Support**: Cross-origin resource sharing
- **File Upload**: Support for model files and configurations
- **Database Optimization**: Proper indexing and relationships
- **Admin Interface**: Full Django admin integration
- **Template System**: Responsive Bootstrap-based UI

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations ai_models
python manage.py migrate
```

### 3. Create Sample Data
```bash
python manage.py create_sample_ai_models
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

## Usage

### Web Interface

1. **Browse Models**: Visit `/ai-models/` to see all available models
2. **Model Details**: Click on any model to view detailed information
3. **Run Inference**: Use the inference interface to test models
4. **User Dashboard**: Track your inference history at `/ai-models/dashboard/`

### API Endpoints

#### List Models
```http
GET /api/ai-models/models/
```

#### Get Model Details
```http
GET /api/ai-models/models/{slug}/
```

#### Run Inference
```http
POST /api/ai-models/models/{model_id}/inference/
Content-Type: application/json

{
    "input_data": "Your input text here",
    "parameters": {
        "temperature": 0.7,
        "max_length": 100
    }
}
```

#### Submit Feedback
```http
POST /api/ai-models/inference/{inference_id}/feedback/
Content-Type: application/json

{
    "feedback_type": "correct",
    "rating": 5,
    "comment": "Great prediction!"
}
```

#### User Inference History
```http
GET /api/ai-models/user/inferences/
```

## Model Structure

### AIModel
- **Basic Info**: Name, description, version, framework
- **Performance**: Accuracy, precision, recall, F1-score
- **Configuration**: Input/output formats, parameters
- **Status**: Training, ready, deployed, maintenance, archived
- **Permissions**: Public/private access, team members

### InferenceRequest
- **Request Data**: Input data and parameters
- **Results**: Model output and performance metrics
- **Status**: Pending, processing, completed, failed
- **Timestamps**: Created, started, completed times

### ModelFeedback
- **Feedback Types**: Correct, incorrect, partially correct
- **Rating**: 1-5 star rating system
- **Comments**: Optional user comments

## Configuration

### Settings
The module adds several configuration options to `settings.py`:

```python
# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# AI Models Configuration
AI_MODELS_UPLOAD_PATH = 'ai_models/'
AI_MODELS_MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
AI_MODELS_ALLOWED_EXTENSIONS = ['.pkl', '.pth', '.h5', '.onnx', '.pt', '.json', '.yaml', '.yml']
```

## File Structure

```
ai_models/
├── __init__.py
├── admin.py              # Django admin configuration
├── apps.py               # App configuration
├── models.py             # Database models
├── views.py              # Regular Django views
├── api_views.py          # REST API views
├── urls.py               # URL patterns
├── api_urls.py           # API URL patterns
├── management/
│   └── commands/
│       └── create_sample_ai_models.py
└── migrations/
    └── 0001_initial.py
```

## Templates

The module includes responsive Bootstrap-based templates:

- `model_list.html` - Browse available models
- `model_detail.html` - Model information and specifications
- `inference_interface.html` - Run model inference
- `inference_result.html` - View inference results
- `user_dashboard.html` - User's inference history

## Admin Interface

The Django admin interface provides full management capabilities:

- **AIModelCategory**: Manage model categories
- **AIModel**: Manage AI models and their configurations
- **InferenceRequest**: Monitor inference requests
- **ModelFeedback**: Review user feedback
- **ModelDeployment**: Track model deployments

## Security Features

- **Authentication**: User authentication required for inference
- **Permissions**: Public/private model access control
- **Input Validation**: Proper input data validation
- **File Upload Security**: Restricted file types and sizes
- **CORS Configuration**: Controlled cross-origin access

## Performance Features

- **Database Indexing**: Optimized database queries
- **Pagination**: Efficient data loading
- **Caching**: Ready for Redis integration
- **Async Processing**: Celery integration ready

## Future Enhancements

- **Real Model Integration**: Replace mock inference with actual model loading
- **Celery Integration**: Async inference processing
- **Model Versioning**: Advanced version management
- **A/B Testing**: Model comparison features
- **Analytics Dashboard**: Advanced usage analytics
- **Model Marketplace**: Share models between teams

## Contributing

1. Follow Django best practices
2. Add proper tests for new features
3. Update documentation for API changes
4. Ensure backward compatibility

## License

This module is part of the Team Blog App project and follows the same license terms.
