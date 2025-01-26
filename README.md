 # CT Restart Python Backend

## Overview
Python backend service for CT Restart platform, handling trial analysis and data processing.

## Tech Stack
- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pytest for testing
- Pandas for data processing

## Project Structure
```
app/
├── models/         # Database models
├── routes/         # API endpoints
├── services/       # Business logic
├── schemas/        # Pydantic models
├── utils/          # Utility functions
└── tests/          # Test files
```

## Setup and Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip and virtualenv

### Installation
1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/ct_restart
API_KEY=your_api_key
PORT=8000
```

### Development
Run the development server:
```bash
uvicorn app.main:app --reload --port 8000
```

### Testing
Run tests:
```bash
pytest
```

## API Documentation
FastAPI automatically generates interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Trial Analysis Endpoints
- GET `/api/trials`: List trials
- POST `/api/trials/analyze`: Analyze trial data
- GET `/api/trials/{id}`: Get trial details
- PUT `/api/trials/{id}`: Update trial
- DELETE `/api/trials/{id}`: Delete trial

## Available Scripts
- `uvicorn app.main:app`: Start production server
- `uvicorn app.main:app --reload`: Start development server
- `pytest`: Run tests
- `black .`: Format code
- `isort .`: Sort imports
- `flake8`: Run linter

## Docker Support
Build the container:
```bash
docker build -t ct-restart-python .
```

Run the container:
```bash
docker run -p 8000:8000 ct-restart-python
```

## Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `API_KEY`: API key for external services
- `PORT`: Server port (default: 8000)
- `ENV`: Environment (development/production)

## Data Processing
The service includes modules for:
- Trial data analysis
- Document processing
- Statistical analysis
- Data visualization
```