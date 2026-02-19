# LEARN-DRF 🎯  
*A complete Django REST Framework learning project*

This repository represents my **end-to-end learning journey with Django REST Framework (DRF)**.  
I built this project step by step while learning backend development — from Django basics to advanced DRF concepts like **permissions, pagination, throttling, and authentication**.

This project is focused on **learning by building**, not just theory.

---

## 📖 Project Overview

The project is built around a simple **Watchlist / Review system**, where users can:
- Register and authenticate
- Access APIs securely
- Perform CRUD operations
- Experience real-world backend concepts like rate limiting and permissions

During development, I continuously tested APIs using **Postman** and improved the structure as I learned new DRF concepts.

---

## 🧠 What I Learned & Implemented

Through this project, I learned and implemented:

- Django project & app structure
- Django ORM (no raw SQL)
- Django REST Framework architecture
- Serializers and validation
- Function-based views → Class-based generic views
- Token-based authentication
- Custom permissions
- Pagination for large datasets
- API throttling (rate limiting)
- Modular API structure (`api/` folders)
- Debugging and testing APIs using Postman
- Writing clean and reusable code
- Git & GitHub workflow

---

## 🚀 Key Features

### 👤 User Management (`user_app`)
- User registration
- User login
- Token generation
- Authentication-based access control

### 📺 Watchlist APIs (`watchlist_app`)
- CRUD operations on watchlist items
- Serializer-based clean API responses
- Custom permissions
- Pagination support
- Throttling to limit API requests
- Well-structured API routing

---

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Language:** Python 3
- **Database:** SQLite (development)
- **Authentication:** Token Authentication
- **Tools:** Postman, Git, GitHub

---
📂 Project Structure
```text
LEARN-DRF/
├── user_app/
│   ├── api/
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   ├── models.py
│   ├── tests.py
│
├── watchlist_app/
│   ├── api/
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── permissions.py
│   │   ├── pagination.py
│   │   ├── throttling.py
│   ├── models.py
│   ├── tests.py
│
├── watchmate/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│
├── db.sqlite3
├── manage.py
├── requirements.txt
├── README.md
```

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/LEARN-DRF.git
cd LEARN-DRF
```

### 2️⃣ Create and activate virtual environment
```bash
python -m venv menv
source menv/bin/activate   # Linux/Mac
menv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run migrations
```bash
python manage.py migrate
```

### 5️⃣ Create superuser (optional)
```bash
python manage.py createsuperuser
```

### 6️⃣ Start the development server
```bash
python manage.py runserver
```

---

## 🔐 Authentication

This project uses **Token Authentication**.

After login, include the token in request headers:

```http
Authorization: Token your_token_here
```

---

## 🧪 API Testing

All APIs were tested using **Postman**:

- Authentication flow verified
- Permission checks tested
- Throttling limits validated
- Pagination responses checked
- Error handling understood

---

## 🎯 Why This Project Matters

This project shows:

- Consistency in learning
- Practical backend understanding
- Ability to read documentation and implement features
- Real-world DRF concepts beyond basics

It is **not a production app** — it is a **strong foundation project**.

---

## 🔮 Future Improvements

- JWT authentication
- API documentation (Swagger)
- Deployment to cloud (Render / Railway / AWS)
- Frontend integration
- Better test coverage
