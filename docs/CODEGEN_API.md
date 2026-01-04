# Code Generation API Documentation

## Overview
The Code Generation API uses Google Gemini to generate complete, production-ready code from natural language descriptions.

## Base URL
```
/api/codegen
```

## Authentication
All endpoints require JWT authentication token in the `Authorization` header:
```
Authorization: Bearer <token>
```

## Endpoints

### 1. Generate HTML Code
**Endpoint:** `POST /html`

**Description:** Generate complete HTML website from vibe description

**Request Body:**
```json
{
  "vibe_description": "Modern, minimalist design with vibrant colors and smooth animations. Should feel professional yet creative. Include a hero section with call-to-action buttons, features showcase, and testimonials section.",
  "language": "html",
  "framework": null
}
```

**Response (200 OK):**
```json
{
  "project_id": "",
  "status": "generated",
  "generated_code": "<!DOCTYPE html>...",
  "preview_url": null,
  "estimated_time": 2.5
}
```

### 2. Generate React Code
**Endpoint:** `POST /react`

**Description:** Generate React component from vibe description

**Request Body:**
```json
{
  "vibe_description": "Modern, minimalist design with vibrant colors and smooth animations...",
  "language": "react",
  "framework": null
}
```

**Response (200 OK):**
```json
{
  "project_id": "",
  "status": "generated",
  "generated_code": "import React from 'react'...",
  "preview_url": null,
  "estimated_time": 2.5
}
```

### 3. Generate CSS Code
**Endpoint:** `POST /css`

**Description:** Generate CSS from vibe description

**Query Parameters:**
- `vibe_description` (required): Description of the desired design

**Response (200 OK):**
```json
{
  "status": "generated",
  "generated_code": "/* CSS code */"
}
```

### 4. Generate Project Structure
**Endpoint:** `POST /project-structure`

**Description:** Generate project structure and component breakdown

**Query Parameters:**
- `vibe_description` (required): Description of the project

**Response (200 OK):**
```json
{
  "status": "generated",
  "structure": {
    "folder_structure": [
      "src/",
      "src/components/",
      "src/pages/",
      "src/styles/",
      "public/"
    ],
    "components": [
      "Header",
      "Hero",
      "Features",
      "Testimonials",
      "Footer"
    ],
    "pages": [
      "Home",
      "About",
      "Contact"
    ],
    "styling": "Tailwind CSS with custom animations",
    "libraries": [
      "React",
      "Tailwind CSS",
      "Framer Motion"
    ],
    "performance": [
      "Code splitting",
      "Image optimization",
      "Lazy loading"
    ],
    "seo": [
      "Meta tags",
      "Structured data",
      "Sitemap"
    ],
    "accessibility": [
      "ARIA labels",
      "Semantic HTML",
      "Keyboard navigation"
    ],
    "compatibility": [
      "Chrome",
      "Firefox",
      "Safari",
      "Edge"
    ]
  }
}
```

### 5. Optimize Code
**Endpoint:** `POST /optimize`

**Description:** Optimize generated code for performance and best practices

**Query Parameters:**
- `code` (required): Code to optimize
- `language` (optional, default: "html"): Programming language

**Response (200 OK):**
```json
{
  "status": "optimized",
  "optimized_code": "/* optimized code */"
}
```

### 6. Generate Code for Project
**Endpoint:** `POST /project/{project_id}/generate`

**Description:** Generate code for a specific project and save it

**Path Parameters:**
- `project_id` (required): Project ID

**Query Parameters:**
- `language` (optional, default: "html"): Programming language (html, react, vue, svelte)

**Response (200 OK):**
```json
{
  "project_id": "project-123",
  "status": "generated",
  "generated_code": "<!DOCTYPE html>...",
  "language": "html"
}
```

## Vibe Description Guidelines

### Effective Vibe Descriptions

A good vibe description should include:

1. **Overall Aesthetic**
   - Modern, minimalist, vintage, futuristic, etc.
   - Professional, playful, serious, creative, etc.

2. **Color Palette**
   - Primary colors
   - Accent colors
   - Background colors
   - Specific color combinations

3. **Typography**
   - Font styles (serif, sans-serif, monospace)
   - Font weights
   - Text hierarchy

4. **Layout**
   - Grid vs. organic
   - Symmetrical vs. asymmetrical
   - Spacing and padding

5. **Components**
   - Buttons (flat, rounded, gradient, etc.)
   - Cards (minimal, shadow, border, etc.)
   - Navigation style
   - Forms and inputs

6. **Animations**
   - Smooth transitions
   - Hover effects
   - Scroll animations
   - Loading states

7. **Specific Features**
   - Hero section
   - Feature showcase
   - Testimonials
   - Call-to-action buttons
   - Contact form
   - Footer

### Example Vibe Descriptions

#### Example 1: Modern SaaS Landing Page
```
Modern, clean SaaS landing page with a dark theme and vibrant cyan accents. 
Minimalist design with plenty of whitespace. 
Hero section with gradient background and animated text. 
Feature cards with icons and descriptions. 
Smooth animations on scroll. 
Call-to-action buttons with hover effects. 
Professional typography with Poppins font. 
Responsive design for all devices.
```

#### Example 2: Creative Agency Portfolio
```
Bold, creative agency portfolio with dark background and colorful accents. 
Asymmetric layout with overlapping elements. 
Large, eye-catching typography. 
Animated hero section with parallax effect. 
Project showcase with image galleries. 
Smooth page transitions. 
Modern, trendy design. 
Playful interactions and micro-animations.
```

#### Example 3: E-commerce Product Page
```
Clean, professional e-commerce product page. 
White background with subtle shadows. 
High-quality product images with zoom functionality. 
Clear product information and specifications. 
Customer reviews and ratings. 
Easy-to-use shopping cart. 
Trust badges and security indicators. 
Mobile-optimized design.
```

## Response Format

All code generation endpoints return code that includes:

1. **HTML Generation**
   - Complete HTML5 document
   - Embedded CSS and JavaScript
   - Responsive design
   - Accessibility features
   - SEO optimization

2. **React Generation**
   - Functional components with hooks
   - Tailwind CSS styling
   - TypeScript types
   - Error handling
   - Performance optimization

3. **CSS Generation**
   - CSS Grid and Flexbox layouts
   - Animations and transitions
   - CSS variables
   - Responsive design
   - Cross-browser compatibility

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Gemini API key not configured"
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

### 500 Internal Server Error
```json
{
  "detail": "Error generating code: [error message]"
}
```

## Usage Examples

### Generate HTML Code
```bash
curl -X POST "http://localhost:8000/api/codegen/html" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "vibe_description": "Modern, minimalist design with vibrant colors...",
    "language": "html"
  }'
```

### Generate React Code
```bash
curl -X POST "http://localhost:8000/api/codegen/react" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "vibe_description": "Modern, minimalist design with vibrant colors...",
    "language": "react"
  }'
```

### Generate CSS
```bash
curl -X POST "http://localhost:8000/api/codegen/css?vibe_description=Modern%20design%20with%20vibrant%20colors" \
  -H "Authorization: Bearer <token>"
```

### Generate Project Structure
```bash
curl -X POST "http://localhost:8000/api/codegen/project-structure?vibe_description=Modern%20design%20with%20vibrant%20colors" \
  -H "Authorization: Bearer <token>"
```

### Optimize Code
```bash
curl -X POST "http://localhost:8000/api/codegen/optimize?language=html" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "<!DOCTYPE html>..."
  }'
```

### Generate Code for Project
```bash
curl -X POST "http://localhost:8000/api/codegen/project/project-123/generate?language=html" \
  -H "Authorization: Bearer <token>"
```

## Configuration

### Google Gemini API Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Set environment variable:
   ```
   GOOGLE_GEMINI_API_KEY=your_api_key
   ```

## Rate Limiting
- Code generation endpoints: 20 requests per minute per user
- Optimization endpoints: 50 requests per minute per user
- Project generation: 10 requests per minute per project

## Best Practices

1. **Detailed Descriptions:** Provide detailed vibe descriptions for better results
2. **Iterative Refinement:** Generate code, review, and regenerate with adjustments
3. **Code Review:** Always review generated code before using in production
4. **Testing:** Test generated code thoroughly
5. **Customization:** Customize generated code to fit your specific needs
6. **Performance:** Optimize generated code for your use case

## Limitations

1. **Code Quality:** Generated code may need refinement
2. **Complexity:** Very complex designs may not generate perfectly
3. **Uniqueness:** Generated code follows common patterns
4. **Dependencies:** May require additional libraries
5. **Accessibility:** Review accessibility features carefully

## Future Enhancements

- [ ] Support for Vue.js and Svelte
- [ ] Code generation for backend (Node.js, Python)
- [ ] Database schema generation
- [ ] API endpoint generation
- [ ] Component library generation
- [ ] Design system generation
- [ ] Testing code generation
- [ ] Documentation generation
