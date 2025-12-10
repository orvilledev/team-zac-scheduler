"""
Decorators for role-based access control
"""
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import login_required, current_user

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('Admin or Team Leader access required.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def worship_leader_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_worship_leader():
            flash('Worship leader or admin access required.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission_type):
    """Decorator to check if user has a specific permission"""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not (current_user.is_admin() or current_user.is_worship_leader() or current_user.has_permission(permission_type)):
                flash('You do not have permission to perform this action.', 'danger')
                return redirect(url_for('main.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

