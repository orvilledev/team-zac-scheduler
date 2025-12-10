"""
Migration script to add UserPermission table to the database
Run this once to add the permissions table
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
        WHERE type='table' AND name='user_permission'
    """)
    
    if cursor.fetchone():
        print("UserPermission table already exists. Skipping migration.")
    else:
        print("Creating UserPermission table...")
        
        # Create UserPermission table
        cursor.execute("""
            CREATE TABLE user_permission (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                permission_type VARCHAR(50) NOT NULL,
                granted_by INTEGER NOT NULL,
                granted_at DATETIME,
                FOREIGN KEY(user_id) REFERENCES user (id),
                FOREIGN KEY(granted_by) REFERENCES user (id),
                UNIQUE(user_id, permission_type)
            )
        """)
        
        # Create indexes for better query performance
        cursor.execute("CREATE INDEX idx_user_permission_user_id ON user_permission(user_id)")
        cursor.execute("CREATE INDEX idx_user_permission_type ON user_permission(permission_type)")
        
        conn.commit()
        print("✓ UserPermission table created successfully!")
        print("✓ Indexes created successfully!")
    
    conn.close()
    print("\nMigration completed successfully!")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)

