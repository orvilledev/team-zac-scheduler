"""
Quick fix script to add recipient_id column to message table
Run this to fix the database immediately
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
    
    # Check if message table exists
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='message'
    """)
    
    if not cursor.fetchone():
        print("Message table does not exist. It will be created when you run the app.")
        conn.close()
        exit(0)
    
    # Check if recipient_id column already exists
    cursor.execute("PRAGMA table_info(message)")
    columns = [row[1] for row in cursor.fetchall()]
    
    print(f"Current columns in message table: {columns}")
    
    if 'recipient_id' in columns:
        print("✓ recipient_id column already exists. No migration needed.")
    else:
        print("Adding recipient_id column to message table...")
        
        # Add the column
        cursor.execute("""
            ALTER TABLE message ADD COLUMN recipient_id INTEGER
        """)
        
        conn.commit()
        print("✓ recipient_id column added successfully!")
    
    # Verify it was added
    cursor.execute("PRAGMA table_info(message)")
    columns_after = [row[1] for row in cursor.fetchall()]
    print(f"Columns after migration: {columns_after}")
    
    conn.close()
    print("\n✓ Migration completed successfully!")
    
except sqlite3.Error as e:
    print(f"❌ Database error: {e}")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

