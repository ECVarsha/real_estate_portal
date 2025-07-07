from django.core.management.base import BaseCommand
from django.core import serializers
from listings.models import *  # Changed from myapp to your actual app name
import os
from datetime import datetime
import json

class Command(BaseCommand):
    help = 'Exports all database data to JSON files with proper formatting'
    
    def handle(self, *args, **options):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_dir = f"data_backups/{timestamp}"
        os.makedirs(export_dir, exist_ok=True)
        
        # Updated to include ALL your models
        models = [
            User, Property, PropertyType, Location, 
            Amenity, Inquiry, FavoriteProperty, 
            Review, PropertyImage
        ]
        
        for model in models:
            try:
                queryset = model.objects.all()
                filename = f"{export_dir}/{model.__name__.lower()}.json"
                
                # Improved serialization with pretty formatting
                data = serializers.serialize(
                    "json", 
                    queryset, 
                    indent=2,
                    use_natural_foreign_keys=True,
                    use_natural_primary_keys=True
                )
                
                # Write to file with better formatting
                with open(filename, 'w') as f:
                    json.dump(json.loads(data), f, indent=2)
                
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Exported {queryset.count()} {model.__name__} records")
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ Failed to export {model.__name__}: {str(e)}")
                )