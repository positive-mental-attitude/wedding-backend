# Wedding Backend (MongoDB Edition)

A Flask-based backend API for wedding RSVP management, providing endpoints for both wedding and afterparty RSVPs.

## Features

- Wedding RSVP API with Yes/No/Maybe responses
- Afterparty RSVP API
- MongoDB Atlas integration (via PyMongo)
- CORS support for frontend integration
- Health check endpoint
- Database initialization scripts

## Tech Stack

- **Framework**: Flask
- **Database**: MongoDB Atlas (PyMongo)
- **Authentication**: None (public API)
- **Deployment**: EC2, Docker

## Getting Started

### Prerequisites

- Python 3.9+
- MongoDB Atlas cluster (or local MongoDB)
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wedding-backend-mongo.git
cd wedding-backend-mongo
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
# Edit .env with your MongoDB Atlas URI
```

5. (Optional) Check MongoDB connection and collections:
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
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/wedding?retryWrites=true&w=majority
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

## Database Schema (MongoDB Documents)

### Wedding RSVP Document
```json
{
  "_id": ObjectId,
  "response_type": "yes" | "no" | "maybe",
  "full_name": "Jane Doe",
  "telegram_username": "@janedoe", // only for 'yes'
  "phone_number": "+6512345678", // only for 'yes'
  "dietary_restrictions": "Vegetarian, no nuts", // only for 'yes'
  "message": "Sorry, I can't make it", // only for 'no'
  "note": "I'll confirm closer to the date", // only for 'maybe'
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Afterparty RSVP Document
```json
{
  "_id": ObjectId,
  "name": "John Smith",
  "telegram": "@johnsmith",
  "phone_number": "+6598765432",
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Deployment

### EC2 Deployment

1. Set up an EC2 instance with Ubuntu/Debian
2. Install Python and nginx
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
# Check MongoDB connection and collections
python init_db.py
python init_wedding_db.py
```

## Project Structure

```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── init_db.py            # Afterparty collection check
├── init_wedding_db.py    # Wedding collection check
├── setup.sh              # Setup script for EC2
├── test_api.py           # API tests
└── env.example           # Environment variables template
```

## Security Considerations

- All database operations use PyMongo (no SQL injection risk)
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