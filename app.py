from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:password@localhost:5432/afterparty_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Wedding database configuration
app.config['SQLALCHEMY_BINDS'] = {
    'wedding': os.getenv(
        'WEDDING_DATABASE_URL',
        'postgresql://paulcheong:afterparty_pw@localhost:5432/wedding_rsvp_db'
    )
}

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Enable CORS
CORS(app)

# SQLAlchemy Model for afterparty table
class AfterpartyRSVP(db.Model):
    __tablename__ = 'afterparty'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    telegram = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AfterpartyRSVP {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'telegram': self.telegram,
            'phone_number': self.phone_number,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# SQLAlchemy Model for wedding RSVP table
class WeddingRSVP(db.Model):
    __tablename__ = 'wedding_rsvp'
    __bind_key__ = 'wedding'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    response_type = db.Column(db.String(10), nullable=False)  # 'yes', 'no', 'maybe'
    full_name = db.Column(db.String(100), nullable=False)
    telegram_username = db.Column(db.String(50), nullable=True)  # Only for 'yes' responses
    phone_number = db.Column(db.String(20), nullable=True)  # Only for 'yes' responses
    dietary_restrictions = db.Column(db.Text, nullable=True)  # Only for 'yes' responses
    message = db.Column(db.Text, nullable=True)  # Only for 'no' responses
    note = db.Column(db.Text, nullable=True)  # Only for 'maybe' responses
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<WeddingRSVP {self.full_name} ({self.response_type})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'response_type': self.response_type,
            'full_name': self.full_name,
            'telegram_username': self.telegram_username,
            'phone_number': self.phone_number,
            'dietary_restrictions': self.dietary_restrictions,
            'message': self.message,
            'note': self.note,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

@app.route('/api/rsvp', methods=['POST'])
def submit_rsvp():
    """
    POST endpoint to submit RSVP information
    Expected JSON payload:
    {
        "name": "Jane Doe",
        "telegram": "@janedoe", 
        "phone_number": "+6512345678"
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['name', 'telegram', 'phone_number']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Validate data types and lengths
        if not isinstance(data['name'], str) or len(data['name'].strip()) == 0:
            return jsonify({'error': 'Name must be a non-empty string'}), 400
        
        if not isinstance(data['telegram'], str) or len(data['telegram'].strip()) == 0:
            return jsonify({'error': 'Telegram must be a non-empty string'}), 400
        
        if not isinstance(data['phone_number'], str) or len(data['phone_number'].strip()) == 0:
            return jsonify({'error': 'Phone number must be a non-empty string'}), 400
        
        # Create new RSVP entry
        new_rsvp = AfterpartyRSVP(
            name=data['name'].strip(),
            telegram=data['telegram'].strip(),
            phone_number=data['phone_number'].strip()
        )
        
        # Add to database
        db.session.add(new_rsvp)
        db.session.commit()
        
        return jsonify({
            'message': 'RSVP received',
            'rsvp_id': new_rsvp.id
        }), 201
        
    except Exception as e:
        # Rollback session in case of error
        db.session.rollback()
        app.logger.error(f'Error submitting RSVP: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/rsvp', methods=['GET'])
def get_rsvps():
    """
    GET endpoint to retrieve all RSVP entries (for admin purposes)
    """
    try:
        rsvps = AfterpartyRSVP.query.order_by(AfterpartyRSVP.created_at.desc()).all()
        return jsonify({
            'rsvps': [rsvp.to_dict() for rsvp in rsvps],
            'count': len(rsvps)
        }), 200
    except Exception as e:
        app.logger.error(f'Error retrieving RSVPs: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/wedding-rsvp', methods=['POST'])
def submit_wedding_rsvp():
    """
    POST endpoint to submit Wedding RSVP information
    Expected JSON payload for 'yes' response:
    {
        "response_type": "yes",
        "full_name": "Jane Doe",
        "telegram_username": "@janedoe",
        "phone_number": "+6512345678",
        "dietary_restrictions": "Vegetarian, no nuts"
    }
    
    Expected JSON payload for 'no' response:
    {
        "response_type": "no",
        "full_name": "John Doe",
        "message": "Sorry, I can't make it"
    }
    
    Expected JSON payload for 'maybe' response:
    {
        "response_type": "maybe",
        "full_name": "Bob Smith",
        "note": "I'll confirm closer to the date"
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate response_type
        if 'response_type' not in data or data['response_type'] not in ['yes', 'no', 'maybe']:
            return jsonify({'error': 'response_type must be one of: yes, no, maybe'}), 400
        
        # Validate full_name (required for all response types)
        if 'full_name' not in data or not isinstance(data['full_name'], str) or len(data['full_name'].strip()) == 0:
            return jsonify({'error': 'Full name must be a non-empty string'}), 400
        
        response_type = data['response_type']
        full_name = data['full_name'].strip()
        
        # Validate fields based on response type
        if response_type == 'yes':
            # For 'yes' responses, telegram_username and phone_number are required
            if 'telegram_username' not in data or not isinstance(data['telegram_username'], str) or len(data['telegram_username'].strip()) == 0:
                return jsonify({'error': 'Telegram username is required for yes responses'}), 400
            
            if 'phone_number' not in data or not isinstance(data['phone_number'], str) or len(data['phone_number'].strip()) == 0:
                return jsonify({'error': 'Phone number is required for yes responses'}), 400
            
            # Create new Wedding RSVP entry for 'yes' response
            new_rsvp = WeddingRSVP(
                response_type=response_type,
                full_name=full_name,
                telegram_username=data['telegram_username'].strip(),
                phone_number=data['phone_number'].strip(),
                dietary_restrictions=data.get('dietary_restrictions', '').strip() if data.get('dietary_restrictions') else None
            )
            
        elif response_type == 'no':
            # For 'no' responses, message is optional
            new_rsvp = WeddingRSVP(
                response_type=response_type,
                full_name=full_name,
                message=data.get('message', '').strip() if data.get('message') else None
            )
            
        elif response_type == 'maybe':
            # For 'maybe' responses, note is optional
            new_rsvp = WeddingRSVP(
                response_type=response_type,
                full_name=full_name,
                note=data.get('note', '').strip() if data.get('note') else None
            )
        
        # Add to database
        db.session.add(new_rsvp)
        db.session.commit()
        
        return jsonify({
            'message': f'Wedding RSVP ({response_type}) received',
            'rsvp_id': new_rsvp.id
        }), 201
        
    except Exception as e:
        # Rollback session in case of error
        db.session.rollback()
        app.logger.error(f'Error submitting Wedding RSVP: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/wedding-rsvp', methods=['GET'])
def get_wedding_rsvps():
    """
    GET endpoint to retrieve all Wedding RSVP entries (for admin purposes)
    Optional query parameter: response_type (yes, no, maybe)
    """
    try:
        response_type = request.args.get('response_type')
        
        if response_type and response_type not in ['yes', 'no', 'maybe']:
            return jsonify({'error': 'response_type must be one of: yes, no, maybe'}), 400
        
        if response_type:
            rsvps = WeddingRSVP.query.filter_by(response_type=response_type).order_by(WeddingRSVP.created_at.desc()).all()
        else:
            rsvps = WeddingRSVP.query.order_by(WeddingRSVP.created_at.desc()).all()
        
        # Group RSVPs by response type
        rsvps_by_type = {
            'yes': [],
            'no': [],
            'maybe': []
        }
        
        for rsvp in rsvps:
            rsvps_by_type[rsvp.response_type].append(rsvp.to_dict())
        
        return jsonify({
            'rsvps': [rsvp.to_dict() for rsvp in rsvps],
            'rsvps_by_type': rsvps_by_type,
            'count': len(rsvps),
            'count_by_type': {
                'yes': len(rsvps_by_type['yes']),
                'no': len(rsvps_by_type['no']),
                'maybe': len(rsvps_by_type['maybe'])
            }
        }), 200
    except Exception as e:
        app.logger.error(f'Error retrieving Wedding RSVPs: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'database': 'disconnected', 'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    # Run the Flask app
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    ) 