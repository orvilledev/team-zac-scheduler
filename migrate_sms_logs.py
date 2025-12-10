"""
Migration script to add SMSLog table to the database
Run this once to add the SMS logs table
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
        WHERE type='table' AND name='sms_log'
    """)
    
    if cursor.fetchone():
        print("SMSLog table already exists. Skipping migration.")
    else:
        print("Creating SMSLog table...")
        
        # Create SMSLog table
        cursor.execute("""
            CREATE TABLE sms_log (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                recipient_user_id INTEGER,
                recipient_phone VARCHAR(20) NOT NULL,
                recipient_name VARCHAR(200),
                message_type VARCHAR(50) NOT NULL,
                practice_id INTEGER,
                musician_id INTEGER,
                message_content TEXT,
                status VARCHAR(20) NOT NULL,
                error_message TEXT,
                sent_by_user_id INTEGER,
                created_at DATETIME,
                FOREIGN KEY(recipient_user_id) REFERENCES user (id),
                FOREIGN KEY(practice_id) REFERENCES practice (id),
                FOREIGN KEY(musician_id) REFERENCES musician (id),
                FOREIGN KEY(sent_by_user_id) REFERENCES user (id)
            )
        """)
        
        # Create indexes for better query performance
        cursor.execute("CREATE INDEX idx_sms_log_created_at ON sms_log(created_at DESC)")
        cursor.execute("CREATE INDEX idx_sms_log_status ON sms_log(status)")
        cursor.execute("CREATE INDEX idx_sms_log_message_type ON sms_log(message_type)")
        cursor.execute("CREATE INDEX idx_sms_log_recipient_user_id ON sms_log(recipient_user_id)")
        
        conn.commit()
        print("✓ SMSLog table created successfully!")
        print("✓ Indexes created successfully!")
    
    conn.close()
    print("\nMigration completed successfully!")
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)

