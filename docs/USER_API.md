# User Management API Documentation

## Overview
The User Management API provides endpoints for managing user accounts, profiles, preferences, and administrative functions.

## Base URL
```
/api/users
```

## Authentication
All endpoints require JWT authentication token in the `Authorization` header:
```
Authorization: Bearer <token>
```

## Endpoints

### 1. Get Current User
**Endpoint:** `GET /me`

**Description:** Get the current authenticated user's information

**Response (200 OK):**
```json
{
  "id": "user-123",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "avatar_url": "https://example.com/avatar.jpg",
  "bio": "Software developer",
  "is_active": true,
  "email_verified": true,
  "two_factor_enabled": false,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-15T10:30:00Z",
  "subscription_tier": "pro",
  "subscription_status": "active",
  "projects_count": 5,
  "storage_used": 2.5,
  "storage_limit": 10.0
}
```

### 2. Get User by ID
**Endpoint:** `GET /{user_id}`

**Description:** Get a specific user's public information

**Parameters:**
- `user_id` (path, required): User ID

**Response (200 OK):** Same as Get Current User

**Response (404 Not Found):**
```json
{
  "detail": "User not found"
}
```

### 3. List All Users
**Endpoint:** `GET /`

**Description:** List all users with pagination (Admin only)

**Query Parameters:**
- `skip` (optional, default: 0): Number of users to skip
- `limit` (optional, default: 100, max: 100): Number of users to return

**Response (200 OK):**
```json
{
  "total": 150,
  "page": 1,
  "limit": 100,
  "users": [
    {
      "id": "user-123",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      ...
    }
  ]
}
```

**Response (403 Forbidden):**
```json
{
  "detail": "Only admins can list users"
}
```

### 4. Update Current User
**Endpoint:** `PUT /me`

**Description:** Update current user's information

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "avatar_url": "https://example.com/new-avatar.jpg",
  "bio": "Updated bio"
}
```

**Response (200 OK):** Updated user object

**Response (400 Bad Request):**
```json
{
  "detail": "Error updating user"
}
```

### 5. Update User (Admin)
**Endpoint:** `PUT /{user_id}`

**Description:** Update a specific user's information (Admin or self)

**Parameters:**
- `user_id` (path, required): User ID

**Request Body:** Same as Update Current User

**Response (200 OK):** Updated user object

**Response (403 Forbidden):**
```json
{
  "detail": "Unauthorized"
}
```

### 6. Change Password
**Endpoint:** `POST /me/change-password`

**Description:** Change current user's password

**Request Body:**
```json
{
  "old_password": "currentPassword123",
  "new_password": "newPassword456",
  "confirm_password": "newPassword456"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Old password is incorrect"
}
```

### 7. Deactivate Account
**Endpoint:** `POST /me/deactivate`

**Description:** Deactivate current user's account

**Request Body:**
```json
{
  "password": "currentPassword123",
  "reason": "Taking a break"
}
```

**Response (200 OK):**
```json
{
  "message": "User deactivated successfully"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Password is incorrect"
}
```

### 8. Delete Account
**Endpoint:** `POST /me/delete`

**Description:** Permanently delete current user's account

**Request Body:**
```json
{
  "password": "currentPassword123",
  "confirmation": "DELETE",
  "reason": "No longer needed"
}
```

**Response (200 OK):**
```json
{
  "message": "User deleted successfully"
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Password is incorrect"
}
```

### 9. Deactivate User (Admin)
**Endpoint:** `POST /{user_id}/deactivate`

**Description:** Deactivate a user account (Admin only)

**Parameters:**
- `user_id` (path, required): User ID

**Response (200 OK):**
```json
{
  "message": "User deactivated successfully"
}
```

### 10. Activate User (Admin)
**Endpoint:** `POST /{user_id}/activate`

**Description:** Activate a user account (Admin only)

**Parameters:**
- `user_id` (path, required): User ID

**Response (200 OK):**
```json
{
  "message": "User activated successfully"
}
```

### 11. Delete User (Admin)
**Endpoint:** `POST /{user_id}/delete`

**Description:** Delete a user account (Admin only)

**Parameters:**
- `user_id` (path, required): User ID

**Response (200 OK):**
```json
{
  "message": "User deleted successfully"
}
```

### 12. Search Users
**Endpoint:** `GET /search/query`

**Description:** Search users by email or name (Admin only)

**Query Parameters:**
- `q` (required): Search query
- `limit` (optional, default: 10, max: 100): Number of results

**Response (200 OK):**
```json
{
  "total": 5,
  "results": [
    {
      "id": "user-123",
      "email": "user@example.com",
      ...
    }
  ]
}
```

### 13. Get User Statistics
**Endpoint:** `GET /stats/overview`

**Description:** Get user statistics (Admin only)

**Response (200 OK):**
```json
{
  "total_users": 1000,
  "active_users": 850,
  "inactive_users": 150,
  "verified_emails": 950,
  "two_factor_enabled": 200,
  "average_projects": 3.5
}
```

### 14. Get User Preferences
**Endpoint:** `GET /me/preferences`

**Description:** Get current user's preferences

**Response (200 OK):**
```json
{
  "email_notifications": true,
  "push_notifications": true,
  "marketing_emails": false,
  "theme": "dark",
  "language": "en"
}
```

### 15. Update User Preferences
**Endpoint:** `PUT /me/preferences`

**Description:** Update current user's preferences

**Request Body:**
```json
{
  "email_notifications": false,
  "push_notifications": true,
  "marketing_emails": false,
  "theme": "light",
  "language": "ar"
}
```

**Response (200 OK):** Updated preferences object

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error.email"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Usage Examples

### Get Current User
```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer <token>"
```

### Update User Profile
```bash
curl -X PUT "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "bio": "Updated bio"
  }'
```

### Change Password
```bash
curl -X POST "http://localhost:8000/api/users/me/change-password" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "currentPassword123",
    "new_password": "newPassword456",
    "confirm_password": "newPassword456"
  }'
```

### Search Users (Admin)
```bash
curl -X GET "http://localhost:8000/api/users/search/query?q=john&limit=10" \
  -H "Authorization: Bearer <admin_token>"
```

### Get User Statistics (Admin)
```bash
curl -X GET "http://localhost:8000/api/users/stats/overview" \
  -H "Authorization: Bearer <admin_token>"
```

## Rate Limiting
- Standard endpoints: 100 requests per minute
- Search endpoints: 50 requests per minute
- Admin endpoints: 200 requests per minute

## Pagination
List endpoints support pagination with `skip` and `limit` query parameters:
- Default limit: 100
- Maximum limit: 100
- Default skip: 0

## Data Validation
- Email: Valid email format required
- First Name: 1-100 characters
- Last Name: 1-100 characters
- Password: Minimum 8 characters
- Bio: Maximum 500 characters

## Response Headers
All responses include:
- `Content-Type: application/json`
- `X-Request-ID: <unique-request-id>`
- `X-RateLimit-Limit: <limit>`
- `X-RateLimit-Remaining: <remaining>`
- `X-RateLimit-Reset: <reset-timestamp>`
