#!/usr/bin/env python
"""Quick test to see if the Flask app can start"""
import sys
import os

try:
    print("Importing app...")
    from app import app
    print("App imported successfully!")
    
    print("\nTesting app configuration...")
    print(f"Debug mode: {app.config.get('DEBUG', 'Not set')}")
    print(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')}")
    
    print("\nCreating test client...")
    client = app.test_client()
    print("Test client created successfully!")
    
    print("\n✓ All checks passed! The app should be able to run.")
    print("\nTo start the server, run: py app.py")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

