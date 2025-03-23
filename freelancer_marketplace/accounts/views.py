from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.db import transaction

from .models import User, FreelancerProfile, HirerProfile
from .forms import (
    CustomUserCreationForm, CustomUserChangeForm,
    FreelancerProfileForm, HirerProfileForm
)


class RegisterView(CreateView):
    """
    View for user registration that creates appropriate profile based on user role.
    """
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('profile_setup')
    
    def form_valid(self, form):
        """
        Save the user and create the appropriate profile based on role.
        """
        with transaction.atomic():
            # Save the user
            user = form.save()
            
            # Create the profile based on role
            if user.is_freelancer:
                # Check if profile already exists
                if not hasattr(user, 'freelancer_profile'):
                    FreelancerProfile.objects.create(user=user)
            elif user.is_hirer:
                # Check if profile already exists
                if not hasattr(user, 'hirer_profile'):
                    HirerProfile.objects.create(user=user)
            
            # Log the user in
            login(self.request, user)
            
            messages.success(self.request, _("Registration successful! Please complete your profile."))
            
            return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProfileSetupView(UpdateView):
    """
    View for setting up the user profile after registration.
    """
    template_name = 'accounts/profile_setup.html'
    success_url = reverse_lazy('home')
    
    def get_object(self):
        """
        Return the current user for the form.
        """
        return self.request.user
    
    def get_form_class(self):
        """
        Return the appropriate form based on user role.
        """
        user = self.request.user
        if user.is_freelancer:
            return FreelancerProfileForm
        elif user.is_hirer:
            return HirerProfileForm
        return CustomUserChangeForm
    
    def get_form_kwargs(self):
        """
        Pass the instance to the form based on user role.
        """
        kwargs = super().get_form_kwargs()
        user = self.request.user
        
        if user.is_freelancer:
            kwargs['instance'] = user.freelancer_profile
        elif user.is_hirer:
            kwargs['instance'] = user.hirer_profile
        
        return kwargs
    
    def form_valid(self, form):
        """
        Save the profile and show a success message.
        """
        form.save()
        messages.success(self.request, _("Your profile has been updated successfully!"))
        return super().form_valid(form)


@login_required
def profile_view(request):
    """
    View for displaying the user's profile.
    """
    user = request.user
    context = {'user': user}
    
    if user.is_freelancer:
        context['profile'] = user.freelancer_profile
    elif user.is_hirer:
        context['profile'] = user.hirer_profile
    
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    """
    View for editing the user's profile.
    """
    user = request.user
    user_form = CustomUserChangeForm(instance=user)
    profile_form = None
    
    if user.is_freelancer:
        profile_form = FreelancerProfileForm(instance=user.freelancer_profile)
    elif user.is_hirer:
        profile_form = HirerProfileForm(instance=user.hirer_profile)
    
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        
        if user.is_freelancer:
            profile_form = FreelancerProfileForm(request.POST, instance=user.freelancer_profile)
        elif user.is_hirer:
            profile_form = HirerProfileForm(request.POST, instance=user.hirer_profile)
        
        if user_form.is_valid() and profile_form and profile_form.is_valid():
            with transaction.atomic():
                user_form.save()
                profile_form.save()
            
            messages.success(request, _("Your profile has been updated successfully!"))
            return redirect('profile')
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    
    return render(request, 'accounts/edit_profile.html', context) 