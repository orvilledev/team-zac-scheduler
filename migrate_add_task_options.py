"""
Migration script to add TaskOption table for saved task templates
Run this script to add the task_options table to the database.
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
    
    # Check if table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='task_option'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("Creating task_option table...")
        cursor.execute("""
            CREATE TABLE task_option (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_text VARCHAR(500) NOT NULL,
                priority INTEGER DEFAULT 2,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES user (id)
            )
        """)
        print("✓ task_option table created successfully!")
    else:
        print("task_option table already exists. Skipping.")
    
    conn.commit()
    conn.close()
    print("\nMigration completed successfully!")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)

