"""
Flask application factory
"""
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_caching import Cache
from config import Config
from models import db, User

# Initialize extensions
csrf = CSRFProtect()
login_manager = LoginManager()
cache = Cache()

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/')
    
    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.blueprints.musicians import bp as musicians_bp
    app.register_blueprint(musicians_bp, url_prefix='/musicians')
    
    from app.blueprints.services import bp as services_bp
    app.register_blueprint(services_bp, url_prefix='/services')
    
    from app.blueprints.practices import bp as practices_bp
    app.register_blueprint(practices_bp, url_prefix='/practices')
    
    from app.blueprints.songs import bp as songs_bp
    app.register_blueprint(songs_bp, url_prefix='/songs')
    
    from app.blueprints.slides import bp as slides_bp
    app.register_blueprint(slides_bp, url_prefix='/slides')
    
    from app.blueprints.notifications import bp as notifications_bp
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
    
    from app.blueprints.announcements import bp as announcements_bp
    app.register_blueprint(announcements_bp, url_prefix='/announcements')
    
    from app.blueprints.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')
    
    from app.blueprints.permissions import bp as permissions_bp
    app.register_blueprint(permissions_bp, url_prefix='/permissions')
    
    from app.blueprints.journal import bp as journal_bp
    app.register_blueprint(journal_bp, url_prefix='/journal')
    
    from app.blueprints.sms import bp as sms_bp
    app.register_blueprint(sms_bp, url_prefix='/sms')
    
    from app.blueprints.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Register template filters and context processors
    from app.utils.template_helpers import register_template_helpers
    register_template_helpers(app)
    
    # Initialize scheduler
    from app.utils.scheduler import init_scheduler
    init_scheduler(app)
    
    return app

