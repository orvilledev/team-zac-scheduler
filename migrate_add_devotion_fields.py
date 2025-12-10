"""
Migration script to add application and prayer_text columns to Journal table
Run this once to add the devotion-specific fields
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
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(journal)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'application' not in columns:
        print("Adding application column to journal table...")
        cursor.execute("""
            ALTER TABLE journal 
            ADD COLUMN application TEXT
        """)
        print("✓ application column added successfully!")
    else:
        print("application column already exists. Skipping.")
    
    if 'prayer_text' not in columns:
        print("Adding prayer_text column to journal table...")
        cursor.execute("""
            ALTER TABLE journal 
            ADD COLUMN prayer_text TEXT
        """)
        print("✓ prayer_text column added successfully!")
    else:
        print("prayer_text column already exists. Skipping.")
    
    conn.commit()
    conn.close()
    print("\nMigration completed successfully!")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)

