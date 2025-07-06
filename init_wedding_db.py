#!/usr/bin/env python3
"""
Database initialization script for the Wedding RSVP application.
This script creates the wedding database and tables if they don't exist.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_wedding_db_config():
    """Parse WEDDING_DATABASE_URL to get connection parameters"""
    database_url = os.getenv('WEDDING_DATABASE_URL', 'postgresql://paulcheong:afterparty_pw@localhost:5432/wedding_rsvp_db')
    
    # Parse the URL: postgresql://username:password@host:port/database
    if database_url.startswith('postgresql://'):
        url_parts = database_url.replace('postgresql://', '').split('@')
        if len(url_parts) == 2:
            auth_part, host_db_part = url_parts
            if ':' in auth_part:
                username, password = auth_part.split(':')
            else:
                username, password = auth_part, ''
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
        'user': 'paulcheong',
        'password': 'afterparty_pw',
        'database': 'wedding_rsvp_db'
    }

def create_wedding_database():
    """Create the wedding database if it doesn't exist"""
    config = get_wedding_db_config()
    
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
            print(f"Creating wedding database '{config['database']}'...")
            cursor.execute(f'CREATE DATABASE "{config["database"]}"')
            print(f"Wedding database '{config['database']}' created successfully!")
        else:
            print(f"Wedding database '{config['database']}' already exists.")
            
    except Exception as e:
        print(f"Error creating wedding database: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def create_wedding_tables():
    """Create the wedding_rsvp table using Flask-SQLAlchemy"""
    from app import app, db
    
    with app.app_context():
        try:
            # Create all tables (including wedding tables)
            db.create_all()
            print("Wedding tables created successfully!")
            
            # Verify table structure
            from app import WeddingRSVP
            print(f"Table '{WeddingRSVP.__tablename__}' is ready for use.")
            
        except Exception as e:
            print(f"Error creating wedding tables: {e}")
            raise

def main():
    """Main function to initialize the wedding database"""
    print("Initializing Wedding RSVP Database...")
    print("=" * 50)
    
    try:
        # Step 1: Create wedding database
        create_wedding_database()
        
        # Step 2: Create wedding tables
        create_wedding_tables()
        
        print("=" * 50)
        print("Wedding database initialization completed successfully!")
        print("You can now use the wedding RSVP endpoints.")
        
    except Exception as e:
        print(f"Wedding database initialization failed: {e}")
        print("Please check your PostgreSQL connection and credentials.")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main()) 