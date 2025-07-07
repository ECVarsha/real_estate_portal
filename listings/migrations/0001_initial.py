# listings/migrations/0001_initial.py
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
import phonenumber_field.modelfields

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Garden', max_length=100)),
                ('icon', models.CharField(blank=True, help_text='Font Awesome icon class', max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Amenities',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PropertyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
                ('icon', models.CharField(blank=True, help_text='Font Awesome icon class', max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Property Types',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(choices=[('Ahmedabad', 'Ahmedabad'), ('Bangalore', 'Bangalore'), ('Chennai', 'Chennai'), ('Delhi', 'Delhi'), ('Gurgaon', 'Gurgaon'), ('Hyderabad', 'Hyderabad'), ('Kolkata', 'Kolkata'), ('Mumbai', 'Mumbai'), ('Noida', 'Noida'), ('Pune', 'Pune')], max_length=100)),
                ('zip_code', models.CharField(max_length=20)),
                ('country', models.CharField(default='India', max_length=100)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
            ],
            options={
                'unique_together': {('address', 'city', 'state', 'zip_code')},
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('role', models.CharField(choices=[('buyer', 'Buyer'), ('agent', 'Agent'), ('owner', 'Owner')], default='buyer', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('for_sale', 'For Sale'), ('for_rent', 'For Rent'), ('sold', 'Sold'), ('rented', 'Rented'), ('pending', 'Pending')], default='for_sale', max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('bedrooms', models.PositiveIntegerField()),
                ('bathrooms', models.DecimalField(decimal_places=1, max_digits=3)),
                ('square_feet', models.PositiveIntegerField()),
                ('lot_size', models.DecimalField(blank=True, decimal_places=2, help_text='In square feet', max_digits=10, null=True)),
                ('year_built', models.PositiveIntegerField(blank=True, null=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='property_images/')),
                ('purpose', models.CharField(choices=[('sale', 'For Sale'), ('rent', 'For Rent'), ('lease', 'For Lease'), ('hostel', 'Hostel/PG')], default='sale', max_length=10)),
                ('furnishing', models.CharField(choices=[('furnished', 'Furnished'), ('semi-furnished', 'Semi-Furnished'), ('unfurnished', 'Unfurnished')], default='unfurnished', max_length=20)),
                ('floor', models.PositiveIntegerField(default=1)),
                ('total_floors', models.PositiveIntegerField(default=1)),
                ('facing', models.CharField(choices=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], default='north', max_length=20)),
                ('agent', models.ForeignKey(limit_choices_to={'profile__role': 'agent'}, on_delete=django.db.models.deletion.PROTECT, related_name='managed_properties', to='auth.user')),
                ('amenities', models.ManyToManyField(blank=True, to='listings.amenity')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='listings.location')),
                ('owner', models.ForeignKey(limit_choices_to={'profile__role': 'owner'}, on_delete=django.db.models.deletion.PROTECT, related_name='owned_properties', to='auth.user')),
                ('property_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='listings.propertytype')),
            ],
            options={
                'verbose_name_plural': 'Properties',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='properties/images/')),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('is_main', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='listings.property')),
            ],
            options={
                'ordering': ['-is_main', 'created_at'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='listings.property')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('property', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('message', models.TextField()),
                ('is_contacted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inquiries', to='listings.property')),
            ],
            options={
                'verbose_name_plural': 'Inquiries',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FavoriteProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.property')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'verbose_name_plural': 'Favorite Properties',
                'unique_together': {('user', 'property')},
            },
        ),
    ]