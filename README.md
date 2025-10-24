# Team Blog App

A Django-based blog application with AI model management capabilities.

## Features

### Blog Features
- **Post Management**: Create, edit, and manage blog posts
- **Rich Text Editing**: MarkdownX integration for rich text editing
- **Tag System**: Organize posts with tags and colors
- **User Authentication**: User registration and login
- **Media Support**: Image uploads and embedding

### AI Models Features
- **Model Management**: Create and manage AI models
- **Categories**: Organize models by categories
- **Model Metadata**: Track performance metrics, versions, and configurations
- **API Endpoints**: REST API for model information
- **User Dashboard**: Manage your created models

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Team_blog_app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Usage

### Blog Management
- Navigate to `/` to view all posts
- Use the "Create" dropdown to create new posts or tags
- Manage your profile and posts from the user dropdown

### AI Model Management
- Navigate to `/ai-models/` to view available models
- Use "Create" → "New AI Model" to create models
- Use "Create" → "New Category" to create model categories
- Access "My AI Models" to manage your created models

### API Endpoints
- `GET /api/ai-models/models/` - List all public models
- `GET /api/ai-models/models/<slug>/` - Get model details

## Project Structure

```
Team_blog_app/
├── blog/                 # Blog app
├── ai_models/           # AI models app
├── account/             # User authentication
├── blog_app/            # Main project settings
├── templates/           # HTML templates
├── media/               # User uploads
├── static/              # Static files
└── requirements.txt     # Dependencies
```

## Dependencies

- Django 4.2.7
- django-markdownx (rich text editing)
- django-embed-video (video embedding)
- django-crispy-forms (form styling)
- crispy-bootstrap5 (Bootstrap 5 integration)
- djangorestframework (API support)
- django-cors-headers (CORS support)

## Development

### Creating Sample Data
```bash
# Create sample blog posts and tags
python manage.py create_sample_data

# Create sample tags
python manage.py create_sample_tags
```

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Notes

- Inference functionality is currently disabled
- AI model files should be stored in the `media/ai_models/` directory
- The application uses SQLite for development (change in production)
- Static files are served automatically in development mode
