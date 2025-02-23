from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings
from django.db.models.fields.files import ImageField
import os


class Command(BaseCommand):
    help = 'Clean up unused images in the media folder.'

    def handle(self, *args, **kwargs):
        # Get the media directory
        media_root = settings.MEDIA_ROOT
        deleted_count = 0

        # 1. Collect all valid image paths stored in the database
        db_image_paths = set()
        for model in apps.get_models():  # Iterate through all models
            for field in model._meta.get_fields():  # Check fields
                if isinstance(field, ImageField):  # Only ImageFields
                    # Fetch all image paths for this field
                    images = model.objects.values_list(field.name, flat=True)
                    db_image_paths.update([img for img in images if img])  # Add non-empty paths

        # 2. Collect all image files in the media directory
        for root, dirs, files in os.walk(media_root):  # Walk through the media folder
            for file in files:
                file_path = os.path.join(root, file)

                # Create relative path to match db path (e.g., "productImages/xyz.jpg")
                relative_path = os.path.relpath(file_path, media_root)

                # 3. Delete files not referenced in the database
                if relative_path not in db_image_paths:
                    os.remove(file_path)  # Delete unused file
                    self.stdout.write(f"Deleted: {relative_path}")
                    deleted_count += 1

        self.stdout.write(self.style.SUCCESS(f"Cleanup completed. {deleted_count} unused images deleted."))
