from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import (
    PropertyType,
    Amenity,
    Location,
    Property,
    PropertyImage,
    Inquiry,
    FavoriteProperty,
    Review
)

# Basic registration for simple models
admin.site.register(PropertyType)
admin.site.register(Amenity)
admin.site.register(Location)
admin.site.register(FavoriteProperty)
admin.site.register(User, UserAdmin)
# Custom admin classes for more complex models
class AgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'license_number', 'is_active')
    list_filter = ('is_active', 'hire_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'license_number')

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'status', 'price', 'location', 'is_featured')
    list_filter = ('status', 'property_type', 'is_featured', 'is_published')
    search_fields = ('title', 'description', 'location__city')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('amenities',)

class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image', 'is_main')
    list_editable = ('is_main',)
    list_filter = ('is_main',)

class InquiryAdmin(admin.ModelAdmin):
    list_display = ('property', 'name', 'email', 'is_contacted', 'created_at')
    list_filter = ('is_contacted', 'created_at')
    search_fields = ('name', 'email', 'property__title')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('property__title', 'user__username')

class OwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_verified', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone')
    list_filter = ('is_verified', 'created_at')

# Register models with custom admin classes
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImage, PropertyImageAdmin)
admin.site.register(Inquiry, InquiryAdmin)
admin.site.register(Review, ReviewAdmin)

