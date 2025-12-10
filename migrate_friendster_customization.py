"""
Database migration script to add Friendster-like customization fields to Musician model.
Run this script once to add the new columns to your existing database.

Usage: python migrate_friendster_customization.py
"""

from app import app, db
from models import Musician
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            # Check if columns already exist by trying to query them
            db.session.execute(text("SELECT background_image FROM musician LIMIT 1"))
            print("Customization columns already exist. Migration not needed.")
            return
        except Exception:
            pass
        
        print("Adding Friendster customization columns to Musician table...")
        
        try:
            # Add new columns
            db.session.execute(text("""
                ALTER TABLE musician 
                ADD COLUMN background_image VARCHAR(255)
            """))
            print("✓ Added background_image column")
        except Exception as e:
            print(f"  Note: background_image column may already exist: {e}")
        
        try:
            db.session.execute(text("""
                ALTER TABLE musician 
                ADD COLUMN background_color VARCHAR(50)
            """))
            print("✓ Added background_color column")
        except Exception as e:
            print(f"  Note: background_color column may already exist: {e}")
        
        try:
            db.session.execute(text("""
                ALTER TABLE musician 
                ADD COLUMN custom_css TEXT
            """))
            print("✓ Added custom_css column")
        except Exception as e:
            print(f"  Note: custom_css column may already exist: {e}")
        
        try:
            db.session.execute(text("""
                ALTER TABLE musician 
                ADD COLUMN music_player_embed TEXT
            """))
            print("✓ Added music_player_embed column")
        except Exception as e:
            print(f"  Note: music_player_embed column may already exist: {e}")
        
        try:
            db.session.execute(text("""
                ALTER TABLE musician 
                ADD COLUMN profile_theme VARCHAR(50) DEFAULT 'default'
            """))
            print("✓ Added profile_theme column")
        except Exception as e:
            print(f"  Note: profile_theme column may already exist: {e}")
        
        try:
            db.session.execute(text("""
                ALTER TABLE musician 
                ADD COLUMN text_color VARCHAR(50)
            """))
            print("✓ Added text_color column")
        except Exception as e:
            print(f"  Note: text_color column may already exist: {e}")
        
        try:
            db.session.execute(text("""
                ALTER TABLE musician 
                ADD COLUMN link_color VARCHAR(50)
            """))
            print("✓ Added link_color column")
        except Exception as e:
            print(f"  Note: link_color column may already exist: {e}")
        
        try:
            db.session.execute(text("""
                ALTER TABLE musician 
                ADD COLUMN profile_views INTEGER DEFAULT 0
            """))
            print("✓ Added profile_views column")
        except Exception as e:
            print(f"  Note: profile_views column may already exist: {e}")
        
        try:
            db.session.commit()
            print("\n✅ Migration completed successfully!")
            print("You can now use the profile customization features.")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Migration failed: {e}")
            print("Please check your database connection and try again.")

if __name__ == '__main__':
    migrate()

