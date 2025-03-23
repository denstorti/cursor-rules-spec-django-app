# Freelancer Marketplace Platform

A comprehensive web application that connects freelancers with clients who need their services. This platform enables user registration, profile management, job posting, application processes, and more.

## Project Overview

This platform creates a marketplace where:
- Freelancers can find work opportunities
- Hirers can post jobs and find skilled professionals
- Both parties can communicate, establish contracts, and complete projects

## Core Features

- **User Management**
  - User registration with role selection (Freelancer or Hirer)
  - Profile creation and customization
  - Authentication and authorization

- **Job Management**
  - Job posting for hirers with detailed requirements
  - Job browsing and searching for freelancers
  - Categories and tags for job classification

- **Application Process**
  - Application submission by freelancers
  - Application review by hirers
  - Candidate selection

- **Messaging System (Not Implemented)**
  - Real-time communication between parties
  - Notification system for updates

- **Contract Management (Not Implemented)**
  - Contract creation and negotiation
  - Milestone tracking
  - Payment integration

- **Review & Rating System (Not Implemented)**
  - Performance feedback for both parties
  - Rating system to build reputation

## Technology Stack

- **Backend**: Django 4.2
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Authentication**: Django Authentication System
- **Containerization**: Docker and Docker Compose

## Project Structure

```
freelancer_marketplace/       # Main application folder
├── accounts/                 # User management app
├── jobs/                     # Job posting and application system
├── templates/                # HTML templates
├── static/                   # Static assets (CSS, JS, images)
├── media/                    # User-uploaded content
├── freelancer_marketplace/   # Project configuration
└── docker-compose.yml        # Docker setup
```

## Getting Started

### With Docker (Recommended)

1. Clone the repository
2. Run `docker-compose up --build`
3. Apply migrations: `docker-compose exec web python manage.py migrate`
4. Create superuser: `docker-compose exec web python manage.py createsuperuser`
5. Access at http://localhost:8000/

### Local Development

1. Create virtual environment: `python -m venv venv`
2. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r freelancer_marketplace/requirements.txt`
4. Configure PostgreSQL database
5. Run migrations: `cd freelancer_marketplace && python manage.py migrate`
6. Start server: `python manage.py runserver`
7. Access at http://127.0.0.1:8000/

## Documentation

Detailed documentation for each component can be found in the `specs/` directory:

- User Management
- Job Management
- Application Process
- Messaging System
- Contract Management
- Reviews & Ratings
- Technical Architecture

## Development Practices

- Features should have comprehensive unit tests
- Local development uses containerized dependencies with Docker
- Follow Django best practices

## License

This project is licensed under the MIT License. 