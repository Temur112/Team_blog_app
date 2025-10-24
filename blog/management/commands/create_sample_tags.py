from django.core.management.base import BaseCommand
from blog.models import Tag


class Command(BaseCommand):
    help = 'Create sample blog tags'

    def handle(self, *args, **options):
        # Create sample tags
        tags_data = [
            {'name': 'Python', 'color': '#3776ab'},
            {'name': 'Django', 'color': '#092e20'},
            {'name': 'Machine Learning', 'color': '#ff6b35'},
            {'name': 'Web Development', 'color': '#4ecdc4'},
            {'name': 'Tutorial', 'color': '#45b7d1'},
            {'name': 'AI', 'color': '#96ceb4'},
            {'name': 'Data Science', 'color': '#feca57'},
            {'name': 'JavaScript', 'color': '#f7b731'},
            {'name': 'React', 'color': '#61dafb'},
            {'name': 'Programming', 'color': '#6c5ce7'},
        ]

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_data['name'],
                defaults=tag_data
            )
            if created:
                self.stdout.write(f'Created tag: {tag.name}')
            else:
                self.stdout.write(f'Tag already exists: {tag.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample blog tags!')
        )
