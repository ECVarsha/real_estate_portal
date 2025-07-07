from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Property, Location, UserProfile
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm


from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    name = forms.CharField(required=True, max_length=20)
    role = forms.ChoiceField(choices= UserProfile.role, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'name', 'phone', 'role']

    def save(self, commit=True):
        user = super().save(commit=commit)
        UserProfile.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            phone=self.cleaned_data['phone'],
            role=self.cleaned_data['role']
        )
        return user
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 'purpose', 'status', 'price',
            'bedrooms', 'bathrooms', 'square_feet', 'lot_size', 'year_built',
            'amenities', 'is_featured', 'main_image', 'furnishing', 'floor',
            'total_floors', 'facing'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'purpose': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Basic Details',
                'title',
                'description',
                'property_type',
                'purpose',
                'status',
                'price',
                'main_image'
            ),
            Fieldset(
                'Property Specifications',
                'bedrooms',
                'bathrooms',
                'square_feet',
                'lot_size',
                'year_built',
                'furnishing',
                'floor',
                'total_floors',
                'facing'
            ),
            Fieldset(
                'Additional Details',
                'amenities',
                'is_featured'
            ),
            ButtonHolder(
                Submit('submit', 'Save Property', css_class='btn-primary')
            )
        )
class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['address', 'city', 'state', 'zip_code', 'country', 'latitude', 'longitude']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
