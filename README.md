# 🚀 Vendor Django REST API

A robust Django REST API backend with OTP-based authentication and user management system. Built with Django REST Framework and Token Authentication.

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [API Documentation](#-api-documentation)
- [Database Models](#-database-models)
- [Testing](#-testing)
- [Admin Interface](#-admin-interface)
- [Development](#-development)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

## ✨ Features

- **🔐 OTP Authentication**: Secure 6-digit OTP generation and verification
- **📧 Email Integration**: Console-based email output for development
- **👤 User Management**: Complete user registration and authentication
- **🔑 Token Authentication**: Django REST Framework token-based auth
- **⏰ OTP Expiry**: 5-minute expiration for security
- **🛡️ Input Validation**: Comprehensive request validation
- **📊 Admin Interface**: Django admin for OTP management
- **🧪 Error Handling**: Robust error handling and responses

## 🛠 Tech Stack

- **Backend Framework**: Django 5.2.4
- **API Framework**: Django REST Framework 3.16.0
- **Authentication**: Token Authentication
- **Database**: SQLite (development)
- **Email Backend**: Console Email Backend
- **Python Version**: 3.x
- **Virtual Environment**: venv

## 📁 Project Structure

```
vendor python app/
├── venv/                          # Virtual environment
├── vendor_project/                # Main Django project
│   ├── __init__.py
│   ├── settings.py               # DRF and email configuration
│   ├── urls.py                   # Main URL patterns
│   ├── wsgi.py
│   └── asgi.py
├── vendor/                        # Vendor app
│   ├── __init__.py
│   ├── admin.py                  # EmailOTP admin interface
│   ├── apps.py
│   ├── models.py                 # EmailOTP model
│   ├── serializers.py            # API serializers
│   ├── urls.py                   # App URL patterns
│   ├── views.py                  # API views
│   ├── tests.py
│   └── migrations/
│       └── 0001_initial.py      # Database migration
├── manage.py
├── db.sqlite3                    # SQLite database
└── README.md                     # This file
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step-by-Step Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd "D:\vendor python app"
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment (Windows)
   .\venv\Scripts\Activate.ps1
   
   # Activate virtual environment (Linux/Mac)
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/vendor/
```

### Authentication
- **Type**: Token Authentication
- **Header**: `Authorization: Token <your-token>`

### Endpoints

#### 1. Send OTP
**POST** `/api/vendor/send-otp/`

Sends a 6-digit OTP to the specified email address.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "OTP sent to your email."
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/vendor/send-otp/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

**Python Example:**
```python
import requests

url = "http://localhost:8000/api/vendor/send-otp/"
data = {"email": "user@example.com"}
response = requests.post(url, json=data)
print(response.json())
```

#### 2. Verify OTP
**POST** `/api/vendor/verify-otp/`

Verifies the OTP and returns an authentication token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

**Response:**
```json
{
  "message": "Login successful",
  "token": "your-auth-token-here"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/vendor/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "otp": "123456"}'
```

**Python Example:**
```python
import requests

url = "http://localhost:8000/api/vendor/verify-otp/"
data = {
    "email": "user@example.com",
    "otp": "123456"
}
response = requests.post(url, json=data)
result = response.json()
print(f"Token: {result.get('token')}")
```

#### 3. User Signup
**POST** `/api/vendor/signup/`

Creates a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "yourPassword123"
}
```

**Response:**
```json
{
  "message": "Signup successful"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/vendor/signup/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "John Doe", "password": "yourPassword123"}'
```

**Python Example:**
```python
import requests

url = "http://localhost:8000/api/vendor/signup/"
data = {
    "email": "user@example.com",
    "name": "John Doe",
    "password": "yourPassword123"
}
response = requests.post(url, json=data)
print(response.json())
```

### Error Responses

**Validation Error (400):**
```json
{
  "email": ["This field is required."]
}
```

**OTP Expired (400):**
```json
{
  "error": "OTP has expired"
}
```

**Invalid OTP (400):**
```json
{
  "error": "Invalid OTP"
}
```

**Server Error (500):**
```json
{
  "error": "Failed to send OTP. Please try again."
}
```

## 🗄️ Database Models

### EmailOTP Model

```python
class EmailOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
```

**Fields:**
- `email`: Email address for OTP delivery
- `otp`: 6-digit OTP code
- `created_at`: Timestamp when OTP was created
- `is_verified`: Boolean flag for OTP usage status

**Methods:**
- `is_expired()`: Checks if OTP is expired (5 minutes)
- `generate_otp()`: Generates a random 6-digit OTP
- `create_otp(email)`: Creates a new OTP for the given email

## 🧪 Testing

### Manual Testing

1. **Start the server:**
   ```bash
   python manage.py runserver
   ```

2. **Test Send OTP:**
   - Send POST request to `/api/vendor/send-otp/`
   - Check console output for OTP email

3. **Test Verify OTP:**
   - Use OTP from console output
   - Send POST request to `/api/vendor/verify-otp/`
   - Verify you receive an authentication token

4. **Test Signup:**
   - Send POST request to `/api/vendor/signup/`
   - Verify user creation

### Automated Testing

Run Django tests:
```bash
python manage.py test
```

## 🔧 Admin Interface

### Access Admin Panel
- **URL**: `http://localhost:8000/admin/`
- **Default Credentials**:
  - Username: `admin`
  - Password: `admin123`

### Admin Features
- View all OTP records
- Filter by verification status and creation date
- Search by email address
- Read-only creation timestamp
- Disabled manual OTP creation for security

## 🛠️ Development

### Code Structure

**Models (`vendor/models.py`):**
- EmailOTP model with OTP generation and validation logic

**Serializers (`vendor/serializers.py`):**
- Input validation for all API endpoints
- Custom validation methods for business logic

**Views (`vendor/views.py`):**
- APIView-based endpoints
- Comprehensive error handling
- Token generation and user management

**URLs (`vendor/urls.py`):**
- RESTful URL patterns
- Namespaced routing

### Configuration

**Settings (`vendor_project/settings.py`):**
```python
# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Adding New Features

1. **Create new model** in `vendor/models.py`
2. **Add serializer** in `vendor/serializers.py`
3. **Create view** in `vendor/views.py`
4. **Add URL pattern** in `vendor/urls.py`
5. **Run migrations** if needed

## 🚀 Deployment

### Production Considerations

1. **Database**: Use PostgreSQL or MySQL instead of SQLite
2. **Email Backend**: Configure SMTP settings for real email delivery
3. **Security**: Update SECRET_KEY and disable DEBUG
4. **Static Files**: Configure static file serving
5. **HTTPS**: Enable SSL/TLS for production

### Environment Variables

Create a `.env` file for production:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000
CMD ["gunicorn", "vendor_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for complex functions
- Write tests for new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) page
2. Create a new issue with detailed description
3. Include error messages and steps to reproduce

## 🔄 Version History

- **v1.0.0** - Initial release with OTP authentication and user management
  - EmailOTP model with expiry logic
  - Three main API endpoints
  - Token authentication
  - Admin interface

---

**Made with ❤️ using Django REST Framework** 