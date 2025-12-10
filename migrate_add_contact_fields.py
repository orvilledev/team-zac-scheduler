"""
Migration script to add mobile, outlook_email, and whatsapp columns to musician table
Run this once to add the new contact fields
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
    cursor.execute("PRAGMA table_info(musician)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'mobile' not in columns:
        print("Adding mobile column to musician table...")
        cursor.execute("""
            ALTER TABLE musician 
            ADD COLUMN mobile VARCHAR(20)
        """)
        print("✓ mobile column added successfully!")
    else:
        print("mobile column already exists. Skipping.")
    
    if 'outlook_email' not in columns:
        print("Adding outlook_email column to musician table...")
        cursor.execute("""
            ALTER TABLE musician 
            ADD COLUMN outlook_email VARCHAR(120)
        """)
        print("✓ outlook_email column added successfully!")
    else:
        print("outlook_email column already exists. Skipping.")
    
    if 'whatsapp' not in columns:
        print("Adding whatsapp column to musician table...")
        cursor.execute("""
            ALTER TABLE musician 
            ADD COLUMN whatsapp VARCHAR(20)
        """)
        print("✓ whatsapp column added successfully!")
    else:
        print("whatsapp column already exists. Skipping.")
    
    conn.commit()
    conn.close()
    print("\nMigration completed successfully!")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)

