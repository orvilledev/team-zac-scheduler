"""
Migration script to add twilio_status column to SMSLog table
Run this once to add the Twilio status tracking field
"""
import sqlite3
import os

# Get the database path
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'database.db')

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    print("The database will be created automatically when you run the app.")
    exit(1)

print(f"Connecting to database: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if column already exists
    cursor.execute("PRAGMA table_info(sms_log)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'twilio_status' in columns:
        print("twilio_status column already exists. Skipping migration.")
    else:
        print("Adding twilio_status column to sms_log table...")
        
        # Add twilio_status column
        cursor.execute("""
            ALTER TABLE sms_log 
            ADD COLUMN twilio_status VARCHAR(20)
        """)
        
        conn.commit()
        print("✓ twilio_status column added successfully!")
    
    conn.close()
    print("\nMigration completed successfully!")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)

