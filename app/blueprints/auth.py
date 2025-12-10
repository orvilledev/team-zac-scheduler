"""
Authentication blueprint
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from forms import LoginForm

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip() if form.username.data else ''
        
        if not username:
            flash('Please enter a username.', 'danger')
            return render_template('login.html', form=form)
        
        from models import User
        user = User.query.filter_by(username=username).first()
        
        if not user:
            flash('User not found.', 'danger')
            return render_template('login.html', form=form)
        
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
    
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('auth.login'))
    except Exception as e:
        print(f"Error during logout: {e}")
        return redirect(url_for('auth.login'))

