"""
Google Gemini API service for AI-powered code generation
"""
import google.generativeai as genai
from config import settings
from typing import Optional, Tuple
import logging
import json

logger = logging.getLogger(__name__)


class GeminiService:
    """Google Gemini API service for code generation"""

    @staticmethod
    def initialize():
        """Initialize Gemini API"""
        if settings.GOOGLE_GEMINI_API_KEY:
            genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)
            logger.info("Gemini API initialized successfully")
        else:
            logger.warning("GOOGLE_GEMINI_API_KEY not set")

    @staticmethod
    def generate_html_code(vibe_description: str) -> Tuple[bool, str, Optional[str]]:
        """Generate HTML code based on vibe description"""
        try:
            if not settings.GOOGLE_GEMINI_API_KEY:
                return False, "Gemini API key not configured", None

            model = genai.GenerativeModel("gemini-pro")

            prompt = f"""You are an expert web developer. Based on the following vibe description, generate a complete, modern HTML website with embedded CSS and JavaScript.

Vibe Description:
{vibe_description}

Requirements:
1. Generate complete HTML5 document
2. Include responsive CSS (mobile-first approach)
3. Include smooth animations and transitions
4. Use modern design patterns
5. Include interactive elements
6. Ensure accessibility (ARIA labels, semantic HTML)
7. Optimize for performance
8. Include a favicon
9. Use Google Fonts for typography
10. Ensure cross-browser compatibility

Please generate only the HTML code, no explanations. Start with <!DOCTYPE html> and end with </html>."""

            response = model.generate_content(prompt)
            generated_code = response.text

            # Clean up the response if it contains markdown code blocks
            if generated_code.startswith("```html"):
                generated_code = generated_code[7:]
            if generated_code.endswith("```"):
                generated_code = generated_code[:-3]

            generated_code = generated_code.strip()

            logger.info("HTML code generated successfully")
            return True, "HTML code generated successfully", generated_code

        except Exception as e:
            logger.error(f"Error generating HTML code: {e}")
            return False, f"Error generating code: {str(e)}", None

    @staticmethod
    def generate_react_code(vibe_description: str) -> Tuple[bool, str, Optional[str]]:
        """Generate React component code based on vibe description"""
        try:
            if not settings.GOOGLE_GEMINI_API_KEY:
                return False, "Gemini API key not configured", None

            model = genai.GenerativeModel("gemini-pro")

            prompt = f"""You are an expert React developer. Based on the following vibe description, generate a complete React component with Tailwind CSS.

Vibe Description:
{vibe_description}

Requirements:
1. Generate a functional React component
2. Use React hooks (useState, useEffect, etc.)
3. Include Tailwind CSS for styling
4. Use modern React patterns
5. Include interactive elements
6. Ensure accessibility
7. Include proper TypeScript types
8. Use component composition
9. Include error handling
10. Optimize for performance

Please generate only the React component code. Use TypeScript. Include the necessary imports."""

            response = model.generate_content(prompt)
            generated_code = response.text

            # Clean up the response if it contains markdown code blocks
            if generated_code.startswith("```typescript") or generated_code.startswith("```tsx"):
                generated_code = generated_code.split("\n", 1)[1]
            if generated_code.startswith("```jsx") or generated_code.startswith("```javascript"):
                generated_code = generated_code.split("\n", 1)[1]
            if generated_code.endswith("```"):
                generated_code = generated_code[:-3]

            generated_code = generated_code.strip()

            logger.info("React code generated successfully")
            return True, "React code generated successfully", generated_code

        except Exception as e:
            logger.error(f"Error generating React code: {e}")
            return False, f"Error generating code: {str(e)}", None

    @staticmethod
    def generate_project_structure(vibe_description: str) -> Tuple[bool, str, Optional[dict]]:
        """Generate project structure and components based on vibe description"""
        try:
            if not settings.GOOGLE_GEMINI_API_KEY:
                return False, "Gemini API key not configured", None

            model = genai.GenerativeModel("gemini-pro")

            prompt = f"""You are an expert web architect. Based on the following vibe description, generate a project structure and component breakdown.

Vibe Description:
{vibe_description}

Please provide:
1. Project folder structure
2. Main components needed
3. Pages/routes
4. CSS/styling approach
5. JavaScript/TypeScript requirements
6. External libraries needed
7. Performance considerations
8. SEO considerations
9. Accessibility features
10. Browser compatibility

Format the response as JSON with the following structure:
{{
  "folder_structure": [...],
  "components": [...],
  "pages": [...],
  "styling": "...",
  "libraries": [...],
  "performance": [...],
  "seo": [...],
  "accessibility": [...],
  "compatibility": [...]
}}"""

            response = model.generate_content(prompt)
            response_text = response.text

            # Clean up the response if it contains markdown code blocks
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            response_text = response_text.strip()

            # Parse JSON
            structure = json.loads(response_text)

            logger.info("Project structure generated successfully")
            return True, "Project structure generated successfully", structure

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return False, "Error parsing generated structure", None
        except Exception as e:
            logger.error(f"Error generating project structure: {e}")
            return False, f"Error generating structure: {str(e)}", None

    @staticmethod
    def optimize_code(code: str, language: str = "html") -> Tuple[bool, str, Optional[str]]:
        """Optimize generated code for performance and best practices"""
        try:
            if not settings.GOOGLE_GEMINI_API_KEY:
                return False, "Gemini API key not configured", None

            model = genai.GenerativeModel("gemini-pro")

            prompt = f"""You are an expert code optimizer. Optimize the following {language} code for:
1. Performance
2. Best practices
3. Accessibility
4. SEO (if applicable)
5. Security
6. Code readability
7. Browser compatibility

Code:
{code}

Please provide only the optimized code, no explanations."""

            response = model.generate_content(prompt)
            optimized_code = response.text

            # Clean up the response if it contains markdown code blocks
            if optimized_code.startswith(f"```{language}"):
                optimized_code = optimized_code.split("\n", 1)[1]
            if optimized_code.endswith("```"):
                optimized_code = optimized_code[:-3]

            optimized_code = optimized_code.strip()

            logger.info("Code optimized successfully")
            return True, "Code optimized successfully", optimized_code

        except Exception as e:
            logger.error(f"Error optimizing code: {e}")
            return False, f"Error optimizing code: {str(e)}", None

    @staticmethod
    def generate_css_from_vibe(vibe_description: str) -> Tuple[bool, str, Optional[str]]:
        """Generate CSS based on vibe description"""
        try:
            if not settings.GOOGLE_GEMINI_API_KEY:
                return False, "Gemini API key not configured", None

            model = genai.GenerativeModel("gemini-pro")

            prompt = f"""You are an expert CSS designer. Based on the following vibe description, generate modern CSS that captures the essence of the design.

Vibe Description:
{vibe_description}

Requirements:
1. Use CSS Grid and Flexbox
2. Include animations and transitions
3. Use CSS variables for colors and spacing
4. Include responsive design
5. Optimize for performance
6. Use modern CSS features
7. Include accessibility considerations
8. Ensure cross-browser compatibility

Please generate only the CSS code, no explanations. Start with /* CSS */ or directly with selectors."""

            response = model.generate_content(prompt)
            generated_css = response.text

            # Clean up the response if it contains markdown code blocks
            if generated_css.startswith("```css"):
                generated_css = generated_css[6:]
            if generated_css.endswith("```"):
                generated_css = generated_css[:-3]

            generated_css = generated_css.strip()

            logger.info("CSS generated successfully")
            return True, "CSS generated successfully", generated_css

        except Exception as e:
            logger.error(f"Error generating CSS: {e}")
            return False, f"Error generating CSS: {str(e)}", None
