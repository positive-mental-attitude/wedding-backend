# Wedding Backend

A Flask-based backend API for wedding RSVP management, providing endpoints for both wedding and afterparty RSVPs.

## Features

- Wedding RSVP API with Yes/No/Maybe responses
- Afterparty RSVP API
- PostgreSQL database integration
- CORS support for frontend integration
- Health check endpoint
- Database initialization scripts

## Tech Stack

- **Framework**: Flask
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: None (public API)
- **Deployment**: EC2

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wedding-backend.git
cd wedding-backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your database credentials
```

5. Initialize the database:
```bash
python init_db.py
python init_wedding_db.py
```

6. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Environment Variables

Create a `.env` file with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/afterparty_db
WEDDING_DATABASE_URL=postgresql://username:password@localhost:5432/wedding_rsvp_db
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
```

## API Endpoints

### Wedding RSVP
- `POST /api/wedding-rsvp` - Submit wedding RSVP
- `GET /api/wedding-rsvp` - Get all wedding RSVPs
- `GET /api/wedding-rsvp?response_type=yes` - Get RSVPs by type

### Afterparty RSVP
- `POST /api/rsvp` - Submit afterparty RSVP
- `GET /api/rsvp` - Get all afterparty RSVPs

### Health Check
- `GET /health` - Health check endpoint

## Database Schema

### Wedding RSVP Table
```sql
CREATE TABLE wedding_rsvp (
    id SERIAL PRIMARY KEY,
    response_type VARCHAR(10) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    telegram_username VARCHAR(50),
    phone_number VARCHAR(20),
    dietary_restrictions TEXT,
    message TEXT,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Afterparty RSVP Table
```sql
CREATE TABLE afterparty (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    telegram VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Deployment

### EC2 Deployment

1. Set up an EC2 instance with Ubuntu/Debian
2. Install Python, PostgreSQL, and nginx
3. Clone the repository
4. Set up environment variables
5. Use systemd or supervisor to run the Flask app
6. Configure nginx as reverse proxy

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

## Development

### Running Tests
```bash
python test_api.py
```

### Database Management
```bash
# Initialize databases
python init_db.py
python init_wedding_db.py

# Reset databases (if needed)
python init_db.py --reset
python init_wedding_db.py --reset
```

## Project Structure

```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── init_db.py            # Afterparty database initialization
├── init_wedding_db.py    # Wedding database initialization
├── setup.sh              # Setup script for EC2
├── test_api.py           # API tests
└── env.example           # Environment variables template
```

## Security Considerations

- All database operations use SQLAlchemy ORM (SQL injection protected)
- Input validation on all endpoints
- CORS configured for frontend integration
- No authentication (public API for wedding RSVPs)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is private and for personal use. 