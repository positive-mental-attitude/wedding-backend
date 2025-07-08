# Quick Start Guide - Afterparty RSVP Backend (MongoDB Edition)

This guide will get you up and running with the Flask backend using MongoDB Atlas in minutes.

## Prerequisites

- Python 3.8+
- MongoDB Atlas cluster (or local MongoDB)
- Basic knowledge of command line

## Quick Setup (5 minutes)

### 1. Run the Setup Script

```bash
cd wedding-backend-mongo
./setup.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Create a `.env` file from template

### 2. Configure Database

Edit the `.env` file with your MongoDB Atlas URI:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/wedding?retryWrites=true&w=majority
```

### 3. (Optional) Check MongoDB Connection

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
  "rsvp_id": "<mongodb_object_id>"
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
  "rsvp_id": "<mongodb_object_id>"
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
      "id": "<mongodb_object_id>",
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
      "id": "<mongodb_object_id>",
      "response_type": "yes",
      "full_name": "Jane Doe",
      "telegram_username": "@janedoe",
      "phone_number": "+6512345678",
      "dietary_restrictions": "Vegetarian, no nuts",
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "count": 1
}
``` 