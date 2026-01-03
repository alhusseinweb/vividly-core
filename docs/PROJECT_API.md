# Project Management API Documentation

## Overview
The Project Management API provides endpoints for creating, managing, and deploying projects using AI-powered code generation.

## Base URL
```
/api/projects
```

## Authentication
All endpoints require JWT authentication token in the `Authorization` header:
```
Authorization: Bearer <token>
```

## Endpoints

### 1. Create Project
**Endpoint:** `POST /`

**Description:** Create a new project

**Request Body:**
```json
{
  "name": "My Awesome Website",
  "description": "A beautiful landing page for my startup",
  "vibe_description": "Modern, minimalist design with vibrant colors and smooth animations. Should feel professional yet creative. Include a hero section with call-to-action buttons, features showcase, and testimonials section."
}
```

**Response (201 Created):**
```json
{
  "id": "project-123",
  "user_id": "user-123",
  "name": "My Awesome Website",
  "description": "A beautiful landing page for my startup",
  "vibe_description": "Modern, minimalist design...",
  "slug": "my-awesome-website",
  "status": "draft",
  "generated_code": null,
  "preview_url": null,
  "live_url": null,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "published_at": null
}
```

### 2. List Projects
**Endpoint:** `GET /`

**Description:** List user's projects with pagination

**Query Parameters:**
- `skip` (optional, default: 0): Number of projects to skip
- `limit` (optional, default: 50, max: 100): Number of projects to return

**Response (200 OK):**
```json
{
  "total": 15,
  "page": 1,
  "limit": 50,
  "projects": [
    {
      "id": "project-123",
      "user_id": "user-123",
      "name": "My Awesome Website",
      ...
    }
  ]
}
```

### 3. Get Project
**Endpoint:** `GET /{project_id}`

**Description:** Get a specific project

**Parameters:**
- `project_id` (path, required): Project ID

**Response (200 OK):** Project object

**Response (404 Not Found):**
```json
{
  "detail": "Project not found"
}
```

### 4. Update Project
**Endpoint:** `PUT /{project_id}`

**Description:** Update project information

**Parameters:**
- `project_id` (path, required): Project ID

**Request Body:**
```json
{
  "name": "Updated Project Name",
  "description": "Updated description",
  "vibe_description": "Updated vibe description",
  "status": "draft"
}
```

**Response (200 OK):** Updated project object

### 5. Delete Project
**Endpoint:** `DELETE /{project_id}`

**Description:** Delete a project

**Parameters:**
- `project_id` (path, required): Project ID

**Response (200 OK):**
```json
{
  "message": "Project deleted successfully"
}
```

### 6. Generate Code
**Endpoint:** `POST /{project_id}/generate-code`

**Description:** Generate project code using AI based on vibe description

**Parameters:**
- `project_id` (path, required): Project ID

**Request Body:**
```json
{
  "vibe_description": "Modern, minimalist design with vibrant colors...",
  "language": "html",
  "framework": null
}
```

**Response (200 OK):**
```json
{
  "project_id": "project-123",
  "status": "generated",
  "generated_code": "<!DOCTYPE html>...",
  "preview_url": "https://preview.vividly.app/project-123",
  "estimated_time": 2.5
}
```

### 7. Publish Project
**Endpoint:** `POST /{project_id}/publish`

**Description:** Publish project to production

**Parameters:**
- `project_id` (path, required): Project ID

**Request Body:**
```json
{
  "domain": "mywebsite.com",
  "enable_analytics": true
}
```

**Response (200 OK):**
```json
{
  "project_id": "project-123",
  "status": "published",
  "live_url": "https://mywebsite.com",
  "domain": "mywebsite.com"
}
```

### 8. Archive Project
**Endpoint:** `POST /{project_id}/archive`

**Description:** Archive a project

**Parameters:**
- `project_id` (path, required): Project ID

**Response (200 OK):**
```json
{
  "message": "Project archived successfully"
}
```

### 9. Duplicate Project
**Endpoint:** `POST /{project_id}/duplicate`

**Description:** Create a copy of a project

**Parameters:**
- `project_id` (path, required): Project ID

**Response (200 OK):**
```json
{
  "original_id": "project-123",
  "new_id": "project-456",
  "new_project": {
    "id": "project-456",
    "name": "My Awesome Website (Copy)",
    ...
  }
}
```

### 10. Export Project
**Endpoint:** `POST /{project_id}/export`

**Description:** Export project as file

**Parameters:**
- `project_id` (path, required): Project ID

**Request Body:**
```json
{
  "format": "json",
  "include_assets": true
}
```

**Response (200 OK):**
```json
{
  "project_id": "project-123",
  "export_url": "https://vividly.app/exports/project-123.json",
  "format": "json",
  "size": 1.5,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 11. Get Project Statistics
**Endpoint:** `GET /stats/overview`

**Description:** Get project statistics for current user

**Response (200 OK):**
```json
{
  "total_projects": 15,
  "published_projects": 8,
  "draft_projects": 5,
  "archived_projects": 2,
  "total_views": 5000,
  "total_likes": 250,
  "average_generation_time": 2.3
}
```

### 12. Search Projects
**Endpoint:** `GET /search/query`

**Description:** Search user's projects

**Query Parameters:**
- `q` (required): Search query
- `status` (optional): Filter by status (draft, published, archived)
- `limit` (optional, default: 10, max: 100): Number of results

**Response (200 OK):**
```json
{
  "total": 3,
  "results": [
    {
      "id": "project-123",
      "name": "My Awesome Website",
      ...
    }
  ]
}
```

### 13. Get Project Versions
**Endpoint:** `GET /{project_id}/versions`

**Description:** Get all versions of a project

**Parameters:**
- `project_id` (path, required): Project ID

**Response (200 OK):**
```json
[
  {
    "id": "version-1",
    "project_id": "project-123",
    "version_number": 3,
    "generated_code": "<!DOCTYPE html>...",
    "created_at": "2024-01-15T10:30:00Z",
    "created_by": "user-123"
  }
]
```

### 14. Get Project Collaborators
**Endpoint:** `GET /{project_id}/collaborators`

**Description:** Get project collaborators

**Parameters:**
- `project_id` (path, required): Project ID

**Response (200 OK):**
```json
[
  {
    "user_id": "user-456",
    "email": "collaborator@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "role": "editor",
    "joined_at": "2024-01-15T10:30:00Z"
  }
]
```

### 15. Add Collaborator
**Endpoint:** `POST /{project_id}/collaborators`

**Description:** Add a collaborator to project

**Parameters:**
- `project_id` (path, required): Project ID

**Request Body:**
```json
{
  "email": "collaborator@example.com",
  "role": "editor"
}
```

**Response (201 Created):**
```json
{
  "user_id": "user-456",
  "email": "collaborator@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "role": "editor",
  "joined_at": "2024-01-15T10:30:00Z"
}
```

### 16. Remove Collaborator
**Endpoint:** `DELETE /{project_id}/collaborators/{user_id}`

**Description:** Remove a collaborator from project

**Parameters:**
- `project_id` (path, required): Project ID
- `user_id` (path, required): Collaborator user ID

**Response (200 OK):**
```json
{
  "message": "Collaborator removed"
}
```

### 17. Update Collaborator Role
**Endpoint:** `PUT /{project_id}/collaborators/{user_id}`

**Description:** Update collaborator role

**Parameters:**
- `project_id` (path, required): Project ID
- `user_id` (path, required): Collaborator user ID

**Request Body:**
```json
{
  "user_id": "user-456",
  "role": "viewer"
}
```

**Response (200 OK):**
```json
{
  "message": "Collaborator role updated"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Unauthorized"
}
```

### 404 Not Found
```json
{
  "detail": "Project not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "vibe_description"],
      "msg": "ensure this value has at least 10 characters",
      "type": "value_error.string.min_length"
    }
  ]
}
```

## Usage Examples

### Create a Project
```bash
curl -X POST "http://localhost:8000/api/projects" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Website",
    "description": "A cool website",
    "vibe_description": "Modern design with vibrant colors..."
  }'
```

### Generate Code
```bash
curl -X POST "http://localhost:8000/api/projects/project-123/generate-code" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "vibe_description": "Modern design with vibrant colors...",
    "language": "html"
  }'
```

### Publish Project
```bash
curl -X POST "http://localhost:8000/api/projects/project-123/publish" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "mywebsite.com",
    "enable_analytics": true
  }'
```

### List Projects
```bash
curl -X GET "http://localhost:8000/api/projects?skip=0&limit=50" \
  -H "Authorization: Bearer <token>"
```

## Data Validation

- **Project Name:** 1-200 characters
- **Description:** Maximum 1000 characters
- **Vibe Description:** 10-2000 characters (required for code generation)
- **Status:** "draft", "generated", "published", "archived"
- **Language:** "html", "react", "vue", "svelte"
- **Collaborator Role:** "editor", "viewer"

## Rate Limiting
- Standard endpoints: 100 requests per minute
- Code generation: 20 requests per minute
- Publishing: 50 requests per minute

## Project Lifecycle

1. **Draft** - Initial state, project created but not generated
2. **Generated** - Code has been generated using AI
3. **Published** - Project is live and accessible
4. **Archived** - Project is archived but can be restored

## Collaboration Roles

- **Owner** - Full access, can manage collaborators
- **Editor** - Can edit project and generate code
- **Viewer** - Read-only access
