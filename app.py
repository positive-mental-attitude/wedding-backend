import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)



# MongoDB configuration
MONGODB_URI = os.environ['MONGODB_URI']
client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
db = client.get_default_database()  # Uses the database from the URI

afterparty_collection = db['afterparty']
wedding_rsvp_collection = db['wedding_rsvp']

@app.route('/api/rsvp', methods=['POST'])
def submit_rsvp():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        required_fields = ['name', 'telegram', 'phone_number']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        if not isinstance(data['name'], str) or len(data['name'].strip()) == 0:
            return jsonify({'error': 'Name must be a non-empty string'}), 400
        if not isinstance(data['telegram'], str) or len(data['telegram'].strip()) == 0:
            return jsonify({'error': 'Telegram must be a non-empty string'}), 400
        if not isinstance(data['phone_number'], str) or len(data['phone_number'].strip()) == 0:
            return jsonify({'error': 'Phone number must be a non-empty string'}), 400
        new_rsvp = {
            'name': data['name'].strip(),
            'telegram': data['telegram'].strip(),
            'phone_number': data['phone_number'].strip(),
            'created_at': datetime.utcnow()
        }
        result = afterparty_collection.insert_one(new_rsvp)
        return jsonify({'message': 'RSVP received', 'rsvp_id': str(result.inserted_id)}), 201
    except Exception as e:
        app.logger.error(f'Error submitting RSVP: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/rsvp', methods=['GET'])
def get_rsvps():
    try:
        rsvps = list(afterparty_collection.find().sort('created_at', -1))
        for rsvp in rsvps:
            rsvp['id'] = str(rsvp['_id'])
            rsvp['created_at'] = rsvp['created_at'].isoformat() if 'created_at' in rsvp else None
            del rsvp['_id']
        return jsonify({'rsvps': rsvps, 'count': len(rsvps)}), 200
    except Exception as e:
        app.logger.error(f'Error retrieving RSVPs: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/wedding-rsvp', methods=['POST'])
def submit_wedding_rsvp():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        if 'response_type' not in data or data['response_type'] not in ['yes', 'no', 'maybe']:
            return jsonify({'error': 'response_type must be one of: yes, no, maybe'}), 400
        if 'full_name' not in data or not isinstance(data['full_name'], str) or len(data['full_name'].strip()) == 0:
            return jsonify({'error': 'Full name must be a non-empty string'}), 400
        response_type = data['response_type']
        full_name = data['full_name'].strip()
        new_rsvp = {
            'response_type': response_type,
            'full_name': full_name,
            'created_at': datetime.utcnow()
        }
        if response_type == 'yes':
            if 'telegram_username' not in data or not isinstance(data['telegram_username'], str) or len(data['telegram_username'].strip()) == 0:
                return jsonify({'error': 'Telegram username is required for yes responses'}), 400
            if 'phone_number' not in data or not isinstance(data['phone_number'], str) or len(data['phone_number'].strip()) == 0:
                return jsonify({'error': 'Phone number is required for yes responses'}), 400
            new_rsvp['telegram_username'] = data['telegram_username'].strip()
            new_rsvp['phone_number'] = data['phone_number'].strip()
            new_rsvp['dietary_restrictions'] = data.get('dietary_restrictions', '').strip() if data.get('dietary_restrictions') else None
        elif response_type == 'no':
            new_rsvp['message'] = data.get('message', '').strip() if data.get('message') else None
        elif response_type == 'maybe':
            new_rsvp['note'] = data.get('note', '').strip() if data.get('note') else None
        result = wedding_rsvp_collection.insert_one(new_rsvp)
        return jsonify({'message': f'Wedding RSVP ({response_type}) received', 'rsvp_id': str(result.inserted_id)}), 201
    except Exception as e:
        app.logger.error(f'Error submitting Wedding RSVP: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/wedding-rsvp', methods=['GET'])
def get_wedding_rsvps():
    try:
        response_type = request.args.get('response_type')
        query = {}
        if response_type:
            if response_type not in ['yes', 'no', 'maybe']:
                return jsonify({'error': 'response_type must be one of: yes, no, maybe'}), 400
            query['response_type'] = response_type
        rsvps = list(wedding_rsvp_collection.find(query).sort('created_at', -1))
        rsvps_by_type = {'yes': [], 'no': [], 'maybe': []}
        for rsvp in rsvps:
            rsvp['id'] = str(rsvp['_id'])
            rsvp['created_at'] = rsvp['created_at'].isoformat() if 'created_at' in rsvp else None
            rsvps_by_type[rsvp['response_type']].append(rsvp.copy())
            del rsvp['_id']
        return jsonify({
            'rsvps': rsvps,
            'rsvps_by_type': rsvps_by_type,
            'count': len(rsvps),
            'count_by_type': {k: len(v) for k, v in rsvps_by_type.items()}
        }), 200
    except Exception as e:
        app.logger.error(f'Error retrieving Wedding RSVPs: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test MongoDB connection
        client.admin.command('ping')
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
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    ) 