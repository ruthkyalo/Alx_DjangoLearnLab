
# Social Media API

This project is a basic Social Media API built with **Django** and **Django REST Framework (DRF)**. It provides user registration, login, and profile management using token-based authentication.

---

## **Setup Instructions**

1. **Clone the repository:**
```bash
git clone https://github.com/<your-username>/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api
````

2. **Create and activate a virtual environment (optional but recommended):**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install required packages:**

```bash
pip install -r requirements.txt
```

 install manually: `pip install django djangorestframework djangorestframework-authtoken`)*

4. **Apply migrations:**

```bash
python manage.py makemigrations
python manage.py migrate
```



5. **Start the development server:**

```bash
python manage.py runserver
```

---

## **User Registration and Login**

### **1. Register a User**

* Endpoint: `POST /api/accounts/register/`
* Request Body Example:

```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123",
    "bio": "Hello, I'm John!",
    "profile_picture": null
}
```



### **2. Login**

* Endpoint: `POST /api/accounts/login/`
* Request Body Example:

```json
{
    "username": "john_doe",
    "password": "password123"
}
```

* Response returns the **token**.

> Use this token in the `Authorization` header for authenticated requests:
> `Authorization: Token <your-token>`

---

## **User Model Overview**

The custom user model extends Django’s `AbstractUser` and includes:

* **bio**: A text field where users can describe themselves.
* **profile\_picture**: An image field to store the user’s profile picture.
* **followers**: A ManyToMany relationship to track users following each other (`symmetrical=False`).

---

## **Project Structure**

```
social_media_api/
│
├── accounts/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── social_media_api/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── README.md
```

---

