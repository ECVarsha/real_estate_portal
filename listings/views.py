from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Property, PropertyType, Location, Amenity, Inquiry, FavoriteProperty, Review
from .forms import PropertyForm, LocationForm, UserRegistrationForm
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Property


def home(request):
    # Get featured properties
    featured_properties = Property.objects.filter(
        is_featured=True, 
        is_published=True
    ).order_by('-created_at')[:6]
    
    # Get property types for navigation/categories
    property_types = PropertyType.objects.all()

    city_choices = Location.CITY_CHOICES
    
    context = {
        'featured_properties': featured_properties,
        'property_types': property_types,
        'city_choices': city_choices,
    }
    return render(request, 'home.html', context)

def property_search(request):
    # Get query parameters
    query = request.GET.get('q', '')
    city = request.GET.get('city', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    property_type = request.GET.get('property_type', '')
    bedrooms = request.GET.get('bedrooms', '')
    budget = request.GET.get('budget', '')
    
    # Start with all published properties
    properties = Property.objects.filter(is_published=True)
    
    # Apply filters
    if query:
        properties = properties.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__city__icontains=query)
        )
    
    if city:
        properties = properties.filter(location__city=city)
    
    if min_price:
        properties = properties.filter(price__gte=min_price)
    
    if max_price:
        properties = properties.filter(price__lte=max_price)
    if budget:
        budget = int(budget)
        if budget == 2000000:
            properties = properties.filter(price__lte=2000000)
        elif budget == 5000000:
            properties = properties.filter(price__gt=2000000, price__lte=5000000)
        elif budget == 10000000:
            properties = properties.filter(price__gt=5000000, price__lte=10000000)
        elif budget == 10000001:
            properties = properties.filter(price__gt=10000000)

    if property_type:
        properties = properties.filter(property_type__name=property_type)
    
    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)

    # Handle AJAX requests differently
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        properties_data = []
        for prop in properties:
            prop_data = {
                'id': prop.id,
                'title': prop.title,
                'slug': prop.slug,
                'description': prop.description,
                'property_type': prop.property_type.name,
                'status': prop.status,
                'price': float(prop.price),  # Convert Decimal to float
                'price_display': prop.get_price_display(),
                'bedrooms': prop.bedrooms,
                'bathrooms': float(prop.bathrooms),  # Convert Decimal to float
                'square_feet': prop.square_feet,
                'lot_size': float(prop.lot_size) if prop.lot_size else None,
                'year_built': prop.year_built,
                'location': {
                    'address': prop.location.address,
                    'city': prop.location.city,
                    'state': prop.location.state,
                    'zip_code': prop.location.zip_code,
                    'latitude': float(prop.location.latitude) if prop.location.latitude else None,
                    'longitude': float(prop.location.longitude) if prop.location.longitude else None
                },
                'main_image': prop.main_image.url if prop.main_image else None,
                'is_featured': prop.is_featured,
                'detail_url': prop.get_absolute_url(),
                'created_at': prop.created_at.isoformat(),
                'updated_at': prop.updated_at.isoformat()
            }
            properties_data.append(prop_data)
        return JsonResponse({'properties': properties_data})

    # Regular HTML response
    context = {
        'search_query': query,
        'properties': properties,
        'selected_city': city,
        'selected_type': property_type,
        'selected_budget': budget,
    }
    return render(request, 'propertysearch.html', context)


def property_detail(request, slug):
    property = get_object_or_404(Property, slug=slug, is_published=True)
    
    # Handle inquiry form submission
    if request.method == 'POST' and 'inquiry' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        Inquiry.objects.create(
            property=property,
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        messages.success(request, 'Your inquiry has been submitted successfully!')
        return redirect('property_detail', slug=slug)
    
    # Handle review submission
    if request.method == 'POST' and 'review' in request.POST and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        Review.objects.create(
            property=property,
            user=request.user,
            rating=rating,
            comment=comment
        )
        messages.success(request, 'Thank you for your review!')
        return redirect('property_detail', slug=slug)
    
    # Check if property is favorited by the user
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = FavoriteProperty.objects.filter(
            user=request.user,
            property=property
        ).exists()
    
    context = {
        'property': property,
        'is_favorited': is_favorited,
        'reviews': property.reviews.all().order_by('-created_at'),
    }
    return render(request, 'p1.html', context)


@login_required
def toggle_favorite(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    favorite, created = FavoriteProperty.objects.get_or_create(
        user=request.user,
        property=property
    )
    
    if not created:
        favorite.delete()
        messages.success(request, 'Removed from favorites')
    else:
        messages.success(request, 'Added to favorites')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def post_property(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'owner':
        messages.warning(request, 'You need to be a registered owner to post properties')
        return redirect('signup')
    
    if request.method == 'POST':
        property_form = PropertyForm(request.POST, request.FILES, user=request.user)
        location_form = LocationForm(request.POST)
        
        if property_form.is_valid() and location_form.is_valid():
            location = location_form.save()
            property = property_form.save(commit=False)
            property.location = location
            property.owner = request.user.owner_profile
            property.save()
            property_form.save_m2m()
            
            messages.success(request, 'Property posted successfully!')
            return redirect('property_detail', slug=property.slug)
    else:
        property_form = PropertyForm(user=request.user)
        location_form = LocationForm()
    
    context = {
        'property_form': property_form,
        'location_form': location_form,
    }
    return render(request, 'postproperty.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        
        form = UserRegistrationForm(request.POST)
            
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            messages.success(request, 'Account created successfully!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Please correct the errors highlighted below.")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'signup.html', {'form': form})

def terms(request):
    return render(request, 'terms.html')

def post_message(request):
    return render(request, 'post_message.html')