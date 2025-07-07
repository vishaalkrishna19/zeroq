# Zeroqueue - Employee Onboarding/Offboarding System

## Overview
Django-based application for managing employee onboarding and offboarding processes with comprehensive user management, role-based permissions, and multi-tenant account support.

## Features
- **Multi-tenant Architecture**: Support for multiple company accounts
- **User Management**: Complete CRUD operations for users
- **Role-Based Permissions**: Granular permission system with admin/staff roles
- **Authentication**: Django Allauth integration with password reset
- **Onboarding/Offboarding**: Workflow management for employee lifecycle
- **Admin Interface**: Full Django admin integration with CRUD operations
- **REST API**: Complete API with Django REST Framework
- **Password Generation**: Automatic strong password generation for new users

## Quick Start

### 1. Setup Environment
```bash
cd /Users/happyfox/Documents/HappyFox/Zeroqueue
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (if not created automatically)
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

### 5. Access Admin Panel
Visit: http://127.0.0.1:8000/admin/
- Default admin credentials (if auto-created): admin/admin123
- **Change password immediately!**

## Database Schema

### Accounts
- **Account**: Company/organization accounts
  - account_id, account_name, timezone
  - Contact info, address, subscription settings
  - Max users limit and current user count

### Users  
- **User**: Extended Django user model
  - Basic auth fields (username, email, password)
  - Employee info (employee_id, job_title, department)
  - Employment status and dates
  - Manager relationship, address fields
  - Security settings (2FA, password policies)

### Roles & Permissions
- **Permission**: Granular permissions by category and level
- **Role**: User roles (admin, staff) with permission collections
- **RolePermission**: Many-to-many with grant/deny and constraints

### User-Account Mapping
- **UserAccount**: Links users to accounts with roles
  - Onboarding/offboarding status tracking
  - Primary account designation
  - Admin access permissions

## API Endpoints

### Authentication
- `/api/auth/login/` - User login
- `/api/auth/logout/` - User logout  
- `/api/auth/password/reset/` - Password reset
- `/api/auth/registration/` - User registration

### Users
- `/api/users/` - List/create users
- `/api/users/{id}/` - User detail/update/delete
- `/api/users/{id}/change_password/` - Change password
- `/api/users/{id}/reset_password/` - Admin password reset
- `/api/users/{id}/accounts/` - User's accounts

### Accounts
- `/api/accounts/` - List/create accounts
- `/api/accounts/{id}/` - Account detail/update/delete
- `/api/accounts/{id}/users/` - Account users
- `/api/accounts/{id}/admins/` - Account admins

### Roles & Permissions
- `/api/roles/permissions/` - List permissions
- `/api/roles/roles/` - List/create roles
- `/api/roles/roles/{id}/assign_permission/` - Assign permission to role

### User Accounts
- `/api/users/accounts/` - User-account relationships
- `/api/users/accounts/{id}/start_onboarding/` - Start onboarding
- `/api/users/accounts/{id}/complete_onboarding/` - Complete onboarding
- `/api/users/accounts/{id}/start_offboarding/` - Start offboarding

## Admin Features

### User Management
- Create users with auto-generated strong passwords
- Password printed to terminal for secure sharing
- Employee information management
- Role assignment per account

### Account Management  
- Company account creation and configuration
- Timezone and subscription management
- User limit enforcement

### Role & Permission Management
- Create custom roles and permissions
- Granular permission assignment
- System role protection

## Security Features

- **Strong Password Generation**: 12-character passwords with mixed case, numbers, symbols
- **Password Policies**: Force password change on first login
- **Role-Based Access**: Granular permissions by category and level
- **Multi-tenant Isolation**: Account-based data separation
- **Admin Protection**: System roles cannot be deleted
- **Audit Logging**: Creation timestamps and user tracking

## Default Setup

### Permissions Created
- User Management: view, create, edit, delete users
- Account Management: view, create, edit, delete accounts  
- Role Management: view, create, edit, delete roles
- Onboarding: view, create, edit, complete onboarding
- Offboarding: view, create, edit, complete offboarding
- System Admin: system settings, admin panel access
- Reporting: view, create, export reports

### Default Roles
- **Admin**: Full permissions across all categories
- **Staff**: Basic view permissions only

## Production Deployment

1. **Environment Variables**:
   ```bash
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com
   DATABASE_URL=postgresql://user:pass@host:port/db
   ```

2. **Database**: Switch to PostgreSQL for production
3. **Static Files**: Configure static file serving
4. **Security**: Enable HTTPS, update CORS settings
5. **Email**: Configure SMTP for password reset emails

## Development Notes

- User creation always generates strong passwords
- Passwords are printed to terminal (secure in dev environment)
- Default admin user created automatically with migrations
- All models use UUID primary keys for security
- Comprehensive admin interface with filtering and search
- API includes pagination and filtering capabilities

## Support

For issues or questions about the Zeroqueue system, check the admin logs and ensure all migrations are applied correctly.