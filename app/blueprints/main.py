"""
Main blueprint - Dashboard and home routes
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import date, datetime, timedelta
from collections import defaultdict
from sqlalchemy.orm import joinedload
from models import (
    db, SundayService, Practice, PracticeMusician, PracticeSong,
    Musician, EventAnnouncement
)

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard page"""
    # Get upcoming services (next 4 weeks)
    today = date.today()
    upcoming_services = SundayService.query.filter(
        SundayService.date >= today
    ).order_by(SundayService.date).limit(5).all()
    
    # Get only the latest upcoming practice with eager loading
    latest_practice = Practice.query.options(
        joinedload(Practice.musicians).joinedload(PracticeMusician.musician),
        joinedload(Practice.songs).joinedload(PracticeSong.song),
        joinedload(Practice.songs).joinedload(PracticeSong.preparer)
    ).filter(
        Practice.date >= today
    ).order_by(Practice.date).first()
    
    # Check if current user is assigned to the latest practice
    user_assignment_info = None
    if latest_practice:
        # Get or create musician profile for current user if needed
        if not current_user.musician:
            musician = Musician(
                name=current_user.get_display_name(),
                user_id=current_user.id,
                instruments=current_user.role if current_user.role in ['case_manager', 'shipment_coordinator', 'data_analyst', 'team_leader'] else None
            )
            db.session.add(musician)
            db.session.commit()
        elif not current_user.musician.instruments and current_user.role in ['case_manager', 'shipment_coordinator', 'data_analyst', 'team_leader']:
            current_user.musician.instruments = current_user.role
            db.session.commit()
        else:
            musician = current_user.musician
        
        # Check if user is assigned to this practice
        practice_assignments = PracticeMusician.query.filter_by(practice_id=latest_practice.id).all()
        for assignment in practice_assignments:
            if assignment.musician and assignment.musician_id == musician.id:
                user_assignment_info = {
                    'instrument': assignment.instrument,
                    'nickname': current_user.get_display_name(),
                    'date': latest_practice.date.strftime('%B %d, %Y')
                }
                break
    
    # Get newly added musicians (created within the last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    all_new_musicians = Musician.query.filter(
        Musician.created_at >= thirty_days_ago
    ).order_by(Musician.created_at.desc()).all()
    
    # Group musicians by user_id or display name to avoid duplicates
    musician_dict = {}
    
    for musician in all_new_musicians:
        display_name = musician.get_display_name().strip().lower() if musician.get_display_name() else musician.name.strip().lower()
        
        existing_musician = None
        existing_key = None
        
        if musician.user_id:
            for key, existing in musician_dict.items():
                if existing.user_id == musician.user_id:
                    existing_musician = existing
                    existing_key = key
                    break
        
        if not existing_musician:
            for key, existing in musician_dict.items():
                existing_display = existing.get_display_name().strip().lower() if existing.get_display_name() else existing.name.strip().lower()
                if existing_display == display_name:
                    existing_musician = existing
                    existing_key = key
                    break
        
        if existing_musician:
            existing_instruments = set()
            new_instruments = set()
            
            if existing_musician.instruments:
                existing_instruments = {inst.strip() for inst in existing_musician.instruments.split(',') if inst.strip()}
            if musician.instruments:
                new_instruments = {inst.strip() for inst in musician.instruments.split(',') if inst.strip()}
            
            combined_instruments = ', '.join(sorted(existing_instruments | new_instruments))
            existing_musician.instruments = combined_instruments if combined_instruments else None
        else:
            if musician.user_id:
                key = f"user_{musician.user_id}"
            else:
                key = f"name_{display_name}"
            musician_dict[key] = musician
    
    new_musicians = list(musician_dict.values())
    
    # Get active event announcements
    announcements = EventAnnouncement.query.filter_by(is_active=True).order_by(EventAnnouncement.display_order, EventAnnouncement.created_at.desc()).all()
    
    return render_template('dashboard.html',
                         upcoming_services=upcoming_services,
                         latest_practice=latest_practice,
                         user_assignment_info=user_assignment_info,
                         new_musicians=new_musicians,
                         announcements=announcements)

