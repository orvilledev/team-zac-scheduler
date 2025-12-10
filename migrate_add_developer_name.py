"""
Migration script to add developer_name column to the tool table
Run this once to add the developer_name column
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
    
    # Check if tool table exists
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='tool'
    """)
    
    if not cursor.fetchone():
        print("Tool table does not exist. It will be created when you run the app.")
        conn.close()
        exit(0)
    
    # Check if developer_name column already exists
    cursor.execute("PRAGMA table_info(tool)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'developer_name' in columns:
        print("developer_name column already exists. Skipping migration.")
    else:
        print("Adding developer_name column to tool table...")
        
        # Add the column
        cursor.execute("""
            ALTER TABLE tool ADD COLUMN developer_name VARCHAR(200)
        """)
        
        conn.commit()
        print("✓ developer_name column added successfully!")
    
    conn.close()
    print("\nMigration completed successfully!")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    exit(1)

