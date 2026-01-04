# OAuth Authentication API Documentation

## Overview
The OAuth API provides endpoints for authenticating users with GitHub and Google OAuth providers.

## Base URL
```
/api/auth/oauth
```

## Endpoints

### 1. GitHub Authorization
**Endpoint:** `GET /github/authorize`

**Description:** Get GitHub OAuth authorization URL

**Response (200 OK):**
```json
{
  "authorization_url": "https://github.com/login/oauth/authorize?client_id=...&redirect_uri=...&scope=user:email&state=vividly_github_oauth"
}
```

### 2. GitHub Callback
**Endpoint:** `GET /github/callback`

**Description:** GitHub OAuth callback endpoint

**Query Parameters:**
- `code` (required): Authorization code from GitHub
- `state` (required): State parameter for security

**Response (200 OK):**
```json
{
  "message": "GitHub authentication successful",
  "user_id": "user-123",
  "email": "user@example.com",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 86400
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Failed to get GitHub access token"
}
```

### 3. Google Authorization
**Endpoint:** `GET /google/authorize`

**Description:** Get Google OAuth authorization URL

**Response (200 OK):**
```json
{
  "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=...&redirect_uri=...&response_type=code&scope=..."
}
```

### 4. Google Callback
**Endpoint:** `GET /google/callback`

**Description:** Google OAuth callback endpoint

**Query Parameters:**
- `code` (required): Authorization code from Google
- `state` (required): State parameter for security

**Response (200 OK):**
```json
{
  "message": "Google authentication successful",
  "user_id": "user-456",
  "email": "user@gmail.com",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 86400
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Failed to get Google access token"
}
```

## OAuth Flow

### GitHub OAuth Flow

1. **User clicks "Sign in with GitHub"**
   ```
   GET /api/auth/oauth/github/authorize
   ```

2. **Redirect to GitHub**
   - User is redirected to GitHub authorization page
   - User grants permissions

3. **GitHub redirects back**
   ```
   GET /api/auth/oauth/github/callback?code=XXXX&state=vividly_github_oauth
   ```

4. **Backend exchanges code for token**
   - Backend calls GitHub API with code
   - Gets access token
   - Fetches user information
   - Creates or updates user in database

5. **Return tokens to frontend**
   ```json
   {
     "access_token": "...",
     "refresh_token": "...",
     "user_id": "..."
   }
   ```

### Google OAuth Flow

1. **User clicks "Sign in with Google"**
   ```
   GET /api/auth/oauth/google/authorize
   ```

2. **Redirect to Google**
   - User is redirected to Google authorization page
   - User grants permissions

3. **Google redirects back**
   ```
   GET /api/auth/oauth/google/callback?code=XXXX&state=vividly_google_oauth
   ```

4. **Backend exchanges code for token**
   - Backend calls Google API with code
   - Gets access token
   - Fetches user information
   - Creates or updates user in database

5. **Return tokens to frontend**
   ```json
   {
     "access_token": "...",
     "refresh_token": "...",
     "user_id": "..."
   }
   ```

## Frontend Implementation

### GitHub OAuth

```javascript
// 1. Get authorization URL
const response = await fetch('/api/auth/oauth/github/authorize');
const { authorization_url } = await response.json();

// 2. Redirect user
window.location.href = authorization_url;

// 3. Handle callback (in your callback page)
const urlParams = new URLSearchParams(window.location.search);
const code = urlParams.get('code');
const state = urlParams.get('state');

// 4. Send code to backend
const callbackResponse = await fetch(
  `/api/auth/oauth/github/callback?code=${code}&state=${state}`
);
const { access_token, refresh_token, user_id } = await callbackResponse.json();

// 5. Store tokens
localStorage.setItem('access_token', access_token);
localStorage.setItem('refresh_token', refresh_token);
localStorage.setItem('user_id', user_id);
```

### Google OAuth

```javascript
// 1. Get authorization URL
const response = await fetch('/api/auth/oauth/google/authorize');
const { authorization_url } = await response.json();

// 2. Redirect user
window.location.href = authorization_url;

// 3. Handle callback (in your callback page)
const urlParams = new URLSearchParams(window.location.search);
const code = urlParams.get('code');
const state = urlParams.get('state');

// 4. Send code to backend
const callbackResponse = await fetch(
  `/api/auth/oauth/google/callback?code=${code}&state=${state}`
);
const { access_token, refresh_token, user_id } = await callbackResponse.json();

// 5. Store tokens
localStorage.setItem('access_token', access_token);
localStorage.setItem('refresh_token', refresh_token);
localStorage.setItem('user_id', user_id);
```

## Configuration

### GitHub OAuth Setup

1. Go to GitHub Settings → Developer settings → OAuth Apps
2. Create a new OAuth App
3. Set Authorization callback URL to: `http://localhost:8000/api/auth/oauth/github/callback`
4. Copy Client ID and Client Secret
5. Set environment variables:
   ```
   GITHUB_CLIENT_ID=your_client_id
   GITHUB_CLIENT_SECRET=your_client_secret
   GITHUB_REDIRECT_URI=http://localhost:8000/api/auth/oauth/github/callback
   ```

### Google OAuth Setup

1. Go to Google Cloud Console → APIs & Services → Credentials
2. Create a new OAuth 2.0 Client ID (Web application)
3. Add Authorized redirect URIs: `http://localhost:8000/api/auth/oauth/google/callback`
4. Copy Client ID and Client Secret
5. Set environment variables:
   ```
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/oauth/google/callback
   ```

## Error Handling

### Invalid State Parameter
```json
{
  "detail": "Invalid state parameter"
}
```

### Failed to Get Access Token
```json
{
  "detail": "Failed to get GitHub access token"
}
```

### Failed to Get User Info
```json
{
  "detail": "Failed to get GitHub user info"
}
```

### Could Not Get Email
```json
{
  "detail": "Could not get user email from GitHub"
}
```

## Security Considerations

1. **State Parameter:** Always validate the state parameter to prevent CSRF attacks
2. **HTTPS:** Always use HTTPS in production
3. **Secure Storage:** Store tokens securely (HttpOnly cookies recommended)
4. **Token Expiration:** Implement token refresh mechanism
5. **Scope Limitation:** Request only necessary scopes
6. **PKCE:** Consider using PKCE for additional security

## User Data Mapping

### GitHub User Data
- Email: `email` field
- Name: `name` field (split into first and last name)
- Avatar: `avatar_url` field
- Bio: `bio` field

### Google User Data
- Email: `email` field
- Name: `name` field (split into first and last name)
- Avatar: `picture` field
- Email Verified: `verified_email` field

## Rate Limiting
- OAuth endpoints: 50 requests per minute per IP
- Callback endpoints: 100 requests per minute per user

## Session Management
- Access token expires in 24 hours
- Refresh token expires in 7 days
- Session information stored in database
- IP address and user agent logged for security
