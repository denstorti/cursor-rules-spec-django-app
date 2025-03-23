from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Skill, Job, JobApplication

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "hirer", "status", "category", "created_at", "deadline", "is_public")
    list_filter = ("status", "category", "experience_level", "is_remote", "is_public")
    search_fields = ("title", "description", "hirer__username", "hirer__email")
    date_hierarchy = "created_at"
    filter_horizontal = ("skills",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {
            "fields": ("title", "description", "hirer", "status")
        }),
        (_("Categorization"), {
            "fields": ("category", "skills")
        }),
        (_("Budget & Timeline"), {
            "fields": ("budget_min", "budget_max", "fixed_budget", "duration", "deadline")
        }),
        (_("Location & Requirements"), {
            "fields": ("is_remote", "location", "experience_level")
        }),
        (_("Visibility & Timestamps"), {
            "fields": ("is_public", "created_at", "updated_at")
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Regular staff users can only see jobs they created if they are hirers
        return qs.filter(hirer=request.user)

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "freelancer", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("job__title", "freelancer__username", "freelancer__email", "cover_letter")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    fieldsets = (
        (None, {
            "fields": ("job", "freelancer", "status")
        }),
        (_("Application Details"), {
            "fields": ("cover_letter", "proposed_budget")
        }),
        (_("Timestamps"), {
            "fields": ("created_at", "updated_at")
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Regular staff users who are hirers can only see applications for their jobs
        if hasattr(request.user, 'is_hirer') and request.user.is_hirer:
            return qs.filter(job__hirer=request.user)
        # Regular staff users who are freelancers can only see their own applications
        if hasattr(request.user, 'is_freelancer') and request.user.is_freelancer:
            return qs.filter(freelancer=request.user)
        return qs.none()
