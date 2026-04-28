# Real-Time Leaderboard System

A high-performance backend service for tracking global player rankings in real-time. Built with **FastAPI**, **PostgreSQL** for persistence, and **Redis** for sub-millisecond ranking updates.

## 🚀 Key Features
- **Stateless Auth:** Secure user registration and login using JWT (JSON Web Tokens).
- **Hybrid Storage:** PostgreSQL stores the permanent history; Redis Sorted Sets handle the real-time rankings.
- **Dynamic Leaderboard:** Global "Top 10" and personal "My Rank" endpoints.
- **Reporting:** SQL-based analytics for top players over custom time periods (e.g., last 7 days).
- **Modular Design:** Clean separation of concerns (Core, API, Services, Schemas, DB).

## 🛠 Tech Stack
- **Framework:** FastAPI (Python 3.12+)
- **Database:** PostgreSQL 15
- **Caching/Ranking:** Redis 7
- **Security:** Bcrypt (Hashing) & PyJWT

## 🚦 Getting Started

### 1. Start Infrastructure
```bash
docker-compose up -d
```

### 2. Initialize Database
```bash
python -m app.db.init_db
```

### 3. Run the Application
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`. Explore the interactive documentation at `http://localhost:8000/docs`.

## 📂 Project Structure
- `app/api`: Request handling and routing.
- `app/services`: Core business logic (Auth, Games, Leaderboard).
- `app/schemas`: Pydantic data validation models.
- `app/db`: Database connection pools and migrations.
- `app/core`: Central configuration and security utilities.

## 🧪 Testing & Data
- `python seed_data.py`: Populates the system with fake users and scores.
- `python -m app.db.warm_up`: Synchronizes the Redis leaderboard with historical data from PostgreSQL.
