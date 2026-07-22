# AI Learning Roadmap Tracker

A full-stack web application to help learners plan, organize, and track their AI/ML learning journey — create roadmaps, break them into topics, tag them with categories, and monitor progress over time.

## Features

- User Authentication — Register & login with JWT-based secure sessions
- Roadmaps — Create, update, and delete learning roadmaps with deadlines
- Categories — Organize roadmaps into custom categories (e.g. Backend, ML, Design)
- Topics — Break each roadmap into individual topics with status, target dates, and notes
- Progress Tracking — Automatic progress history logging whenever a topic's status changes
- Overall Progress % — Real-time calculation of roadmap completion

## Tech Stack

**Backend**
- FastAPI — REST API framework
- PostgreSQL — relational database
- SQLAlchemy — ORM
- Pydantic — request/response validation
- JWT (python-jose) + Passlib (bcrypt) — authentication & password hashing

**Frontend**
- Streamlit — interactive multi-page web UI
- Requests — API communication

## Project Structure

```
ai_learning_roadmap_tracker/
├── backend/
│   ├── main.py                # FastAPI app entry point
│   ├── config.py               # Environment settings
│   ├── database.py             # DB engine & session setup
│   ├── security.py             # Password hashing + JWT logic
│   ├── dependencies.py         # Shared dependencies (get_current_user)
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   ├── roadmap.py
│   │   ├── topic.py
│   │   ├── category.py
│   │   └── progress_history.py
│   ├── schemas/                 # Pydantic schemas
│   │   ├── user.py
│   │   ├── roadmap.py
│   │   ├── topic.py
│   │   ├── category.py
│   │   └── progress_history.py
│   ├── services/                # Business logic layer
│   │   ├── auth_services.py
│   │   ├── roadmap_services.py
│   │   ├── topic_services.py
│   │   ├── category_service.py
│   │   └── progress_history_services.py
│   └── routers/                  # API endpoints
│       ├── auth.py
│       ├── roadmap.py
│       ├── topic.py
│       ├── category.py
│       └── progress_history.py
│
├── frontend/
│   ├── app.py                    # Login / Register page
│   ├── pages/
│   │   ├── 1_Roadmaps.py
│   │   ├── 2_Topics.py
│   │   ├── 3_Progress.py
│   │   └── 4_Categories.py
│   └── utils/
│       └── api.py                 # Backend API helper functions
│
├── requirements.txt
└── .gitignore
```

## Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd ai_learning_roadmap_tracker
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL
Create a database:
```sql
CREATE DATABASE ai_roadmap_tracker;
```

### 5. Configure environment variables
Create a `.env` file in the root folder:
```
DATABASE_URL=postgresql://postgres:<your_password>@localhost:5432/ai_roadmap_tracker
SECRET_KEY=<your_generated_secret_key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 6. Run the backend
```bash
uvicorn backend.main:app --reload
```
API docs available at: `http://127.0.0.1:8000/docs`

### 7. Run the frontend
In a new terminal:
```bash
cd frontend
streamlit run app.py
```

## API Overview

| Resource | Endpoints |
|---|---|
| Auth | `POST /auth/register`, `POST /auth/login` |
| Roadmaps | `GET /roadmaps/`, `POST /roadmaps/`, `GET /roadmaps/{id}`, `PUT /roadmaps/{id}`, `DELETE /roadmaps/{id}` |
| Topics | `GET /topics/roadmap/{roadmap_id}`, `POST /topics/{roadmap_id}`, `GET /topics/{id}`, `PUT /topics/{id}`, `DELETE /topics/{id}` |
| Categories | `GET /categories/`, `POST /categories/`, `PUT /categories/{id}`, `DELETE /categories/{id}` |
| Progress History | `GET /progress-history/{roadmap_id}/{topic_id}` |

All endpoints except `auth/register` and `auth/login` require a Bearer token in the `Authorization` header.

## Author

Built by Rubab as part of an AI/ML engineering learning project — an internship sprint project combining FastAPI, PostgreSQL, and Streamlit.
