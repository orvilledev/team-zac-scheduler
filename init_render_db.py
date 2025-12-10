"""
Database initialization script for Render deployment
Run this script once after deploying to Render to initialize the database

Usage: python init_render_db.py
"""
import os
import sys

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, init_db
from models import User

def init_database():
    """Initialize the database and create tables"""
    with app.app_context():
        print("=" * 60)
        print("Initializing Database for Render Deployment")
        print("=" * 60)
        
        # Use the app's init_db function which handles migrations
        print("\nCreating database tables and running migrations...")
        init_db()
        print("✓ Database tables created successfully!")
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("\nCreating default admin user...")
            admin = User(
                username='admin',
                role='admin',
                display_name='Administrator'
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created!")
            print("  Username: admin")
            print("  Note: Passwords are disabled - just use the username to login")
        else:
            print("\n✓ Admin user already exists.")
            print("  Username: admin")
        
        print("\n" + "=" * 60)
        print("✓ Database initialization completed!")
        print("=" * 60)
        print("\nYou can now access your application and login with:")
        print("  Username: admin")
        print("  (No password required)")

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

