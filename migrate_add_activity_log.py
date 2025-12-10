"""
Migration script to add ActivityLog table
Run this script to add the ActivityLog table to the database.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import directly from models and config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, ActivityLog
from config import Config

def migrate():
    """Create ActivityLog table if it doesn't exist"""
    # Create a minimal Flask app for migration
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        try:
            # Try to create all tables - SQLAlchemy will skip if they exist
            db.create_all()
            db.session.commit()
            print("ActivityLog table created/verified successfully!")
        except Exception as e:
            print(f"Error creating ActivityLog table: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    migrate()
