from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ai_models.models import AIModelCategory, AIModel


class Command(BaseCommand):
    help = 'Create sample AI models data'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Natural Language Processing', 'description': 'Models for text analysis and generation', 'color': '#007bff'},
            {'name': 'Computer Vision', 'description': 'Models for image and video analysis', 'color': '#28a745'},
            {'name': 'Machine Learning', 'description': 'General purpose ML models', 'color': '#ffc107'},
            {'name': 'Deep Learning', 'description': 'Neural network based models', 'color': '#dc3545'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = AIModelCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Get or create a user for the models
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write('Created admin user')

        # Create sample AI models
        models_data = [
            {
                'name': 'Sentiment Analysis Model',
                'description': 'A transformer-based model for analyzing sentiment in text. Trained on large-scale social media and review datasets.',
                'model_type': 'sentiment_analysis',
                'category': categories['Natural Language Processing'],
                'version': '2.1',
                'framework': 'PyTorch',
                'accuracy': 0.92,
                'precision': 0.91,
                'recall': 0.93,
                'f1_score': 0.92,
                'input_format': {'text': 'string', 'max_length': 512},
                'output_format': {'sentiment': 'string', 'confidence': 'float', 'scores': 'dict'},
                'max_input_length': 512,
                'status': 'ready',
                'is_public': True,
            },
            {
                'name': 'Text Classification Model',
                'description': 'BERT-based model for multi-class text classification. Supports up to 50 different categories.',
                'model_type': 'text_classification',
                'category': categories['Natural Language Processing'],
                'version': '1.5',
                'framework': 'Transformers',
                'accuracy': 0.89,
                'precision': 0.88,
                'recall': 0.90,
                'f1_score': 0.89,
                'input_format': {'text': 'string', 'categories': 'list'},
                'output_format': {'predicted_class': 'string', 'confidence': 'float', 'all_predictions': 'list'},
                'max_input_length': 256,
                'status': 'ready',
                'is_public': True,
            },
            {
                'name': 'Image Classification Model',
                'description': 'ResNet-based model for image classification. Trained on ImageNet dataset with 1000 classes.',
                'model_type': 'image_classification',
                'category': categories['Computer Vision'],
                'version': '3.0',
                'framework': 'PyTorch',
                'accuracy': 0.95,
                'precision': 0.94,
                'recall': 0.96,
                'f1_score': 0.95,
                'input_format': {'image': 'file', 'format': 'RGB'},
                'output_format': {'predicted_class': 'string', 'confidence': 'float', 'top_predictions': 'list'},
                'max_input_length': 224,
                'status': 'ready',
                'is_public': True,
            },
            {
                'name': 'Text Generation Model',
                'description': 'GPT-style model for creative text generation. Fine-tuned for various writing styles.',
                'model_type': 'text_generation',
                'category': categories['Natural Language Processing'],
                'version': '1.2',
                'framework': 'Transformers',
                'accuracy': 0.85,
                'precision': 0.84,
                'recall': 0.86,
                'f1_score': 0.85,
                'input_format': {'prompt': 'string', 'max_length': 100},
                'output_format': {'generated_text': 'string', 'tokens_generated': 'int'},
                'max_input_length': 1024,
                'status': 'ready',
                'is_public': True,
            },
            {
                'name': 'Named Entity Recognition Model',
                'description': 'SpaCy-based NER model for extracting entities from text. Supports person, organization, location, and more.',
                'model_type': 'named_entity_recognition',
                'category': categories['Natural Language Processing'],
                'version': '1.0',
                'framework': 'SpaCy',
                'accuracy': 0.88,
                'precision': 0.87,
                'recall': 0.89,
                'f1_score': 0.88,
                'input_format': {'text': 'string'},
                'output_format': {'entities': 'list', 'entity_types': 'list'},
                'max_input_length': 512,
                'status': 'ready',
                'is_public': True,
            },
            {
                'name': 'Question Answering Model',
                'description': 'BERT-based QA model for answering questions based on given context. Trained on SQuAD dataset.',
                'model_type': 'question_answering',
                'category': categories['Natural Language Processing'],
                'version': '2.0',
                'framework': 'Transformers',
                'accuracy': 0.87,
                'precision': 0.86,
                'recall': 0.88,
                'f1_score': 0.87,
                'input_format': {'question': 'string', 'context': 'string'},
                'output_format': {'answer': 'string', 'confidence': 'float', 'start_position': 'int'},
                'max_input_length': 512,
                'status': 'ready',
                'is_public': True,
            },
        ]

        for model_data in models_data:
            model, created = AIModel.objects.get_or_create(
                name=model_data['name'],
                version=model_data['version'],
                defaults={
                    **model_data,
                    'created_by': user,
                }
            )
            if created:
                self.stdout.write(f'Created model: {model.name} v{model.version}')
            else:
                self.stdout.write(f'Model already exists: {model.name} v{model.version}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample AI models data!')
        )
