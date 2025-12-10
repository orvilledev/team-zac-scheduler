"""
Template filters and context processors
"""
from flask import current_app
from flask_login import current_user
from flask_wtf.csrf import generate_csrf
from models import Notification

def register_template_helpers(app):
    """Register all template filters and context processors"""
    
    @app.context_processor
    def inject_csrf_token():
        def get_csrf_token():
            return generate_csrf()
        
        unread_notification_count = 0
        if current_user.is_authenticated:
            unread_notification_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        
        return dict(
            get_csrf_token=get_csrf_token,
            unread_notification_count=unread_notification_count
        )
    
    @app.template_filter('format_instrument')
    def format_instrument(instrument):
        """Format instrument name with appropriate suffix"""
        if not instrument:
            return ""
        
        instrument_lower = instrument.lower().strip()
        
        if instrument_lower == 'drums' or instrument_lower == 'drum':
            return 'Drummer'
        elif instrument_lower == 'vocals' or instrument_lower == 'vocal':
            return 'Vocalist'
        elif instrument_lower == 'keyboard' or instrument_lower == 'keyboards':
            return 'Keyboardist'
        else:
            return f"{instrument} player"
    
    @app.template_filter('bold_title')
    def bold_title_filter(text, title):
        """Bold the title if it appears at the start of the text"""
        if not text or not title:
            return text
        text = text.lstrip()
        title = title.strip()
        if text.lower().startswith(title.lower()):
            remaining_text = text[len(title):]
            return f'<strong>{text[:len(title)]}</strong>{remaining_text}'
        return text
    
    @app.template_filter('manila_time')
    def manila_time(dt):
        """Convert UTC datetime to Manila time (UTC+8)"""
        if not dt:
            return None
        
        try:
            import pytz
            utc = pytz.UTC
            manila_tz = pytz.timezone('Asia/Manila')
            
            if dt.tzinfo is None:
                dt = utc.localize(dt)
            
            manila_dt = dt.astimezone(manila_tz)
            return manila_dt
        except ImportError:
            from datetime import timedelta, timezone
            if dt.tzinfo is None:
                return dt + timedelta(hours=8)
            else:
                utc_dt = dt.astimezone(timezone.utc) if hasattr(dt, 'astimezone') else dt
                return utc_dt.replace(tzinfo=None) + timedelta(hours=8)
    
    @app.context_processor
    def inject_manila_time_formatter():
        """Make manila_time formatter available in templates"""
        # Get the manila_time filter function
        manila_time_filter = app.template_filters.get('manila_time')
        
        def format_manila_time(dt, format_string='%B %d, %Y at %I:%M %p'):
            """Format datetime in Manila time"""
            if not dt:
                return ''
            if manila_time_filter:
                manila_dt = manila_time_filter(dt)
                if manila_dt:
                    return manila_dt.strftime(format_string)
            return ''
        return dict(format_manila_time=format_manila_time)

