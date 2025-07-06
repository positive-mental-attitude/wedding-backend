# Quick Start Guide - Afterparty RSVP Backend

This guide will get you up and running with the Flask backend in minutes.

## Prerequisites

- Python 3.8+
- PostgreSQL (running locally or remotely)
- Basic knowledge of command line

## Quick Setup (5 minutes)

### 1. Run the Setup Script

```bash
cd project/backend
./setup.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Create a `.env` file from template

### 2. Configure Database

Edit the `.env` file with your PostgreSQL credentials:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/afterparty_db
WEDDING_DATABASE_URL=postgresql://username:password@localhost:5432/wedding_rsvp_db
```

### 3. Initialize Database

```bash
python init_db.py
python init_wedding_db.py
```

### 4. Start the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

## Test the API

### Quick Test with curl

```bash
# Health check
curl http://localhost:5000/health

# Submit Afterparty RSVP
curl -X POST http://localhost:5000/api/rsvp \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "telegram": "@janedoe",
    "phone_number": "+6512345678"
  }'

# Submit Wedding RSVP (Yes)
curl -X POST http://localhost:5000/api/wedding-rsvp \
  -H "Content-Type: application/json" \
  -d '{
    "response_type": "yes",
    "full_name": "Jane Doe",
    "telegram_username": "@janedoe",
    "phone_number": "+6512345678",
    "dietary_restrictions": "Vegetarian, no nuts"
  }'

# Get all Afterparty RSVPs
curl http://localhost:5000/api/rsvp

# Get all Wedding RSVPs
curl http://localhost:5000/api/wedding-rsvp
```

### Run Full Test Suite

```bash
python test_api.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/rsvp` | Submit Afterparty RSVP |
| GET | `/api/rsvp` | Get all Afterparty RSVPs |
| POST | `/api/wedding-rsvp` | Submit Wedding RSVP |
| GET | `/api/wedding-rsvp` | Get all Wedding RSVPs |
| GET | `/health` | Health check |

## Example Usage

### Submit Afterparty RSVP
```bash
curl -X POST http://localhost:5000/api/rsvp \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Smith",
    "telegram": "@johnsmith",
    "phone_number": "+6598765432"
  }'
```

**Response:**
```json
{
  "message": "RSVP received",
  "rsvp_id": 1
}
```

### Submit Wedding RSVP (Yes)
```bash
curl -X POST http://localhost:5000/api/wedding-rsvp \
  -H "Content-Type: application/json" \
  -d '{
    "response_type": "yes",
    "full_name": "Jane Doe",
    "telegram_username": "@janedoe",
    "phone_number": "+6512345678",
    "dietary_restrictions": "Vegetarian, no nuts"
  }'
```

### Submit Wedding RSVP (No)
```bash
curl -X POST http://localhost:5000/api/wedding-rsvp \
  -H "Content-Type: application/json" \
  -d '{
    "response_type": "no",
    "full_name": "John Doe",
    "message": "Sorry, I can't make it"
  }'
```

### Submit Wedding RSVP (Maybe)
```bash
curl -X POST http://localhost:5000/api/wedding-rsvp \
  -H "Content-Type: application/json" \
  -d '{
    "response_type": "maybe",
    "full_name": "Bob Smith",
    "note": "I'll confirm closer to the date"
  }'
```

**Response:**
```json
{
  "message": "Wedding RSVP (yes) received",
  "rsvp_id": 1
}
```

### Get All Afterparty RSVPs
```bash
curl http://localhost:5000/api/rsvp
```

**Response:**
```json
{
  "rsvps": [
    {
      "id": 1,
      "name": "John Smith",
      "telegram": "@johnsmith",
      "phone_number": "+6598765432",
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "count": 1
}
```

### Get All Wedding RSVPs
```bash
curl http://localhost:5000/api/wedding-rsvp
```

**Response:**
```json
{
  "rsvps": [
    {
      "id": 1,
      "response_type": "yes",
      "full_name": "Jane Doe",
      "telegram_username": "@janedoe",
      "phone_number": "+6512345678",
      "dietary_restrictions": "Vegetarian, no nuts",
      "message": null,
      "note": null,
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "rsvps_by_type": {
    "yes": [...],
    "no": [...],
    "maybe": [...]
  },
  "count": 1,
  "count_by_type": {
    "yes": 1,
    "no": 0,
    "maybe": 0
  }
}
```

## Troubleshooting

### Common Issues

1. **"Connection refused" error**
   - Make sure PostgreSQL is running
   - Check your database credentials in `.env`

2. **"Module not found" error**
   - Activate virtual environment: `source venv/bin/activate`
   - Reinstall dependencies: `pip install -r requirements.txt`

3. **"Permission denied" error**
   - Make sure PostgreSQL user has proper permissions
   - Check database exists: `createdb afterparty_db`

### Debug Mode

Enable debug mode by setting `FLASK_DEBUG=True` in your `.env` file.

## Next Steps

- Integrate with your frontend application
- Set up production deployment
- Add authentication if needed
- Configure logging and monitoring

For detailed documentation, see `README.md`. 