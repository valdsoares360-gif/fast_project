🚀 Fast Project API
<p align="center"> <img src="https://img.shields.io/badge/Python-3.12-blue"> <img src="https://img.shields.io/badge/FastAPI-Production-green"> <img src="https://img.shields.io/badge/PostgreSQL-Database-blue"> <img src="https://img.shields.io/badge/Docker-Containerized-blue"> <img src="https://img.shields.io/badge/CI/CD-Automated-success"> </p> <p align="center"> A production-ready REST API built with <b>FastAPI</b>, using async SQLAlchemy, JWT authentication and PostgreSQL. </p>
📌 Overview

This project demonstrates real backend engineering practices:

🔐 Authentication & Authorization (JWT)

⏳ Token expiration handling

📄 Pagination & Filtering

🗄 Database migrations

🧪 Automated testing

⚙️ CI/CD pipeline

🐳 Docker containerization

📚 Interactive API documentation

Designed to reflect real-world production standards.

🛠 Tech Stack
Layer	Technology
Framework	FastAPI
Database	PostgreSQL
ORM	SQLAlchemy (Async)
Migrations	Alembic
Authentication	JWT (OAuth2 Password Flow)
Testing	Pytest + Freezegun
CI/CD	GitHub Actions
Containerization	Docker & Docker Compose
🧱 Project Architecture
fast_project/
│
├── models.py
├── schemas.py
├── security.py
├── database.py
├── settings.py
│
├── routers/
│   ├── auth.py
│   ├── users.py
│   └── todos.py
│
alembic/
docker-compose.yml
Dockerfile
README.md
images/
Responsibility Separation

models.py → Database models

schemas.py → Data validation layer

security.py → JWT generation & validation

database.py → Async session management

routers/ → Domain-based route separation

settings.py → Environment configuration

🔐 Authentication Flow

User logs in via /auth/login

API returns a JWT access token

Token must be sent in header:

Authorization: Bearer <your_token>

Expired or invalid tokens are rejected

Refresh endpoint available at /auth/refresh_token

Secure and production-ready authentication flow.

📸 API Demonstration
🧾 Interactive Swagger Documentation
<p align="center"> <img src="./imagens/swagger.png" width="900"> </p>

✔️ Organized routes
✔️ Protected endpoints (🔒)
✔️ Request/response inspection
✔️ Built-in authentication testing

🔐 Successful Login (JWT Issued)
<p align="center"> <img src="./imagens/login.png" width="900"> </p>

✔️ OAuth2 Password Flow
✔️ Access token generated
✔️ Secure session started

✅ Creating a Todo (Protected Route)
<p align="center"> <img src="./imagens/create_todo.png" width="900"> </p>

Example response:

{
  "title": "hytest",
  "description": "hytest description",
  "state": "draft",
  "id": 2
}

✔️ Authenticated request
✔️ Data persisted in PostgreSQL
✔️ Status 200 OK

⛔ Token Expiration Handling
<p align="center"> <img src="./imagens/token_expired.png" width="900"> </p>

Example response:

{
  "detail": "could not validate credentials"
}

✔️ Status 401 Unauthorized
✔️ Proper security headers
✔️ Credential validation enforced

📝 Todo State System

Todos use an Enum-based state model:

draft

todo

doing

done

trash

Ensures controlled transitions and domain integrity.

📄 Pagination & Filtering

The API supports scalable data retrieval:

GET /users?limit=10&offset=0
GET /todos?limit=5&offset=0

Filtering example:

GET /todos?state=done

✔️ Optimized queries
✔️ Production-ready list endpoints
✔️ Flexible data access

🧪 Automated Testing

Run all tests:

pytest

Coverage includes:

Token generation

Invalid login handling

Token expiration validation

Refresh token validation

Protected route access control

Pagination validation

Filter validation

Test-driven reliability.

⚙️ CI/CD Pipeline

This project includes a GitHub Actions workflow.

Pipeline runs automatically on:

Push

Pull Request

Workflow steps:

✔️ Install dependencies
✔️ Run automated tests
✔️ Validate application build

Ensures continuous integration and code stability.

🐳 Running with Docker
1️⃣ Build and start containers
docker compose up --build
2️⃣ Apply migrations
docker compose exec fast_project alembic upgrade head

API available at:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs
⚙️ Environment Variables

Create a .env file:

DATABASE_URL=postgresql+psycopg://app_user:app_password@fastproject_database:5432/app_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
🚀 Production Readiness Highlights

✔️ Async database operations
✔️ Secure JWT authentication
✔️ Token expiration enforcement
✔️ Pagination & filtering
✔️ Database versioning (Alembic)
✔️ Automated tests
✔️ CI/CD integration
✔️ Dockerized environment

This project reflects real backend production patterns.

📈 Future Improvements

Role-Based Access Control (RBAC)

Advanced filtering system

Rate limiting

Centralized logging

Monitoring integration


👨‍💻 Author

Backend project built for professional portfolio development.

⭐ Final Statement

This API demonstrates:

Clean architecture

Secure authentication flow

Production-aware design

DevOps fundamentals

Scalable endpoint structure

you can see my api here https://fast-project-bcgx.onrender.com/docs
