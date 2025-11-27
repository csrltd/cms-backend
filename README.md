# 🚀 CMS Backend API

A modern, scalable Content Management System API built with Django REST Framework, featuring a clean layered architecture, comprehensive testing, and production-ready configurations.

## ✨ Features

- **📝 Blog Management** - Full CRUD operations with rich text content
- **📂 Category System** - Organize content with hierarchical categories
- **📧 Contact Forms** - Handle inquiries with email notifications
- **🖼️ Media Handling** - Local development + Cloudflare R2 production storage
- **🔍 Advanced Filtering** - Filter blogs by category, date range
- **📱 RESTful API** - Clean, consistent API design
- **🧪 Comprehensive Testing** - 34+ tests with Factory Boy
- **📚 API Documentation** - Interactive Swagger/OpenAPI docs
- **⚡ Performance** - Redis caching, optimized queries
- **🔧 Background Tasks** - Celery for email processing

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Views    │───▶│  Services   │───▶│ Repositories│───▶│   Models    │
│ (API Layer) │    │(Business    │    │(Data Access)│    │ (Database)  │
│             │    │ Logic)      │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Clean Layered Architecture
- **Views**: Handle HTTP requests/responses
- **Services**: Business logic and validation
- **Repositories**: Database operations
- **Models**: Data structure and relationships

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- uv (Python package manager)
- Redis (for caching and Celery)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd cms-backend

# Install dependencies
uv sync

# Setup environment
cp .env.example .env
# Edit .env with your configurations

# Run migrations
uv run python manage.py migrate

# Create test data
uv run python setup_test_data.py

# Start development server
uv run python manage.py runserver
```

### 🌐 Access Points
- **API Base**: http://127.0.0.1:8000/api/
- **Admin Panel**: http://127.0.0.1:8000/admin/ (admin/admin123)
- **API Documentation**: http://127.0.0.1:8000/api/docs/

## 📡 API Endpoints

### Blog Management
```
GET    /api/blogs/                    # List published blogs
GET    /api/blogs/?category=tech      # Filter by category
GET    /api/blogs/?date_from=2024-01-01&date_to=2024-12-31  # Date range
GET    /api/blogs/{slug}/             # Get single blog
POST   /api/blogs/                    # Create blog (auth required)
PUT    /api/blogs/{slug}/             # Update blog (auth required)
DELETE /api/blogs/{slug}/             # Delete blog (auth required)
```

### Category Management
```
GET    /api/categories/               # List all categories
GET    /api/categories/{slug}/        # Category details + blogs
```

### Contact Forms
```
POST   /api/contact/                  # Submit contact form
```

### Documentation
```
GET    /api/docs/                     # Interactive Swagger UI
GET    /api/schema/                   # OpenAPI schema
```

## 🧪 Testing

```bash
# Run all tests
uv run python manage.py test

# Run specific app tests
uv run python manage.py test blog.tests
uv run python manage.py test contact.tests

# Check code coverage
uv run python manage.py test --with-coverage
```
## 🏭 Production Deployment

### Media Storage
- **Development**: Local file storage
- **Production**: Cloudflare R2 (CDN + Storage)

### Background Tasks
```bash
# Start Celery worker
celery -A core worker --loglevel=info

# Start Celery beat (scheduled tasks)
celery -A core beat --loglevel=info
```

### Performance Features
- **Redis Caching**: Blog list caching
- **Query Optimization**: `select_related()` for relationships
- **CDN Integration**: Cloudflare for media delivery
- **Background Processing**: Email sending via Celery

## 📊 Project Structure

```
cms-backend/
├── core/                    # Django project settings
├── base/                    # Shared utilities and base classes
│   ├── models.py           # BaseModel with audit fields
│   ├── responses.py        # Standardized response classes
│   └── utils/              # Utility functions
├── blog/                   # Blog management app
│   ├── models.py           # Blog and Category models
│   ├── serializers.py     # API serializers
│   ├── views.py            # API endpoints
│   ├── repository/         # Data access layer
│   ├── service/            # Business logic layer
│   └── tests/              # Comprehensive test suite
├── contact/                # Contact form app
│   ├── models.py           # ContactMessage model
│   ├── tasks.py            # Celery email tasks
│   ├── repository/         # Data access layer
│   ├── service/            # Business logic layer
│   └── tests/              # Test suite
├── api/                    # API URL routing
│   └── urls/               # Modular URL configuration
├── media/                  # Local media storage (development)
├── logs/                   # Application logs
└── requirements.txt        # Python dependencies
```

### Code Quality
- **Logging**: Structured logging with Loguru
- **Error Handling**: Comprehensive try/catch blocks
- **Type Hints**: Python typing for better IDE support
- **Documentation**: Inline docstrings and API docs

## 👥 Team

**Development Team**: Tuombe • Paccy • Christian
