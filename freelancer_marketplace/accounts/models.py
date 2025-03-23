from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser with additional fields and role choices.
    """
    class Role(models.TextChoices):
        FREELANCER = 'FREELANCER', _('Freelancer')
        HIRER = 'HIRER', _('Hirer')
    
    role = models.CharField(
        max_length=20, 
        choices=Role.choices,
        verbose_name=_('Role'),
        help_text=_('User role in the system (Freelancer or Hirer)')
    )
    email = models.EmailField(_('email address'), unique=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        null=True, 
        blank=True,
        verbose_name=_('Profile Picture')
    )
    
    # Make email required and unique
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    @property
    def is_freelancer(self):
        return self.role == self.Role.FREELANCER
    
    @property
    def is_hirer(self):
        return self.role == self.Role.HIRER


class FreelancerProfile(models.Model):
    """
    Profile model for freelancers with specific data fields.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='freelancer_profile',
        limit_choices_to={'role': User.Role.FREELANCER}
    )
    skills = models.TextField(
        _('Skills'),
        blank=True,
        help_text=_('Skills separated by commas')
    )
    experience = models.TextField(
        _('Experience'),
        blank=True,
        help_text=_('Professional experience details')
    )
    portfolio = models.URLField(
        _('Portfolio URL'),
        blank=True,
        help_text=_('URL to online portfolio')
    )
    rate_expectations = models.DecimalField(
        _('Hourly Rate'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    AVAILABILITY_CHOICES = [
        ('AVAILABLE', _('Available')),
        ('BUSY', _('Busy')),
        ('UNAVAILABLE', _('Unavailable')),
    ]
    availability_status = models.CharField(
        _('Availability Status'),
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='AVAILABLE'
    )
    
    def __str__(self):
        return f"{self.user.get_full_name()}'s Freelancer Profile"


class HirerProfile(models.Model):
    """
    Profile model for hirers with specific data fields.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='hirer_profile',
        limit_choices_to={'role': User.Role.HIRER}
    )
    company_name = models.CharField(
        _('Company Name'),
        max_length=255,
        blank=True
    )
    industry = models.CharField(
        _('Industry'),
        max_length=100,
        blank=True
    )
    COMPANY_SIZE_CHOICES = [
        ('1-10', _('1-10 employees')),
        ('11-50', _('11-50 employees')),
        ('51-200', _('51-200 employees')),
        ('201-500', _('201-500 employees')),
        ('501+', _('501+ employees')),
    ]
    company_size = models.CharField(
        _('Company Size'),
        max_length=20,
        choices=COMPANY_SIZE_CHOICES,
        blank=True
    )
    website = models.URLField(
        _('Website'),
        blank=True
    )
    
    def __str__(self):
        return f"{self.user.get_full_name()}'s Hirer Profile" 