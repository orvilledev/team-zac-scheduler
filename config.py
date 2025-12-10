import os
from datetime import timedelta

class Config:
    """Configuration class for Flask application"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database Configuration
    # Support PostgreSQL (Render) and SQLite (local development)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    elif not SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'database.db')
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'chords')
    SLIDES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'slides')
    ANNOUNCEMENTS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'announcements')
    JOURNALS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'journals')
    TOOLS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'tools')
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB max file size (for videos)
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG'}
    ALLOWED_SLIDE_EXTENSIONS = {'ppt', 'pptx', 'doc', 'docx', 'xls', 'xlsx', 'csv', 'pdf', 'txt', 'jpg', 'jpeg', 'png', 'gif', 'PPT', 'PPTX', 'DOC', 'DOCX', 'XLS', 'XLSX', 'CSV', 'PDF', 'TXT', 'JPG', 'JPEG', 'PNG', 'GIF'}
    ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF'}
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'MP4', 'MOV', 'AVI', 'MKV'}
    
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

