from django import forms
from django.core.exceptions import ValidationError
from .models import AIModel, AIModelCategory
import json


class AIModelForm(forms.ModelForm):
    """Form for creating and editing AI models"""
    
    class Meta:
        model = AIModel
        fields = [
            'name', 'description', 'model_type', 'category', 'version',
            'framework', 'model_file', 'config_file', 'accuracy', 'precision',
            'recall', 'f1_score', 'input_format', 'output_format',
            'max_input_length', 'batch_size', 'is_public'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter model name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your AI model...'
            }),
            'model_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'version': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 1.0, 2.1'
            }),
            'framework': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., PyTorch, TensorFlow, Transformers'
            }),
            'model_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pkl,.pth,.h5,.onnx,.pt,.json,.yaml,.yml'
            }),
            'config_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.json,.yaml,.yml'
            }),
            'accuracy': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0',
                'max': '1'
            }),
            'precision': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0',
                'max': '1'
            }),
            'recall': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0',
                'max': '1'
            }),
            'f1_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0',
                'max': '1'
            }),
            'input_format': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '{"text": "string", "max_length": 512}'
            }),
            'output_format': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '{"prediction": "string", "confidence": "float"}'
            }),
            'max_input_length': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'batch_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Make some fields optional
        self.fields['category'].required = False
        self.fields['model_file'].required = False
        self.fields['config_file'].required = False
        self.fields['accuracy'].required = False
        self.fields['precision'].required = False
        self.fields['recall'].required = False
        self.fields['f1_score'].required = False
        
        # Set default values
        self.fields['version'].initial = '1.0'
        self.fields['framework'].initial = 'PyTorch'
        self.fields['max_input_length'].initial = 512
        self.fields['batch_size'].initial = 1
        self.fields['is_public'].initial = True
        
        # Set default input/output formats
        self.fields['input_format'].initial = '{"text": "string", "max_length": 512}'
        self.fields['output_format'].initial = '{"prediction": "string", "confidence": "float"}'
    
    def clean_input_format(self):
        """Validate JSON input format"""
        input_format = self.cleaned_data.get('input_format')
        if input_format:
            try:
                json.loads(input_format)
            except json.JSONDecodeError:
                raise ValidationError('Input format must be valid JSON')
        return input_format
    
    def clean_output_format(self):
        """Validate JSON output format"""
        output_format = self.cleaned_data.get('output_format')
        if output_format:
            try:
                json.loads(output_format)
            except json.JSONDecodeError:
                raise ValidationError('Output format must be valid JSON')
        return output_format
    
    def clean_model_file(self):
        """Validate model file upload"""
        model_file = self.cleaned_data.get('model_file')
        if model_file:
            # Check file size (100MB limit)
            if model_file.size > 100 * 1024 * 1024:
                raise ValidationError('Model file size cannot exceed 100MB')
            
            # Check file extension
            allowed_extensions = ['.pkl', '.pth', '.h5', '.onnx', '.pt', '.json', '.yaml', '.yml']
            file_extension = '.' + model_file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(f'File type {file_extension} is not allowed. Allowed types: {", ".join(allowed_extensions)}')
        
        return model_file
    
    def clean_config_file(self):
        """Validate config file upload"""
        config_file = self.cleaned_data.get('config_file')
        if config_file:
            # Check file size (10MB limit for config files)
            if config_file.size > 10 * 1024 * 1024:
                raise ValidationError('Config file size cannot exceed 10MB')
            
            # Check file extension
            allowed_extensions = ['.json', '.yaml', '.yml']
            file_extension = '.' + config_file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise ValidationError(f'Config file type {file_extension} is not allowed. Allowed types: {", ".join(allowed_extensions)}')
        
        return config_file
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        
        # Validate metrics are between 0 and 1
        metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        for metric in metrics:
            value = cleaned_data.get(metric)
            if value is not None and (value < 0 or value > 1):
                raise ValidationError(f'{metric.replace("_", " ").title()} must be between 0 and 1')
        
        return cleaned_data
    
    def save(self, commit=True):
        """Save the model with the current user as creator"""
        model = super().save(commit=False)
        if self.user:
            model.created_by = self.user
        
        if commit:
            model.save()
            # Add creator to team members
            if self.user:
                model.team_members.add(self.user)
        
        return model


class AIModelCategoryForm(forms.ModelForm):
    """Form for creating AI model categories"""
    
    class Meta:
        model = AIModelCategory
        fields = ['name', 'description', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe this category...'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'value': '#007bff'
            })
        }
