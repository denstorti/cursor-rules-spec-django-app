from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from .models import Job, JobApplication, Category, Skill

class JobForm(forms.ModelForm):
    """
    Form for creating and editing jobs
    """
    # Add a field for creating new skills on the fly
    new_skills = forms.CharField(
        required=False,
        label=_("Add New Skills"),
        help_text=_("Enter new skills separated by commas"),
        widget=forms.TextInput(attrs={"placeholder": "e.g. Django, React, AWS"})
    )
    
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'category', 'skills',
            'budget_min', 'budget_max', 'fixed_budget',
            'duration', 'deadline',
            'is_remote', 'location', 'experience_level',
            'is_public', 'status'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'class': 'markdown-editor'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'skills': forms.SelectMultiple(attrs={'class': 'select2 form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Make some fields not required
        self.fields['category'].required = True
        self.fields['skills'].required = False
        
        # Custom labels and help texts
        self.fields['budget_min'].help_text = _("For range-based budget")
        self.fields['budget_max'].help_text = _("For range-based budget")
        self.fields['fixed_budget'].help_text = _("For fixed-price jobs")
        
        # Conditionally show status field
        if not self.instance.pk:  # New job
            self.fields.pop('status')  # Remove status field for new jobs
    
    def clean(self):
        cleaned_data = super().clean()
        budget_min = cleaned_data.get('budget_min')
        budget_max = cleaned_data.get('budget_max')
        fixed_budget = cleaned_data.get('fixed_budget')
        
        # Budget validation - must have either fixed_budget or budget_range
        if fixed_budget and (budget_min or budget_max):
            raise forms.ValidationError(
                _("Please specify either a fixed budget or a budget range, not both")
            )
        
        if budget_min and budget_max and budget_min > budget_max:
            raise forms.ValidationError(
                _("Minimum budget cannot be greater than maximum budget")
            )
        
        if not fixed_budget and not budget_min and not budget_max:
            raise forms.ValidationError(
                _("Please specify either a fixed budget or a budget range")
            )
        
        # Location validation
        is_remote = cleaned_data.get('is_remote')
        location = cleaned_data.get('location')
        
        if not is_remote and not location:
            self.add_error('location', _("Location is required for on-site jobs"))
        
        return cleaned_data
    
    def save(self, commit=True):
        job = super().save(commit=False)
        
        # Set the hirer
        if not job.pk and self.user:
            job.hirer = self.user
        
        # Set initial status for new jobs
        if not job.pk:
            job.status = Job.Status.DRAFT
        
        if commit:
            job.save()
            self.save_m2m()
            
            # Process new skills
            new_skills_text = self.cleaned_data.get('new_skills')
            if new_skills_text:
                skill_names = [s.strip() for s in new_skills_text.split(',') if s.strip()]
                for skill_name in skill_names:
                    # Create slug from name
                    slug = skill_name.lower().replace(' ', '-')
                    skill, created = Skill.objects.get_or_create(
                        name=skill_name,
                        defaults={'slug': slug}
                    )
                    job.skills.add(skill)
        
        return job


class JobSearchForm(forms.Form):
    """
    Form for searching and filtering jobs
    """
    q = forms.CharField(
        required=False,
        label=_("Search"),
        widget=forms.TextInput(attrs={
            'placeholder': _('Search job title or description...'),
            'class': 'form-control'
        })
    )
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        label=_("Category"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    skills = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Skill.objects.all(),
        label=_("Skills"),
        widget=forms.SelectMultiple(attrs={'class': 'select2 form-control'})
    )
    budget_min = forms.DecimalField(
        required=False,
        label=_("Min Budget"),
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': _('Min'),
            'class': 'form-control'
        })
    )
    budget_max = forms.DecimalField(
        required=False,
        label=_("Max Budget"),
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': _('Max'),
            'class': 'form-control'
        })
    )
    is_remote = forms.BooleanField(
        required=False,
        label=_("Remote Only"),
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    experience_level = forms.ChoiceField(
        required=False,
        choices=[('', _('Any Experience'))] + list(Job.ExperienceLevel.choices),
        label=_("Experience Level"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sort = forms.ChoiceField(
        required=False,
        choices=[
            ('-created_at', _('Newest First')),
            ('created_at', _('Oldest First')),
            ('-budget_max', _('Highest Budget')),
            ('budget_min', _('Lowest Budget')),
            ('deadline', _('Deadline (Soonest)')),
        ],
        initial='-created_at',
        label=_("Sort By"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class JobApplicationForm(forms.ModelForm):
    """
    Form for submitting job applications
    """
    class Meta:
        model = JobApplication
        fields = ['cover_letter', 'proposed_budget']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'proposed_budget': forms.NumberInput(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        self.job = kwargs.pop('job', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.job:
            # Set proposed budget initial values based on job
            if self.job.fixed_budget:
                self.fields['proposed_budget'].initial = self.job.fixed_budget
            elif self.job.budget_min:
                self.fields['proposed_budget'].initial = self.job.budget_min
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate that job is open for applications
        if self.job and self.job.status != Job.Status.PUBLISHED:
            raise forms.ValidationError(_("This job is not open for applications"))
        
        # Validate budget is within range if specified
        proposed_budget = cleaned_data.get('proposed_budget')
        if proposed_budget:
            if self.job.budget_min and proposed_budget < self.job.budget_min:
                self.add_error(
                    'proposed_budget',
                    _("Your proposed budget is below the minimum budget of %(min)s") % 
                    {'min': self.job.budget_min}
                )
            if self.job.budget_max and proposed_budget > self.job.budget_max:
                self.add_error(
                    'proposed_budget',
                    _("Your proposed budget is above the maximum budget of %(max)s") % 
                    {'max': self.job.budget_max}
                )
        
        return cleaned_data
    
    def save(self, commit=True):
        application = super().save(commit=False)
        
        if self.job:
            application.job = self.job
        
        if self.user:
            application.freelancer = self.user
        
        if commit:
            application.save()
        
        return application
