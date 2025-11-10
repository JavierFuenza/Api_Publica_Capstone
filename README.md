# Environmental Metrics API

A FastAPI-based REST API for accessing environmental quality data, including air and water quality measurements. This API uses Firebase authentication and connects to a PostgreSQL database via Neon.

## Features

- 🔐 **Firebase Authentication**: Secure endpoints with Firebase ID token verification
- 🌍 **Environmental Data**: Access air and water quality metrics
- 📊 **Flexible Filtering**: Query data by date range, location, and other parameters
- 🐳 **Docker Support**: Easy deployment with Docker and docker-compose
- 📚 **Auto-generated Documentation**: Interactive API docs at `/docs`
- 🔄 **CORS Enabled**: Ready for integration with frontend applications

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (via Neon)
- **Authentication**: Firebase Admin SDK
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Server**: Uvicorn

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional, for containerized deployment)
- PostgreSQL database (Neon account recommended)
- Firebase project with service account credentials

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Api_Publica_Capstone
```

### 2. Configure Environment Variables

Edit the `.env` file with your actual credentials:

```bash
# Database - Update with your Neon connection string
DATABASE_URL=postgresql://user:password@your-neon-host.neon.tech:5432/your-database?sslmode=require

# Firebase - Path to your credentials file
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# CORS - Add your frontend URLs
CORS_ORIGINS=http://localhost:3000,http://localhost:4321,https://yourdomain.com

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
ENVIRONMENT=development
```

### 3. Add Firebase Credentials

1. Go to Firebase Console → Project Settings → Service Accounts
2. Click "Generate New Private Key"
3. Save the JSON file as `firebase-credentials.json` in the project root

### 4. Update Database Models

The database models in `app/models/` are placeholders. Update them to match your actual database schema:

- `app/models/air_quality.py` - Air quality table structure
- `app/models/water_quality.py` - Water quality table structure

### 5. Installation

#### Option A: Docker (Recommended)

```bash
# Build and run with docker-compose
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

#### Option B: Local Development

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
```

## Usage

### Access the API

Once running, the API is available at:

- **API Docs (Swagger UI)**: http://srv1105893.hstgr.cloud:8000/docs
- **Alternative Docs (ReDoc)**: http://srv1105893.hstgr.cloud:8000/redoc
- **Health Check**: http://srv1105893.hstgr.cloud:8000/health
- **API Info**: http://srv1105893.hstgr.cloud:8000/api/v1

### Authentication

All endpoints (except `/health`) require Firebase authentication. Include the Firebase ID token in the Authorization header:

```bash
curl -H "Authorization: Bearer <your-firebase-token>" \
     http://srv1105893.hstgr.cloud:8000/api/v1/air-quality
```

See [FRONTEND_INTEGRATION.md](./FRONTEND_INTEGRATION.md) for detailed frontend integration instructions.

### Available Endpoints

#### Air Quality

- `GET /api/v1/air-quality` - List all air quality measurements
  - Query params: `date_from`, `date_to`, `location`, `limit`, `offset`
- `GET /api/v1/air-quality/{id}` - Get specific measurement by ID

#### Water Quality

- `GET /api/v1/water-quality` - List all water quality measurements
  - Query params: `date_from`, `date_to`, `location`, `source`, `limit`, `offset`
- `GET /api/v1/water-quality/{id}` - Get specific measurement by ID

### Example Request

```bash
# Get air quality measurements from the last week
curl -H "Authorization: Bearer eyJhbGc..." \
     "http://srv1105893.hstgr.cloud:8000/api/v1/air-quality?date_from=2024-01-01&limit=10"
```

## Project Structure

```
Api_Publica_Capstone/
├── app/
│   ├── api/
│   │   └── v1/              # API version 1 endpoints
│   │       ├── air_quality.py
│   │       └── water_quality.py
│   ├── core/                # Core functionality
│   │   ├── config.py        # Configuration management
│   │   ├── database.py      # Database connection
│   │   ├── security.py      # Firebase authentication
│   │   ├── exceptions.py    # Error handlers
│   │   └── middleware.py    # Custom middleware
│   ├── models/              # SQLAlchemy models
│   │   ├── air_quality.py
│   │   └── water_quality.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── air_quality.py
│   │   └── water_quality.py
│   ├── services/            # Business logic (future)
│   └── main.py              # Application entry point
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
└── README.md               # This file
```

## Development

### Running Tests

```bash
# TODO: Add test framework and commands
```

### Code Style

The project follows Python best practices. Consider using:

```bash
# Format code
black app/

# Lint code
ruff check app/

# Type checking
mypy app/
```

### Database Migrations

To manage database schema changes:

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head
```

## Troubleshooting

### Firebase Credentials Not Found

**Error**: `WARNING: Firebase credentials file not found`

**Solution**: Ensure `firebase-credentials.json` exists in the project root and the path in `.env` is correct.

### Database Connection Failed

**Error**: Database connection errors

**Solutions**:
- Verify DATABASE_URL in `.env` is correct
- Ensure your Neon database is accessible
- Check if SSL mode is required (`?sslmode=require`)
- Verify network connectivity

### CORS Errors

**Error**: CORS policy blocking requests from frontend

**Solution**: Add your frontend URL to `CORS_ORIGINS` in `.env`:
```
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Set `ENVIRONMENT=production`
- [ ] Use strong database credentials
- [ ] Secure Firebase credentials (use secrets management)
- [ ] Configure proper CORS origins
- [ ] Set up SSL/TLS (HTTPS)
- [ ] Enable logging and monitoring
- [ ] Set up database backups
- [ ] Configure rate limiting (if needed)

### Deploy with Docker

```bash
# Build production image
docker build -t environmental-metrics-api .

# Run container
docker run -d \
  -p 8000:8000 \
  -v /path/to/.env:/app/.env \
  -v /path/to/firebase-credentials.json:/app/firebase-credentials.json \
  environmental-metrics-api
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For questions or issues:
- Open an issue on GitHub
- Contact the development team
- Check API documentation at `/docs`
