"""
Migration script to add Task table
Run this script to add the Task table to the database.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Task
from config import Config

def migrate():
    """Create Task table if it doesn't exist"""
    # Create a minimal Flask app for migration
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        try:
            # Try to create all tables - SQLAlchemy will skip if they exist
            db.create_all()
            db.session.commit()
            print("Task table created/verified successfully!")
        except Exception as e:
            print(f"Error creating Task table: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    migrate()

