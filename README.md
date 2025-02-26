# Teaching-Internship Portfolio Submission System

This project is a **Teaching-Internship Portfolio Submission System** designed for **Akenten Appiah-Menka University of Skills Training and Entrepreneurial Development (AAMUSTED)**. The system enables interns to submit monthly reports digitally, reducing the need for in-person supervision and physical document printing.

## Features
- User authentication (JWT-based)
- Role-based access (Interns, Supervisors, Admins)
- Monthly internship portfolio submissions (documents, images, videos)
- Notification system
- Profile management with change password feature
- Internship progress tracking

---

## Tech Stack

### Backend (Django + DRF)
- **Django** (Python Web Framework)
- **Django REST Framework** (API Development)
- **SimpleJWT** (Authentication)
- **Django Allauth** (User Management)
- **PostgreSQL** (Database)


### Frontend (Vue 3 + Vite)
- **Vue 3** (Modern JavaScript Framework)
- **Vue Router** (Navigation)
- **Pinia** (State Management)
- **Tailwind CSS** (Styling)
- **Vue Toastification** (Notifications)
- **Axios** (API Calls)

---

# Installation & Setup

## Prerequisites
Ensure you have the following installed:
- **Python** (>=3.10)
- **Node.js** (>=16.x)
- **PostgreSQL**


## Backend Setup

### 1. Clone the repository:
```sh
  git clone https://github.com/your-repo.git
  cd backend
```

### 2. Create and activate a virtual environment:
```sh
  python -m venv venv
  source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies:
```sh
  pip install -r requirements.txt
```

### 4. Set up environment variables:
Create a `.env` file in the `backend/` directory with:
```sh
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=your_db_name
DB_USER="your_db_user"
DB_PASS="your_db_password"
DB_HOST="your_db_host"
DB_PORT="5432"

```

### 5. Run migrations:
```sh
  python manage.py migrate
```

### 6. Create a superuser:
```sh
  python manage.py createsuperuser
```

### 7. Start the development server:
```sh
  python manage.py runserver
```

---

## Frontend Setup

### 1. Navigate to the frontend directory:
```sh
  cd frontend
```

### 2. Install dependencies:
```sh
  npm install
```

### 3. Set up environment variables:
Create a `.env` file in the `frontend/` directory with:
```sh
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

### 4. Start the development server:
```sh
  npm run dev
```

---

## Django Admin
Login to Django Admin: `http://127.0.0.1:8000/admin/`

---
