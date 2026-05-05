# Income Tax Calculator

A full-stack application to calculate income tax based on Indian tax regimes.
Built with FastAPI (backend), Streamlit (UI), and Docker for containerized deployment.

---

## Features

* Calculate tax for **old and new regimes**
* Apply **standard deduction and rebates**
* Store and retrieve **calculation history**
* Interactive **Streamlit UI**
* Fully tested backend with clean architecture
* Dockerized setup for easy deployment

---

## Tech Stack

* **Backend**: FastAPI, SQLAlchemy, Pydantic
* **Frontend**: Streamlit
* **Database**: SQLite
* **Testing**: Pytest
* **Containerization**: Docker, Docker Compose

---

## Project Structure

```
project/
├── app/                # Backend (API, services, models)
├── ui/                 # Streamlit UI
├── Dockerfile          # Backend container
├── Dockerfile.ui       # UI container
├── docker-compose.yml
├── requirements.txt
├── requirements-ui.txt
```

---

## Running Locally (Without Docker)

### 1. Start Backend

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API Docs: http://localhost:8000/docs

---

### 2. Start UI

```bash
pip install -r requirements-ui.txt
streamlit run ui/app.py
```

UI: http://localhost:8501

---

## Running with Docker

```bash
docker-compose up --build
```

* API: http://localhost:8000/docs
* UI: http://localhost:8501

---

## API Endpoints

* `POST /calculate-tax` → Calculate tax
* `GET /history` → Fetch previous records

---

## Example Request

```json
{
  "income": 1000000,
  "hra": 200000,
  "regime": "old"
}
```

---

## Testing

```bash
pytest
```

---

## Design Highlights

* Clean separation: **API → Service → Repository**
* Centralized **exception handling**
* Input validation using **Pydantic**
* Minimal and maintainable dependency management

---

## Future Improvements

* Async database support
* PostgreSQL integration
* Authentication & user-specific history
* Deployment (Cloud / CI-CD)

