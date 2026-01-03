# Vividly - AI Website Builder Platform

**Vividly** is a next-generation AI-powered website builder that enables users to describe their website ideas in natural language and automatically generate fully functional, production-ready websites.

## 🎯 Project Overview

Vividly transforms the way websites are built by combining:
- **AI-Powered Code Generation** - Convert ideas to code automatically
- **Live Development Environment** - Real-time preview and editing
- **Full-Stack Capabilities** - Backend + Frontend + Database
- **Third-Party Integrations** - Connect with 50+ services
- **Production Deployment** - One-click deployment to production
- **Domain Management** - Automatic domain registration and SSL

## 📋 Project Structure

```
vividly-core/
├── backend/              # FastAPI backend
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── routes/          # API routes
│   ├── utils/           # Utility functions
│   ├── main.py          # FastAPI app
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile       # Docker configuration
├── frontend/            # React frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile.dev
├── docs/                # Documentation
├── docker-compose.yml   # Docker Compose setup
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend development)
- PostgreSQL 15+ (if running without Docker)

### Using Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/alhusseinweb/vividly-core.git
cd vividly-core
```

2. **Create environment file**
```bash
cp backend/.env.example backend/.env
```

3. **Start services**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development Setup

1. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

2. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

## 📚 API Documentation

### Health Check
```bash
GET /health
```

### Authentication Endpoints (Phase 1)
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password

### User Endpoints (Phase 1)
- `GET /api/users/me` - Get current user
- `PUT /api/users/me` - Update user profile
- `POST /api/users/change-password` - Change password

Interactive API documentation available at: http://localhost:8000/docs

## 🏗️ Architecture

### Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM for database
- PostgreSQL - Primary database
- Redis - Caching and sessions
- JWT - Authentication tokens
- Pydantic - Data validation

**Frontend:**
- React 19 - UI framework
- TypeScript - Type safety
- Tailwind CSS - Styling
- shadcn/ui - Component library
- Zustand - State management

**DevOps:**
- Docker - Containerization
- Docker Compose - Local development
- GitHub Actions - CI/CD
- Railway.app - Deployment

## 📋 Development Phases

### Phase 1: Critical Foundation (Current)
- ✅ Database design
- ✅ Authentication system
- ✅ User management
- ✅ Basic dashboard

### Phase 2: Code Generation Engine
- AI-powered code generation
- Design-to-code conversion
- Template system

### Phase 3: Development Environment
- Live preview
- Code editor
- Version control

### Phase 4: Error Detection & Fixing
- Automated error detection
- AI-powered fixes
- Testing framework

### Phase 5: Service Integrations
- Third-party API connections
- Webhook support
- Service marketplace

### Phase 6: Deployment & Production
- CI/CD pipeline
- Production environment
- Monitoring & logging

### Phase 7: Domain Management
- Domain registration
- DNS management
- SSL certificates

### Phase 8: User Dashboards
- User dashboard
- Admin dashboard
- Analytics

### Phase 9: Security & Compliance
- Encryption
- GDPR compliance
- SOC 2 certification

### Phase 10: Monitoring & Support
- Uptime monitoring
- Support system
- Analytics

## 🔐 Security

- Password hashing with bcrypt
- JWT-based authentication
- HTTPS/TLS encryption
- CORS protection
- Rate limiting
- Input validation
- SQL injection prevention

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test
pytest tests/test_auth.py
```

## 📝 Code Style

We follow PEP 8 standards. Use the following tools:

```bash
# Format code
black .

# Check linting
flake8 .

# Sort imports
isort .

# Type checking
mypy .
```

## 🤝 Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- **Project Lead:** Vividly Team
- **Backend:** FastAPI Development Team
- **Frontend:** React Development Team

## 📞 Support

For support, email support@vividly.ai or open an issue on GitHub.

## 🎉 Acknowledgments

- FastAPI community
- React community
- PostgreSQL team
- All contributors

---

**Last Updated:** January 3, 2026
**Version:** 1.0.0
**Status:** In Development (Phase 1)
