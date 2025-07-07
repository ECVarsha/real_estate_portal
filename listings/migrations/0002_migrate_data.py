# listings/migrations/0002_migrate_data.py
from django.db import migrations

def migrate_users(apps, schema_editor):
    # Get models
    OldUser = apps.get_model('listings', 'User')
    NewUser = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('listings', 'UserProfile')
    Property = apps.get_model('listings', 'Property')
    FavoriteProperty = apps.get_model('listings', 'FavoriteProperty')
    Review = apps.get_model('listings', 'Review')
    
    # Migrate each user
    for old_user in OldUser.objects.all():
        try:
            # Create new auth.User
            new_user = NewUser.objects.create(
                username=old_user.username,
                password=old_user.password,
                email=old_user.email,
                is_superuser=old_user.is_superuser,
                is_staff=old_user.is_staff,
                is_active=old_user.is_active,
                date_joined=old_user.date_joined,
                first_name=old_user.first_name or '',
                last_name=old_user.last_name or '',
                last_login=old_user.last_login
            )
            
            # Create UserProfile
            UserProfile.objects.create(
                user=new_user,
                name=old_user.name,
                phone=old_user.phone,
                role=old_user.role
            )
            
            # Update all relationships
            Property.objects.filter(owner=old_user).update(owner=new_user)
            Property.objects.filter(agent=old_user).update(agent=new_user)
            FavoriteProperty.objects.filter(user=old_user).update(user=new_user)
            Review.objects.filter(user=old_user).update(user=new_user)
            
        except Exception as e:
            print(f"Failed to migrate user {old_user.username}: {str(e)}")

def reverse_migration(apps, schema_editor):
    """Optional reverse operation"""
    pass  # Not implemented as this is a one-way migration

class Migration(migrations.Migration):
    dependencies = [
        ('listings', '0001_initial'),  # Depends on our corrected initial migration
    ]

    operations = [
        migrations.RunPython(migrate_users, reverse_migration),
    ]