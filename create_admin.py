"""
Script to create an admin user in the database
Run this on Render after deployment to create your admin account
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def create_admin():
    """Create an admin user"""
    with app.app_context():
        username = input("Enter admin username (default: admin): ").strip() or 'admin'
        display_name = input("Enter display name (default: Administrator): ").strip() or 'Administrator'
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"User '{username}' already exists!")
            response = input("Do you want to update their role to admin? (y/n): ").strip().lower()
            if response == 'y':
                existing_user.role = 'admin'
                existing_user.display_name = display_name
                db.session.commit()
                print(f"✓ User '{username}' updated to admin!")
            return
        
        # Create new admin user
        admin = User(
            username=username,
            role='admin',
            display_name=display_name
        )
        db.session.add(admin)
        db.session.commit()
        print(f"✓ Admin user '{username}' created successfully!")

if __name__ == '__main__':
    create_admin()

