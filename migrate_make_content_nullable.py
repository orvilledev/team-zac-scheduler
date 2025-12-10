import sqlite3
import os

# Determine the path to the database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def migrate():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print(f"Connecting to database: {DB_PATH}")
        
        # SQLite doesn't support ALTER COLUMN directly, so we need to:
        # 1. Create a new table with the updated schema
        # 2. Copy data from old table to new table
        # 3. Drop old table
        # 4. Rename new table
        
        print("\nStep 1: Creating new journal table with nullable content...")
        cursor.execute("""
            CREATE TABLE journal_new (
                id INTEGER NOT NULL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                entry_type VARCHAR(50) NOT NULL,
                title VARCHAR(200),
                content TEXT,
                application TEXT,
                prayer_text TEXT,
                image_path VARCHAR(255),
                mood_emojis VARCHAR(500),
                date DATE NOT NULL,
                created_at DATETIME,
                updated_at DATETIME,
                FOREIGN KEY(user_id) REFERENCES user (id)
            )
        """)
        
        print("Step 2: Copying data from old table to new table...")
        cursor.execute("""
            INSERT INTO journal_new 
            (id, user_id, entry_type, title, content, application, prayer_text, 
             image_path, mood_emojis, date, created_at, updated_at)
            SELECT 
                id, user_id, entry_type, title, content, application, prayer_text,
                image_path, mood_emojis, date, created_at, updated_at
            FROM journal
        """)
        
        print("Step 3: Dropping old journal table...")
        cursor.execute("DROP TABLE journal")
        
        print("Step 4: Renaming new table to journal...")
        cursor.execute("ALTER TABLE journal_new RENAME TO journal")
        
        conn.commit()
        print("\n✓ Migration completed successfully!")
        print("The content column in the journal table is now nullable.")
        
    except sqlite3.Error as e:
        print(f"\n✗ Database error: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    migrate()

