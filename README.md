# 🔧 Servfix - Home Maintenance Services Platform

![Django](https://img.shields.io/badge/Django-5.0.1-green.svg)
![Python](https://img.shields.io/badge/Python-3.11.3-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A comprehensive home maintenance services platform that connects customers with service providers, built with Django REST Framework and supports real-time chat and notifications.

## 📝 Project Description

Servfix is a graduation project aimed at facilitating access to home maintenance services through a reliable digital platform. Customers can find suitable service providers, while service providers can showcase their work and communicate with customers.

## ✨ Key Features

### For Customers:
- 🔍 Search for service providers by type and location
- ⭐ Rating and review system
- 💬 Direct chat with service providers
- 📱 Real-time notifications
- ❤️ Favorite service providers list
- 📍 Location and city specification

### For Service Providers:
- 📋 Detailed profile with work portfolio
- 💼 Display available services
- 💰 Set fixed pricing
- 📊 Track ratings and statistics
- 🗂️ Manage customer requests

### Technical Features:
- 🔐 Secure authentication system using JWT
- 🌐 Complete RESTful API
- 💬 Real-time chat using WebSockets
- 📧 Advanced notification system
- 🖼️ Image upload and management
- 📱 CORS support for mobile applications

## 🏗️ Technical Architecture

### Technologies Used:
- **Backend**: Django 5.0.1 + Django REST Framework
- **Database**: MySQL / SQLite (for development)
- **Authentication**: JWT (Simple JWT)
- **Real-time**: Django Channels + WebSockets
- **File Upload**: Pillow for image processing
- **Deployment**: Vercel ready

### Application Structure:
```
servfix/
├── account/          # User management and profiles
├── service/          # Service management
├── chat/            # Chat system
├── notification/    # Notification system
├── notifi/         # Additional notifications
└── media/          # Media files
```

## 🚀 Installation and Setup Instructions

### Prerequisites:
- Python 3.11.3 or newer
- MySQL (optional - SQLite can be used for development)

### Installation Steps:

1. **Download Python 3.11.3:**
   ```
   https://www.python.org/downloads/release/python-3113/
   ```

2. **Clone the project:**
   ```bash
   git clone https://github.com/ahmedhessuin27/Servfix.git
   cd Servfix
   ```

3. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

4. **Activate virtual environment:**
   
   **Windows:**
   ```cmd
   call ./venv/Scripts/activate
   ```
   
   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

5. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Setup database:**
   ```bash
   cd servfix
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```
   
   **Or use default admin account:**
   - Username: `admin`
   - Email: `admingamed@gmail.com`
   - Password: `admingamed30203020`

8. **Run the server:**
   ```bash
   python manage.py runserver
   ```

Now you can access the application at: `http://127.0.0.1:8000`

## 🔧 Database Configuration

### MySQL (for production):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'servv',
        'USER': 'root',
        'PASSWORD': '',
        'PORT': '3306',
        'HOST': 'localhost',
    }
}
```

### SQLite (for development):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 📱 API Endpoints

### Authentication:
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/refresh/` - Token refresh

### Services:
- `GET /api/services/` - List all services
- `GET /api/services/{id}/` - Get specific service

### Service Providers:
- `GET /api/providers/` - List service providers
- `GET /api/providers/{id}/` - Get provider profile
- `POST /api/providers/{id}/review/` - Add review

### Chat:
- `WebSocket /ws/chat/{room_name}/` - Real-time chat

## 🌐 Deployment on Vercel

The project is pre-configured for Vercel deployment:

1. Push code to GitHub
2. Connect repository to Vercel
3. Automatic deployment using `vercel.json` configuration

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the project
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support and Contact

- **Email**: servfix2023@gmail.com
- **GitHub**: [ahmedhessuin27](https://github.com/ahmedhessuin27)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Achievements

- ✅ Complete graduation project
- ✅ Secure authentication system
- ✅ Real-time chat
- ✅ Rating system
- ✅ Image upload and management
- ✅ Advanced notifications
- ✅ Production ready

---

**Note**: This is an educational project for development and learning purposes. Please review security settings before using in production environment.