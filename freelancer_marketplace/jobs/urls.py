from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Job listings and search
    path('', views.JobListView.as_view(), name='job_list'),
    path('search/', views.JobListView.as_view(), name='job_search'),
    
    # Job details
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    
    # Job management (for hirers)
    path('create/', views.JobCreateView.as_view(), name='job_create'),
    path('<int:pk>/edit/', views.JobUpdateView.as_view(), name='job_update'),
    path('<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),
    path('my-jobs/', views.MyJobsView.as_view(), name='my_jobs'),
    path('<int:job_id>/applications/', views.JobApplicationsView.as_view(), name='job_applications'),
    
    # Job applications (for freelancers)
    path('<int:job_id>/apply/', views.JobApplicationCreateView.as_view(), name='job_apply'),
    path('my-applications/', views.MyApplicationsView.as_view(), name='my_applications'),
    
    # Application management
    path('application/<int:pk>/update-status/', views.UpdateApplicationStatusView.as_view(), name='update_application_status'),
    path('application/<int:pk>/withdraw/', views.WithdrawApplicationView.as_view(), name='withdraw_application'),
    
    # Categories
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
]
