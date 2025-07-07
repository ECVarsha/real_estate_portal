"""
URL configuration for Realestate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # Add this import
from django.urls import path, include  # Added include
from listings import views
from django.conf import settings
from django.conf.urls.static import static
from listings import views



urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', views.home, name='home'),
    path('post_message',views.post_message, name='post_message'),
    path('search/', views.property_search, name='property_search'),
    path('property/<slug:slug>/', views.property_detail, name='property_detail'),
    path('property/<int:property_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('post-property/', views.post_property, name='post_property'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('terms/', views.terms, name='terms'),

    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)