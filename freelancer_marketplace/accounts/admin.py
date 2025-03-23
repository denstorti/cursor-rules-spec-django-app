from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, FreelancerProfile, HirerProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    """
    Custom admin for the User model with additional fields.
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'profile_picture')}),
        (_('Role'), {'fields': ('role',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)


class FreelancerProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for FreelancerProfile model.
    """
    list_display = ('get_user_email', 'get_user_full_name', 'availability_status')
    list_filter = ('availability_status',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'skills')
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = _('Email')
    get_user_email.admin_order_field = 'user__email'
    
    def get_user_full_name(self, obj):
        return obj.user.get_full_name()
    get_user_full_name.short_description = _('Full Name')
    get_user_full_name.admin_order_field = 'user__first_name'


class HirerProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for HirerProfile model.
    """
    list_display = ('get_user_email', 'get_user_full_name', 'company_name', 'industry')
    list_filter = ('industry',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'company_name')
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = _('Email')
    get_user_email.admin_order_field = 'user__email'
    
    def get_user_full_name(self, obj):
        return obj.user.get_full_name()
    get_user_full_name.short_description = _('Full Name')
    get_user_full_name.admin_order_field = 'user__first_name'


# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(FreelancerProfile, FreelancerProfileAdmin)
admin.site.register(HirerProfile, HirerProfileAdmin) 