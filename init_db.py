#!/usr/bin/env python3
"""
Database initialization script for the Afterparty RSVP application.
This script creates the database and tables if they don't exist.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_config():
    """Parse DATABASE_URL to get connection parameters"""
    database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/afterparty_db')
    
    # Parse the URL: postgresql://username:password@host:port/database
    if database_url.startswith('postgresql://'):
        url_parts = database_url.replace('postgresql://', '').split('@')
        if len(url_parts) == 2:
            auth_part, host_db_part = url_parts
            username, password = auth_part.split(':')
            host_port, database = host_db_part.split('/')
            
            if ':' in host_port:
                host, port = host_port.split(':')
            else:
                host, port = host_port, '5432'
                
            return {
                'host': host,
                'port': port,
                'user': username,
                'password': password,
                'database': database
            }
    
    # Fallback to default values
    return {
        'host': 'localhost',
        'port': '5432',
        'user': 'postgres',
        'password': 'password',
        'database': 'afterparty_db'
    }

def create_database():
    """Create the database if it doesn't exist"""
    config = get_db_config()
    
    # Connect to PostgreSQL server (not to a specific database)
    conn = psycopg2.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database='postgres'  # Connect to default postgres database
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    try:
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (config['database'],))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database '{config['database']}'...")
            cursor.execute(f'CREATE DATABASE "{config["database"]}"')
            print(f"Database '{config['database']}' created successfully!")
        else:
            print(f"Database '{config['database']}' already exists.")
            
    except Exception as e:
        print(f"Error creating database: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def create_tables():
    """Create the afterparty table using Flask-SQLAlchemy"""
    from app import app, db
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("Tables created successfully!")
            
            # Verify table structure
            from app import AfterpartyRSVP
            print(f"Table '{AfterpartyRSVP.__tablename__}' is ready for use.")
            
        except Exception as e:
            print(f"Error creating tables: {e}")
            raise

def main():
    """Main function to initialize the database"""
    print("Initializing Afterparty RSVP Database...")
    print("=" * 50)
    
    try:
        # Step 1: Create database
        create_database()
        
        # Step 2: Create tables
        create_tables()
        
        print("=" * 50)
        print("Database initialization completed successfully!")
        print("You can now run the Flask application with: python app.py")
        
    except Exception as e:
        print(f"Database initialization failed: {e}")
        print("Please check your PostgreSQL connection and credentials.")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main()) 