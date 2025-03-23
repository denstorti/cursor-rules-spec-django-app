# Job Management

## Overview
This document outlines the job management system for the Freelancer-Hirer Marketplace application. The system handles job posting, browsing, searching, and categorization.

## Job Posting

### Job Creation
- **Access**: Only authenticated hirers can create job postings
- **Job Status Options**:
  - Draft
  - Published
  - Closed
  - Filled
  - Expired

### Job Details
- **Title**: Brief, descriptive job title
- **Description**: Detailed job description with requirements
- **Category**: Primary job category
- **Tags/Skills**: Relevant skills and keywords
- **Budget Range**: Min-Max or Fixed budget
- **Duration**: Estimated project duration
- **Deadline**: Application deadline
- **Location**: Remote or specific location
- **Required Experience Level**: Entry, Intermediate, Expert
- **Creation Date**: Auto-generated timestamp
- **Visibility**: Public or Private

## Job Browsing and Search

### Browse Features
- **Pagination**: Show limited jobs per page
- **Sorting Options**:
  - Newest first
  - Budget (high to low)
  - Budget (low to high)
  - Expiry date
  - Relevance to user skills (for freelancers)

### Search Features
- **Keyword Search**: Search in title and description
- **Filters**:
  - By category
  - By skills/tags
  - By budget range
  - By duration
  - By location (remote vs on-site)
  - By experience level

### Job Categories
- Web Development
- Mobile Development
- Design & Creative
- Writing & Translation
- Administrative & Support
- Finance & Accounting
- Marketing & Sales
- Legal
- Engineering & Architecture
- Other

## Job Visibility and Management

### For Hirers
- View all jobs created by them
- Edit job details (for draft or published jobs)
- Close job applications
- Reopen closed jobs
- Delete draft jobs
- View application statistics

### For Freelancers
- View all public jobs
- Save jobs to favorites
- View application history
- Receive relevant job recommendations

## Technical Implementation

### Models
- Job Model
- Category Model
- Tag/Skill Model
- JobApplication Model (relation)

### Views
- Job Create/Edit View
- Job Detail View
- Job Listing View
- Job Search View
- My Jobs View (for hirers)
- Applied Jobs View (for freelancers)

### Forms
- Job Creation Form
- Job Search Form
- Job Application Form

### Additional Features
- Markdown support for job description
- Image upload for job attachments
- Automatic expiration based on deadline
- Email notifications for new relevant jobs
- SEO-friendly job URLs 