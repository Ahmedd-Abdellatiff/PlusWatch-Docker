# PulseWatch

### Website Monitoring System

PulseWatch is a containerized website monitoring system built with Python and FastAPI.

The application allows users to register websites and monitor their availability. It checks whether each website is up or down, measures response time, and stores monitoring results for later reference.

## Architecture

The project is built using three separate services managed through Docker Compose:

- **API:** Handles website registration, retrieval, deletion, and exposes REST API endpoints using FastAPI.
- **Worker:** Handles website monitoring and executes health checks against registered websites.
- **Database:** Stores website information and monitoring results.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Docker Compose

## Features

- Add and manage monitored websites.
- Retrieve all registered websites.
- Retrieve website details by ID.
- Delete registered websites.
- Check website availability (UP/DOWN).
- Measure HTTP response time.
- Track HTTP status codes.
- Store monitoring results in the database.
- API health check endpoint.

## Project Structure

```text
PulseWatch/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── health.py
│   └── monitor.py
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md

## Accessing the Application

After starting the application with Docker Compose, you can access the following endpoints:

| Endpoint | Description |
|---|---|
| `http://localhost:8000/docs` | Interactive API documentation using Swagger UI. |
| `http://localhost:8000/health` | Check application and database health. |
| `http://localhost:8000/websites/` | Retrieve all registered websites. |

### Managing Websites

Using the Swagger documentation, you can:

- Register a new website for monitoring.
- View all registered websites.
- Retrieve website details by ID.
- Delete a website.

### Monitoring

The Worker service is responsible for checking registered websites, tracking their availability (UP/DOWN), and measuring response time.

Monitoring results are stored in the database.

---

## Author

**Ahmed AbdelLatif**