from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from accounts.models import User

class Category(models.Model):
    """
    Job categories for organizing job listings
    """
    name = models.CharField(_("Category Name"), max_length=100)
    description = models.TextField(_("Description"), blank=True)
    slug = models.SlugField(_("Slug"), unique=True)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("jobs:category_detail", kwargs={"slug": self.slug})


class Skill(models.Model):
    """
    Skills/tags for job listings
    """
    name = models.CharField(_("Skill Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)
    
    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        ordering = ["name"]
    
    def __str__(self):
        return self.name


class Job(models.Model):
    """
    Job posting model containing all job details
    """
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        PUBLISHED = 'PUBLISHED', _('Published')
        CLOSED = 'CLOSED', _('Closed')
        FILLED = 'FILLED', _('Filled')
        EXPIRED = 'EXPIRED', _('Expired')
    
    class ExperienceLevel(models.TextChoices):
        ENTRY = 'ENTRY', _('Entry')
        INTERMEDIATE = 'INTERMEDIATE', _('Intermediate')
        EXPERT = 'EXPERT', _('Expert')
    
    # Basic Job Info
    title = models.CharField(_("Job Title"), max_length=200)
    description = models.TextField(_("Job Description"))
    
    # Job Metadata
    hirer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="jobs", 
        limit_choices_to={"role": User.Role.HIRER},
        verbose_name=_("Hirer")
    )
    status = models.CharField(
        _("Status"), 
        max_length=20, 
        choices=Status.choices,
        default=Status.DRAFT
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="jobs",
        verbose_name=_("Category")
    )
    skills = models.ManyToManyField(
        Skill, 
        related_name="jobs",
        verbose_name=_("Required Skills")
    )
    
    # Budget and Timeline
    budget_min = models.DecimalField(
        _("Minimum Budget"), 
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    budget_max = models.DecimalField(
        _("Maximum Budget"), 
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    fixed_budget = models.DecimalField(
        _("Fixed Budget"), 
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text=_("If this is a fixed-price job, specify the budget here")
    )
    duration = models.CharField(
        _("Estimated Duration"), 
        max_length=100, 
        blank=True,
        help_text=_("e.g. '2 weeks', '3 months'")
    )
    deadline = models.DateTimeField(
        _("Application Deadline"), 
        blank=True, 
        null=True
    )
    
    # Location and Experience
    is_remote = models.BooleanField(
        _("Remote Work"), 
        default=True
    )
    location = models.CharField(
        _("Location"), 
        max_length=200, 
        blank=True,
        help_text=_("Required for on-site jobs")
    )
    experience_level = models.CharField(
        _("Required Experience Level"), 
        max_length=20, 
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.INTERMEDIATE
    )
    
    # Visibility and timestamps
    is_public = models.BooleanField(
        _("Public Listing"), 
        default=True,
        help_text=_("If unchecked, only invited freelancers can view this job")
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("jobs:job_detail", kwargs={"pk": self.pk})
    
    @property
    def is_expired(self):
        """Check if job has passed deadline"""
        if self.deadline:
            return timezone.now() > self.deadline
        return False
    
    def update_status(self):
        """Update job status based on deadline"""
        if self.status == self.Status.PUBLISHED and self.is_expired:
            self.status = self.Status.EXPIRED
            self.save(update_fields=["status"])


class JobApplication(models.Model):
    """
    Model for job applications submitted by freelancers
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        SHORTLISTED = 'SHORTLISTED', _('Shortlisted')
        REJECTED = 'REJECTED', _('Rejected')
        ACCEPTED = 'ACCEPTED', _('Accepted')
        WITHDRAWN = 'WITHDRAWN', _('Withdrawn')
    
    job = models.ForeignKey(
        Job, 
        on_delete=models.CASCADE, 
        related_name="applications",
        verbose_name=_("Job")
    )
    freelancer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="applications",
        limit_choices_to={"role": User.Role.FREELANCER},
        verbose_name=_("Freelancer")
    )
    cover_letter = models.TextField(_("Cover Letter"))
    proposed_budget = models.DecimalField(
        _("Proposed Budget"), 
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True
    )
    status = models.CharField(
        _("Status"), 
        max_length=20, 
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(_("Applied At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    class Meta:
        verbose_name = _("Job Application")
        verbose_name_plural = _("Job Applications")
        ordering = ["-created_at"]
        # Ensure a freelancer can only apply once to a job
        unique_together = ["job", "freelancer"]
    
    def __str__(self):
        return f"{self.freelancer} - {self.job}"
    
    def get_absolute_url(self):
        return reverse("jobs:application_detail", kwargs={"pk": self.pk})
