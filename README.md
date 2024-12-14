README: Connecting API1 and API2

This document explains how API1 and API2 interact with each other, focusing on authentication and data flow. It is intended for developers or administrators who need to understand and maintain the connection.

Overview

API1 and API2 are two independent Django-based services that share user authentication and some data interactions. They are designed to work together seamlessly by:

Sharing a MySQL database for authentication.

Using DRF Token Authentication for secured endpoints.

Architecture

API1 (Primary API)

Purpose: Handles user authentication (signup, login, token generation).

Technologies: Django, DRF (Django Rest Framework).

Key Features:

User creation and token generation.

Exposes an endpoint to validate tokens (/api/validate-token/).

Provides authentication tokens used by API2.

API2 (Secondary API)

Purpose: Provides additional functionality such as profile management and resource handling, requiring authentication via API1 tokens.

Technologies: Django, DRF.

Key Features:

Relies on tokens issued by API1 for user authentication.

Reads the shared database to verify user tokens.

Integration Setup

1. Shared Database Configuration

Both APIs are connected to the same MySQL database, enabling API2 to validate and authenticate users created in API1.

Database Configuration (in settings.py):

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shared_database_name',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

Ensure the database is accessible to both API1 and API2.

2. Token Authentication

API1 generates authentication tokens upon user login.

API2 verifies these tokens to authenticate users.

Token Generation (API1):

When a user logs in via API1, a token is created using Django REST Framework's TokenAuthentication:

from rest_framework.authtoken.models import Token
user = User.objects.get(email="user@example.com")
token, _ = Token.objects.get_or_create(user=user)

Token Verification (API2):

API2 uses TokenAuthentication to validate tokens stored in the shared database:

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

Add @authentication_classes([TokenAuthentication]) and @permission_classes([IsAuthenticated]) to the views that require authentication.

Authentication Workflow

User Signup (API1):

Users register using the /api/signup/ endpoint on API1.

API1 stores user credentials in the shared database.

User Login & Token Issuance (API1):

Users log in using /api/login/.

API1 generates a token and sends it in the response.

Example Response:

{
    "success": true,
    "message": "Login successful",
    "token": "abcdef1234567890"
}

Token-Based Authentication (API2):

Users send the token received from API1 in the Authorization header when making requests to API2.

API2 verifies the token by querying the shared database.

Example Request:

GET /api/edit-profile/ HTTP/1.1
Host: api2.example.com
Authorization: Token abcdef1234567890

Logout (API1):

When users log out via /api/logout/ on API1, the token is deleted from the database, invalidating access to both API1 and API2.

Endpoints Overview

API1

/api/signup/: User registration.

/api/login/: User login and token generation.

/api/logout/: User logout (deletes token).

/api/validate-token/: Validates a token for authentication.

API2

/api/edit-profile/: Allows users to view or update their profile (requires a valid token).

/api/resource/: Example endpoint that requires authentication.

Common Issues & Solutions

"Authentication credentials were not provided."

Ensure the token is included in the Authorization header for all requests to API2.

Check that both APIs are connected to the same database.

"Invalid token."

Verify that the token exists in the authtoken_token table of the shared database.

Ensure the token hasn't been deleted during logout.

Database Connection Errors:

Double-check database credentials in settings.py for both APIs.

Test database connectivity manually.

Security Notes

Use HTTPS: Ensure all API communications occur over HTTPS to protect token transmissions.

Token Expiry: Consider using rest_framework_simplejwt for time-limited tokens instead of permanent tokens.

Environment Variables: Store sensitive data like database credentials and secret keys in environment variables.

Future Improvements

Token Revocation: Implement token blacklisting for enhanced security.

Service Communication: Consider using a message broker like RabbitMQ or REST API calls between services instead of a shared database.

By following this guide, API1 and API2 should integrate smoothly, sharing authentication and user data effectively.

