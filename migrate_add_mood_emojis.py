"""
Migration script to add mood_emojis column to Journal table
Run this once to add the mood emojis field
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
    cursor.execute("PRAGMA table_info(journal)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'mood_emojis' in columns:
        print("mood_emojis column already exists. Skipping migration.")
    else:
        print("Adding mood_emojis column to journal table...")
        
        # Add mood_emojis column
        cursor.execute("""
            ALTER TABLE journal 
            ADD COLUMN mood_emojis VARCHAR(500)
        """)
        
        conn.commit()
        print("✓ mood_emojis column added successfully!")
    
    conn.close()
    print("\nMigration completed successfully!")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)

