"""
Migration script to add Journal table to the database
Run this once to add the journal table
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
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='journal'
    """)
    
    if cursor.fetchone():
        print("Journal table already exists. Skipping migration.")
    else:
        print("Creating Journal table...")
        
        # Create Journal table
        cursor.execute("""
            CREATE TABLE journal (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                entry_type VARCHAR(50) NOT NULL,
                title VARCHAR(200),
                content TEXT NOT NULL,
                image_path VARCHAR(255),
                date DATE NOT NULL,
                created_at DATETIME,
                updated_at DATETIME,
                FOREIGN KEY(user_id) REFERENCES user (id)
            )
        """)
        
        # Create indexes for better query performance
        cursor.execute("CREATE INDEX idx_journal_user_id ON journal(user_id)")
        cursor.execute("CREATE INDEX idx_journal_entry_type ON journal(entry_type)")
        cursor.execute("CREATE INDEX idx_journal_date ON journal(date DESC)")
        
        conn.commit()
        print("✓ Journal table created successfully!")
        print("✓ Indexes created successfully!")
    
    conn.close()
    print("\nMigration completed successfully!")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)

