from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Job, Category, Skill, JobApplication
from .forms import JobForm, JobSearchForm, JobApplicationForm


class JobListView(ListView):
    """
    Display a list of published jobs with search and filter functionalities
    """
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10
    
    def get_queryset(self):
        # Start with published jobs
        queryset = Job.objects.filter(status=Job.Status.PUBLISHED)
        
        # Process search form
        form = JobSearchForm(self.request.GET)
        if form.is_valid():
            # Keyword search
            q = form.cleaned_data.get('q')
            if q:
                queryset = queryset.filter(
                    Q(title__icontains=q) | Q(description__icontains=q)
                )
            
            # Category filter
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)
            
            # Skills filter
            skills = form.cleaned_data.get('skills')
            if skills:
                # Return jobs that have ALL the selected skills
                for skill in skills:
                    queryset = queryset.filter(skills=skill)
            
            # Budget filter
            budget_min = form.cleaned_data.get('budget_min')
            if budget_min:
                queryset = queryset.filter(
                    Q(budget_min__gte=budget_min) | Q(fixed_budget__gte=budget_min)
                )
            budget_max = form.cleaned_data.get('budget_max')
            if budget_max:
                queryset = queryset.filter(
                    Q(budget_max__lte=budget_max) | Q(fixed_budget__lte=budget_max)
                )
            
            # Remote only filter
            is_remote = form.cleaned_data.get('is_remote')
            if is_remote:
                queryset = queryset.filter(is_remote=True)
            
            # Experience level filter
            exp_level = form.cleaned_data.get('experience_level')
            if exp_level:
                queryset = queryset.filter(experience_level=exp_level)
            
            # Sorting
            sort = form.cleaned_data.get('sort')
            if sort:
                queryset = queryset.order_by(sort)
            else:
                queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = JobSearchForm(self.request.GET or None)
        context['categories'] = Category.objects.all()
        context['popular_skills'] = Skill.objects.annotate(
            job_count=Count('jobs')
        ).order_by('-job_count')[:10]
        return context


class JobDetailView(DetailView):
    """
    Display details about a specific job
    """
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # If the user is not authenticated, only show public published jobs
        if not self.request.user.is_authenticated:
            return queryset.filter(status=Job.Status.PUBLISHED, is_public=True)
        
        # If the user is the hirer who created the job, show it regardless of status
        if hasattr(self.request.user, 'is_hirer') and self.request.user.is_hirer:
            return queryset.filter(
                Q(hirer=self.request.user) | 
                Q(status=Job.Status.PUBLISHED, is_public=True)
            )
        
        # For authenticated freelancers, show all public published jobs
        return queryset.filter(status=Job.Status.PUBLISHED, is_public=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if the user has already applied to this job
        if self.request.user.is_authenticated and hasattr(self.request.user, 'is_freelancer') and self.request.user.is_freelancer:
            user_has_applied = JobApplication.objects.filter(
                job=self.object,
                freelancer=self.request.user
            ).exists()
            context['user_has_applied'] = user_has_applied

            # Create application form
            if not user_has_applied:
                context['application_form'] = JobApplicationForm(job=self.object, user=self.request.user)
        
        # Get related jobs based on category and skills
        if self.object.category:
            related_jobs = Job.objects.filter(
                category=self.object.category,
                status=Job.Status.PUBLISHED,
                is_public=True
            ).exclude(pk=self.object.pk)
            
            if self.object.skills.exists():
                # Boost jobs that share skills
                related_jobs = related_jobs.filter(
                    skills__in=self.object.skills.all()
                ).distinct()
            
            context['related_jobs'] = related_jobs[:5]
        
        return context


class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Create a new job (hirers only)
    """
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    
    def test_func(self):
        return hasattr(self.request.user, 'is_hirer') and self.request.user.is_hirer
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create New Job')
        context['submit_text'] = _('Save as Draft')
        context['publish_text'] = _('Publish Job')
        return context
    
    def form_valid(self, form):
        # Save the job with draft status
        self.object = form.save()
        
        # Check if publish button was clicked
        if 'publish' in self.request.POST:
            self.object.status = Job.Status.PUBLISHED
            self.object.save()
            messages.success(self.request, _('Your job has been published successfully!'))
        else:
            messages.success(self.request, _('Your job has been saved as a draft.'))
        
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('jobs:job_detail', kwargs={'pk': self.object.pk})


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit an existing job (owner only)
    """
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    
    def test_func(self):
        job = self.get_object()
        return (
            hasattr(self.request.user, 'is_hirer') and 
            self.request.user.is_hirer and 
            job.hirer == self.request.user
        )
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit Job')
        context['submit_text'] = _('Save Changes')
        
        # Add publish button if the job is a draft
        if self.object.status == Job.Status.DRAFT:
            context['publish_text'] = _('Save and Publish')
        
        # For published jobs, add close button
        if self.object.status == Job.Status.PUBLISHED:
            context['close_text'] = _('Save and Close Job')
        
        # For closed jobs, add reopen button
        if self.object.status == Job.Status.CLOSED:
            context['reopen_text'] = _('Save and Reopen Job')
        
        return context
    
    def form_valid(self, form):
        # Save the job normally
        self.object = form.save()
        
        # Check if any special action buttons were clicked
        if 'publish' in self.request.POST and self.object.status == Job.Status.DRAFT:
            self.object.status = Job.Status.PUBLISHED
            self.object.save()
            messages.success(self.request, _('Your job has been published successfully!'))
        
        elif 'close' in self.request.POST and self.object.status == Job.Status.PUBLISHED:
            self.object.status = Job.Status.CLOSED
            self.object.save()
            messages.success(self.request, _('Your job has been closed for applications.'))
        
        elif 'reopen' in self.request.POST and self.object.status == Job.Status.CLOSED:
            self.object.status = Job.Status.PUBLISHED
            self.object.save()
            messages.success(self.request, _('Your job has been reopened for applications.'))
        
        else:
            messages.success(self.request, _('Your job has been updated successfully.'))
        
        return redirect(self.get_success_url())


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a job (owner only, and only if it's a draft)
    """
    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('jobs:my_jobs')
    
    def test_func(self):
        job = self.get_object()
        # Only allow deletion of draft jobs by the owner
        return (
            hasattr(self.request.user, 'is_hirer') and 
            self.request.user.is_hirer and 
            job.hirer == self.request.user and
            job.status == Job.Status.DRAFT
        )


class MyJobsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Show all jobs created by the current hirer
    """
    model = Job
    template_name = 'jobs/my_jobs.html'
    context_object_name = 'jobs'
    paginate_by = 10
    
    def test_func(self):
        return hasattr(self.request.user, 'is_hirer') and self.request.user.is_hirer
    
    def get_queryset(self):
        return Job.objects.filter(hirer=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Group jobs by status
        context['draft_jobs'] = self.get_queryset().filter(status=Job.Status.DRAFT)
        context['published_jobs'] = self.get_queryset().filter(status=Job.Status.PUBLISHED)
        context['closed_jobs'] = self.get_queryset().filter(
            Q(status=Job.Status.CLOSED) | 
            Q(status=Job.Status.FILLED) | 
            Q(status=Job.Status.EXPIRED)
        )
        
        # Add application counts
        for job_list in [context['draft_jobs'], context['published_jobs'], context['closed_jobs']]:
            for job in job_list:
                job.application_count = job.applications.count()
        
        return context


class JobApplicationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Submit an application for a job
    """
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'jobs/job_application_form.html'
    
    def test_func(self):
        # Check if user is a freelancer
        if not (hasattr(self.request.user, 'is_freelancer') and self.request.user.is_freelancer):
            return False
        
        # Get the job
        job_id = self.kwargs.get('job_id')
        self.job = get_object_or_404(Job, pk=job_id)
        
        # Check if the job is published
        if self.job.status != Job.Status.PUBLISHED:
            return False
        
        # Check if user already applied to this job
        user_applied = JobApplication.objects.filter(
            job=self.job,
            freelancer=self.request.user
        ).exists()
        
        return not user_applied
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['job'] = self.job
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.job
        return context
    
    def form_valid(self, form):
        # Set the job and freelancer
        form.instance.job = self.job
        form.instance.freelancer = self.request.user
        
        # Save the application
        response = super().form_valid(form)
        
        # Show success message
        messages.success(self.request, _('Your application has been submitted successfully!'))
        
        return response
    
    def get_success_url(self):
        return reverse('jobs:job_detail', kwargs={'pk': self.job.pk})


class MyApplicationsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Show all applications submitted by the current freelancer
    """
    model = JobApplication
    template_name = 'jobs/my_applications.html'
    context_object_name = 'applications'
    paginate_by = 10
    
    def test_func(self):
        return hasattr(self.request.user, 'is_freelancer') and self.request.user.is_freelancer
    
    def get_queryset(self):
        return JobApplication.objects.filter(
            freelancer=self.request.user
        ).select_related('job').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Group applications by status
        context['pending_applications'] = self.get_queryset().filter(status=JobApplication.Status.PENDING)
        context['active_applications'] = self.get_queryset().filter(
            Q(status=JobApplication.Status.SHORTLISTED) | 
            Q(status=JobApplication.Status.ACCEPTED)
        )
        context['rejected_applications'] = self.get_queryset().filter(
            Q(status=JobApplication.Status.REJECTED) | 
            Q(status=JobApplication.Status.WITHDRAWN)
        )
        
        return context


class JobApplicationsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Show all applications for a specific job (job owner only)
    """
    model = JobApplication
    template_name = 'jobs/job_applications.html'
    context_object_name = 'applications'
    paginate_by = 20
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.job = get_object_or_404(Job, pk=self.kwargs.get('job_id'))
    
    def test_func(self):
        # Only the job owner can view applications
        return (
            hasattr(self.request.user, 'is_hirer') and 
            self.request.user.is_hirer and 
            self.job.hirer == self.request.user
        )
    
    def get_queryset(self):
        return JobApplication.objects.filter(
            job=self.job
        ).select_related('freelancer').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.job
        
        # Group applications by status
        context['pending_applications'] = self.get_queryset().filter(status=JobApplication.Status.PENDING)
        context['shortlisted_applications'] = self.get_queryset().filter(status=JobApplication.Status.SHORTLISTED)
        context['accepted_applications'] = self.get_queryset().filter(status=JobApplication.Status.ACCEPTED)
        context['rejected_applications'] = self.get_queryset().filter(
            Q(status=JobApplication.Status.REJECTED) | 
            Q(status=JobApplication.Status.WITHDRAWN)
        )
        
        return context


class UpdateApplicationStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Update the status of a job application
    """
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.application = get_object_or_404(JobApplication, pk=self.kwargs.get('pk'))
    
    def test_func(self):
        # Only the job owner can update application statuses
        return (
            hasattr(self.request.user, 'is_hirer') and 
            self.request.user.is_hirer and 
            self.application.job.hirer == self.request.user
        )
    
    def post(self, request, *args, **kwargs):
        new_status = request.POST.get('status')
        
        # Validate the status
        valid_statuses = [choice[0] for choice in JobApplication.Status.choices]
        if new_status not in valid_statuses:
            messages.error(request, _('Invalid status.'))
            return redirect('jobs:job_applications', job_id=self.application.job.pk)
        
        # Update the status
        self.application.status = new_status
        self.application.save()
        
        # If accepting this application, update job status
        if new_status == JobApplication.Status.ACCEPTED:
            self.application.job.status = Job.Status.FILLED
            self.application.job.save()
            
            # Reject all other pending applications
            JobApplication.objects.filter(
                job=self.application.job,
                status=JobApplication.Status.PENDING
            ).exclude(pk=self.application.pk).update(status=JobApplication.Status.REJECTED)
        
        # Show success message
        messages.success(request, _('Application status updated successfully.'))
        
        return redirect('jobs:job_applications', job_id=self.application.job.pk)


class WithdrawApplicationView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Allow a freelancer to withdraw their application
    """
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.application = get_object_or_404(JobApplication, pk=self.kwargs.get('pk'))
    
    def test_func(self):
        # Only the freelancer who created the application can withdraw it
        return (
            hasattr(self.request.user, 'is_freelancer') and 
            self.request.user.is_freelancer and 
            self.application.freelancer == self.request.user and
            self.application.status in [
                JobApplication.Status.PENDING,
                JobApplication.Status.SHORTLISTED
            ]
        )
    
    def post(self, request, *args, **kwargs):
        # Update the status to withdrawn
        self.application.status = JobApplication.Status.WITHDRAWN
        self.application.save()
        
        # Show success message
        messages.success(request, _('Your application has been withdrawn.'))
        
        return redirect('jobs:my_applications')


class CategoryDetailView(ListView):
    """
    Show all jobs for a specific category
    """
    model = Job
    template_name = 'jobs/category_detail.html'
    context_object_name = 'jobs'
    paginate_by = 10
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
    
    def get_queryset(self):
        return Job.objects.filter(
            category=self.category,
            status=Job.Status.PUBLISHED,
            is_public=True
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        
        # Get popular skills for this category
        context['popular_skills'] = Skill.objects.filter(
            jobs__category=self.category
        ).annotate(
            job_count=Count('jobs')
        ).order_by('-job_count')[:10]
        
        return context
