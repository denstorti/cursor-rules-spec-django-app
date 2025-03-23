from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User, FreelancerProfile, HirerProfile

class CustomUserCreationForm(UserCreationForm):
    """
    Form for user registration with email as the unique identifier.
    """
    role = forms.ChoiceField(
        choices=User.Role.choices,
        widget=forms.RadioSelect,
        label=_("I am registering as a")
    )
    
    email = forms.EmailField(
        label=_("Email address"),
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text=_("We'll never share your email with anyone else.")
    )
    
    terms_agreement = forms.BooleanField(
        required=True,
        label=_("I agree to the terms and conditions"),
        error_messages={
            'required': _("You must agree to the terms and conditions to register")
        }
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'role', 'terms_agreement')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the default password widget classes
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        """
        Validate that the email is unique.
        """
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(_("This email address is already in use."))
        return email


class CustomUserChangeForm(UserChangeForm):
    """
    Form for users to update their account information (excluding password).
    """
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'profile_picture')


class FreelancerProfileForm(forms.ModelForm):
    """
    Form for freelancers to update their profile.
    """
    skills = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text=_("Enter your skills separated by commas (e.g., Python, JavaScript, UI/UX Design)")
    )
    
    experience = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        required=False
    )
    
    class Meta:
        model = FreelancerProfile
        fields = ('skills', 'experience', 'portfolio', 'rate_expectations', 'availability_status')
        widgets = {
            'rate_expectations': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }


class HirerProfileForm(forms.ModelForm):
    """
    Form for hirers to update their profile.
    """
    class Meta:
        model = HirerProfile
        fields = ('company_name', 'industry', 'company_size', 'website')
        widgets = {
            'website': forms.URLInput(attrs={'placeholder': 'https://'}),
        } 