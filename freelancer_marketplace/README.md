# Freelancer Marketplace

A web application for connecting freelancers with clients who need their services. This platform facilitates user registration, profile management, job posting, and application processes.

## Features

- **User Management**
  - User registration with role selection (Freelancer or Hirer)
  - Profile creation and management
  - Authentication and authorization

- **Job Management** (Coming Soon)
  - Job posting for hirers
  - Job search and filtering for freelancers
  - Application submission

- **Messaging System** (Coming Soon)
  - Real-time chat between freelancers and hirers
  - Notifications for new messages

- **Contract Management** (Coming Soon)
  - Contract creation and management
  - Payment integration

## Technology Stack

- **Backend**: Django 4.2
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Authentication**: Django Authentication System

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd freelancer_marketplace
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL database:
   - Create a database named 'freelancer_marketplace'
   - Update database settings in settings.py if needed

5. Apply migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

## How to Run

### Option 1: Using Docker (Recommended)

This project includes Docker configuration for easy setup and deployment.

1. Make sure you have Docker and Docker Compose installed on your system.

2. Build and run the containers:
   ```
   docker-compose up --build
   ```

3. **Important**: When running for the first time, you need to apply migrations:
   ```
   # Create migrations if they don't exist
   docker-compose exec web python manage.py makemigrations accounts
   
   # Apply all migrations
   docker-compose exec web python manage.py migrate
   ```

4. Create a superuser for admin access:
   ```
   docker-compose exec web python manage.py createsuperuser
   ```

5. The application will be available at http://localhost:8000/

6. To stop the containers:
   ```
   docker-compose down
   ```

### Option 2: Local Development

If you've already followed the installation steps above:

1. Ensure your PostgreSQL database is running and properly configured in settings.py

2. Apply migrations if you haven't already:
   ```
   python manage.py migrate
   ```

3. Start the development server:
   ```
   python manage.py runserver
   ```

4. Access the application at http://127.0.0.1:8000/

## Troubleshooting

### Database Connection Issues

If you encounter a "Connection refused" error when connecting to the PostgreSQL database:

1. **When using Docker**:
   - Make sure the database container is running: `docker-compose ps`
   - Ensure your settings.py is configured to use 'db' as the database host (this is the service name in docker-compose.yml)
   - Try restarting the containers: `docker-compose down && docker-compose up`

2. **For local development**:
   - Verify PostgreSQL is running on your machine
   - Check that the database credentials in settings.py match your local PostgreSQL settings
   - For local development, set the environment variable: `export DB_HOST=localhost`

### Migrations Issues

If you encounter migration problems:
  ```
  docker-compose exec web python manage.py migrate --fake-initial
  ```

If you see errors like "relation does not exist":
  ```
  # Create migrations first
  docker-compose exec web python manage.py makemigrations accounts
  
  # Then apply them
  docker-compose exec web python manage.py migrate
  ```

### Static Files Not Loading

If static files are not being served correctly:
  ```
  docker-compose exec web python manage.py collectstatic --noinput
  ```

## Project Structure

```
freelancer_marketplace/
│
├── accounts/                  # User management app
│   ├── migrations/            # Database migrations
│   ├── templates/accounts/    # Account-related templates
│   ├── admin.py               # Admin configuration
│   ├── forms.py               # User and profile forms
│   ├── models.py              # User and profile models
│   ├── urls.py                # Account URL routing
│   └── views.py               # Account views
│
├── static/                    # Static files
│   ├── css/                   # CSS files
│   ├── js/                    # JavaScript files
│   └── img/                   # Images
│
├── templates/                 # Base templates
│   ├── base.html              # Base template
│   └── home.html              # Homepage template
│
├── media/                     # User-uploaded files
│
└── freelancer_marketplace/    # Project configuration
    ├── settings.py            # Project settings
    ├── urls.py                # Main URL routing
    ├── wsgi.py                # WSGI configuration
    └── asgi.py                # ASGI configuration
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. 