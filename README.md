# Travel Booking Backend – Key Concepts Overview

This document provides a clear explanation of the main backend concepts used in the development of a travel booking platform. It covers Django models, database relationships, constraints, serializers, seeding, and other core components that form the foundation of the project.

---

## 🌱 Key Backend Concepts

### 1. Django Models
Django models provide the blueprint for database tables.  
Each Python class represents a table, and each class attribute represents a column in that table.

---

### 2. Relationships Between Models
Real applications involve connections between data.

Django supports:
- **One-to-Many**: e.g., one user can create many bookings.
- **Many-to-One**: each booking is linked to one property.
- **Many-to-Many**: e.g., users can like many properties, and properties can be liked by many users.

These relationships keep data organized and meaningful.

---

### 3. Database Constraints
Constraints are rules that ensure the data stored in the database is valid.

Examples:
- Email must be unique for each user.
- Booking end date must be after the start date.
- Pricing values must be positive.

These rules protect the database from invalid or conflicting data.

---

### 4. Serializers (Django REST Framework)
APIs communicate using JSON, while Django uses Python objects. Serializers convert data between the two formats.

Serializers allow:
- Converting model instances into JSON.
- Validating and converting JSON input into Python objects.

This is essential when building REST APIs for mobile, web, or third-party clients.

---

### 5. Django Management Commands
Django allows extending its CLI by creating custom management commands.  
These commands automate tasks such as:

- Seeding the database
- Cleaning old records
- Importing/exporting data

Example:
```sh
python manage.py seed_data
