from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('agent', 'Agent'),
        ('owner', 'Owner'),
    ]
    name = models.CharField(max_length=20)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone = models.CharField(max_length=15, blank=True)
    
    # Add these to resolve auth.User conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="listings_user_groups",
        related_query_name="listings_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="listings_user_permissions",
        related_query_name="listings_user",
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=10, choices=[
        ('buyer', 'Buyer'),
        ('agent', 'Agent'),
        ('owner', 'Owner')
    ], default='buyer')

    def __str__(self):
        return self.name
    
class PropertyType(models.Model):
    """Model for different types of properties (House, Apartment, Land, etc.)"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")

    class Meta:
        verbose_name_plural = "Property Types"
        ordering = ['name']

    def __str__(self):
        return self.name

class Amenity(models.Model):
    """Model for property amenities/features"""
    name = models.CharField(max_length=100, default="Garden")
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")

    class Meta:
        verbose_name_plural = "Amenities"
        ordering = ['name']

    def __str__(self):
        return self.name


class Location(models.Model):
    """Model for property locations"""
    address = models.CharField(max_length=255)
    CITY_CHOICES = [
        ('Ahmedabad', 'Ahmedabad'),
        ('Bangalore', 'Bangalore'),
        ('Chennai', 'Chennai'),
        ('Delhi', 'Delhi'),
        ('Gurgaon', 'Gurgaon'),
        ('Hyderabad', 'Hyderabad'),
        ('Kolkata', 'Kolkata'),
        ('Mumbai', 'Mumbai'),
        ('Noida', 'Noida'),
        ('Pune', 'Pune'),
    ]
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100, choices=CITY_CHOICES)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="India")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        unique_together = ('address', 'city', 'state', 'zip_code')

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"



class Property(models.Model):
    """Main model for property listings"""
    PROPERTY_STATUS = [
        ('for_sale', 'For Sale'),
        ('for_rent', 'For Rent'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
        ('pending', 'Pending'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    description = models.TextField()
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        limit_choices_to={'role': 'owner'}, 
        on_delete=models.PROTECT, 
        related_name='owned_properties'  # Changed from 'properties'
    )
    status = models.CharField(max_length=20, choices=PROPERTY_STATUS, default='for_sale')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    square_feet = models.PositiveIntegerField()
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="In square feet")
    year_built = models.PositiveIntegerField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    amenities = models.ManyToManyField(Amenity, blank=True)
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'agent'}, 
        on_delete=models.PROTECT, 
        related_name='managed_properties'  # Changed from 'properties'
    )
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    main_image = models.ImageField(upload_to='property_images/', null=True, blank=True)
    PROPERTY_PURPOSE = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('lease', 'For Lease'),
        ('hostel', 'Hostel/PG')
    ]
    
    # Keep existing fields and add:
    purpose = models.CharField(max_length=10, choices=PROPERTY_PURPOSE, default='sale')
    furnishing = models.CharField(max_length=20, choices=[
        ('furnished', 'Furnished'),
        ('semi-furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished')
    ], default='unfurnished')
    floor = models.PositiveIntegerField(default=1)
    total_floors = models.PositiveIntegerField(default=1)
    facing = models.CharField(max_length=20, choices=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], default='north')
    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.location.city}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'slug': self.slug})

    def get_price_display(self):
        if self.status in ['for_rent', 'rented']:
            return f"${self.price}/mo"
        return f"${self.price:,}"

    def get_main_image(self):
        return self.images.filter(is_main=True).first()


class PropertyImage(models.Model):
    """Model for property images"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/images/')
    caption = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_main', 'created_at']

    def __str__(self):
        return f"Image for {self.property.title}"

    def save(self, *args, **kwargs):
        # Ensure only one main image per property
        if self.is_main:
            PropertyImage.objects.filter(property=self.property).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)


class Inquiry(models.Model):
    """Model for property inquiries from potential buyers/renters"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField(blank=True)
    message = models.TextField()
    is_contacted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry for {self.property.title} from {self.name}"


class FavoriteProperty(models.Model):
    """Model for users to save favorite properties"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')
        verbose_name_plural = "Favorite Properties"

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.property.title}"


class Review(models.Model):
    """Model for property reviews"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('property', 'user')

    def __str__(self):
        return f"{self.rating} star review by {self.user.username} for {self.property.title}"
