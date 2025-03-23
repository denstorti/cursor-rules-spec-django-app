# User Management

## Overview
This document outlines the user management system for the Freelancer-Hirer Marketplace application. The system handles user registration, authentication, profile management, and role-based permissions.

## User Types

### Freelancer
Individuals looking for job opportunities and offering their services.

### Hirer
Individuals or companies looking to hire talent for specific projects.

## User Registration

### Requirements
- Users must provide a valid email address
- Users must create a secure password (min 8 characters with combination of letters, numbers, and special characters)
- Users must select their role (Freelancer or Hirer)
- Users must agree to terms and conditions

### User Data
- **Common Data**
  - Email (unique)
  - Password (hashed)
  - Name
  - Role (Freelancer/Hirer)
  - Registration date
  - Last login
  - Profile picture (optional)
  - Contact information

- **Freelancer Specific Data**
  - Skills
  - Experience
  - Portfolio
  - Rate expectations
  - Availability status

- **Hirer Specific Data**
  - Company name (if applicable)
  - Industry
  - Company size (if applicable)
  - Website (optional)

## Authentication

- Email and password based login
- Password reset functionality
- Remember me option
- Session management
- JWT-based authentication for API access

## Profile Management

### Features
- Edit profile information
- Upload/change profile picture
- Manage privacy settings
- Update password
- Deactivate account

## Role-Based Permissions

### Freelancer Permissions
- Browse and search jobs
- Apply to jobs
- Communicate with potential hirers
- Manage received offers
- Track application status

### Hirer Permissions
- Post new jobs
- Edit/delete posted jobs
- Review applications
- Communicate with applicants
- Approve applications
- Manage active contracts

## Technical Implementation

- Utilize Django's built-in User model with extensions
- Create custom user model by extending AbstractUser
- Implement Django auth views for registration and login
- Use Django forms for validation
- Store profile images in media directory with appropriate size limits
- Implement proper password hashing using Django's authentication system 