# Distance Calculator API

A FastAPI-based backend service for calculating distances between addresses with intelligent address correction. Live demo available at [https://bain.yizhou.me](https://bain.yizhou.me).

## Features

### 1. Distance Calculation
- Calculate distances between any two addresses worldwide
- Support for both miles and kilometers
- Uses the Haversine formula for accurate distance calculation
- Real-time geocoding using OpenStreetMap's Nominatim service

### 2. Intelligent Address Processing
- Address correction and validation using OpenAI's GPT-3.5
- Handles misspellings and incomplete addresses
- Provides feedback on address corrections
- Fallback mechanism for OpenAI service unavailability

### 3. Query History
- Store and retrieve historical distance calculations
- Pagination support for large history sets
- Protected by reCAPTCHA v2
- Includes timestamps and corrected addresses

### 4. Security Features
- reCAPTCHA protection on sensitive endpoints
- Rate limiting
- Comprehensive error handling
- Input validation and sanitization

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy with async support
- **Migrations**: Alembic
- **External Services**:
  - OpenAI GPT-3.5
  - Google reCAPTCHA v2
  - OpenStreetMap Nominatim
- **Containerization**: Docker & Docker Compose

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 16
- Docker & Docker Compose (for containerized deployment)

### Environment Variables

Create a `.env` file in the root directory with the following configurations:

```env
# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=root
POSTGRES_PASSWORD=your_password
POSTGRES_DB=distance_calculator

# Nominatim
NOMINATIM_BASE_URL=https://nominatim.openstreetmap.org
NOMINATIM_USER_AGENT=DistanceCalculator/1.0

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME="Distance Calculator API"

# External Services
RECAPTCHA_SECRET_KEY=your_recaptcha_secret_key
OPENAI_API_KEY=your_openai_api_key
```

### Local Development Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run database migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Docker Deployment

1. Build and start the containers:
   ```bash
   docker-compose up -d --build
   ```

2. The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

- `POST /api/v1/distance`: Calculate distance between two addresses
- `GET /api/v1/history`: Retrieve calculation history
- `GET /api/v1/health`: API health check

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

For test coverage report:
```bash
pytest tests/ --cov=app -v
```

## Deployment

The service is designed to be easily deployable to any cloud platform that supports Docker containers. The live demo is currently hosted at [https://bain.yizhou.me](https://bain.yizhou.me).

### Production Deployment Considerations

1. Use proper SSL/TLS certificates
2. Configure appropriate rate limiting
3. Set up monitoring and logging
4. Use production-grade PostgreSQL setup
5. Configure proper backup strategies

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Joey Li

## Live Demo

Visit [https://bain.yizhou.me](https://bain.yizhou.me) to try out the live version of the application. 