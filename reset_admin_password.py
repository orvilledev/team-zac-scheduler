"""
Script to reset the admin password in the database.
Run this script if you cannot log in as admin.

Usage: py -3 reset_admin_password.py
"""

import os
import sys
from werkzeug.security import generate_password_hash

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User

def reset_admin_password(new_password='admin123'):
    """Reset the admin user's password"""
    with app.app_context():
        # Find admin user
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("Admin user not found. Creating admin user...")
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin.set_password(new_password)
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user created with password: {new_password}")
        else:
            # Reset password
            admin.set_password(new_password)
            db.session.commit()
            print(f"Admin password reset successfully!")
            print(f"Username: admin")
            print(f"Password: {new_password}")
            print("\nYou can now log in with these credentials.")

if __name__ == '__main__':
    print("=" * 50)
    print("Admin Password Reset Script")
    print("=" * 50)
    print()
    
    # Ask for new password or use default
    use_default = input("Use default password 'admin123'? (y/n): ").strip().lower()
    
    if use_default == 'y' or use_default == '':
        new_password = 'admin123'
    else:
        new_password = input("Enter new password (min 6 characters): ").strip()
        if len(new_password) < 6:
            print("Error: Password must be at least 6 characters long.")
            sys.exit(1)
    
    try:
        reset_admin_password(new_password)
        print("\n" + "=" * 50)
        print("Password reset complete!")
        print("=" * 50)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

