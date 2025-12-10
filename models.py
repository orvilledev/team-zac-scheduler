from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)  # Optional - passwords disabled
    nickname = db.Column(db.String(100), nullable=True)  # Display name throughout the app
    mobile_number = db.Column(db.String(20), nullable=True)  # Mobile phone number
    role = db.Column(db.String(20), nullable=False, default='case_manager')  # admin, case_manager, shipment_coordinator, data_analyst, team_leader
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    musician = db.relationship('Musician', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password (optional - passwords disabled)"""
        if password and password.strip():
            self.password_hash = generate_password_hash(password.strip())
        else:
            # Allow empty passwords
            self.password_hash = None
    
    def check_password(self, password):
        """Check password against hash"""
        if not password:
            return False
        if not self.password_hash:
            return False
        
        # Try with stripped password first
        password_clean = password.strip()
        result = check_password_hash(self.password_hash, password_clean)
        
        # If that fails, try with original password (in case password was set with spaces)
        if not result:
            result = check_password_hash(self.password_hash, password)
        
        return result
    
    def is_admin(self):
        return self.role in ['admin', 'team_leader']
    
    def is_team_leader(self):
        return self.role == 'team_leader' or self.role == 'admin'
    
    def is_worship_leader(self):
        return self.role in ['admin', 'team_leader', 'case_manager']
    
    def has_permission(self, permission_type):
        """Check if user has a specific permission"""
        if self.is_admin():
            return True  # Admins have all permissions
        if self.is_worship_leader():
            # Worship leaders have default permissions, but can be overridden by specific permissions
            return any(p.permission_type == permission_type for p in self.permissions)
        # Regular users need explicit permission
        return any(p.permission_type == permission_type for p in self.permissions)
    
    def get_display_name(self):
        """Get display name (nickname if available, otherwise username)"""
        return self.nickname if self.nickname else self.username
    
    def __repr__(self):
        return f'<User {self.username}>'


class Musician(db.Model):
    """Musician profile"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    outlook_email = db.Column(db.String(120))
    whatsapp = db.Column(db.String(20))
    instruments = db.Column(db.String(200))  # Comma-separated list
    bio = db.Column(db.Text)  # Short bio/about section
    roles = db.Column(db.String(200))  # Comma-separated list of ministry roles
    interests = db.Column(db.String(300))  # Other interesting stuff
    profile_picture = db.Column(db.String(255))  # Path to profile picture
    banner = db.Column(db.String(255))  # Path to banner image
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Friendster-like customization fields
    background_image = db.Column(db.String(255))  # Path to background image
    background_color = db.Column(db.String(50))  # Background color (hex code)
    custom_css = db.Column(db.Text)  # Custom CSS code
    music_player_embed = db.Column(db.Text)  # Music player embed code (iframe/script)
    profile_theme = db.Column(db.String(50), default='default')  # Theme selection
    text_color = db.Column(db.String(50))  # Text color (hex code)
    link_color = db.Column(db.String(50))  # Link color (hex code)
    profile_views = db.Column(db.Integer, default=0)  # Profile view counter
    
    # Relationships
    # Note: User model has backref='user' which creates musician.user automatically
    service_assignments = db.relationship('ServiceMusician', backref='musician', lazy=True, cascade='all, delete-orphan')
    practice_assignments = db.relationship('PracticeMusician', backref='musician', lazy=True, cascade='all, delete-orphan')
    availability = db.relationship('MusicianAvailability', backref='musician', lazy=True, cascade='all, delete-orphan')
    posts = db.relationship('ProfilePost', backref='musician', lazy=True, cascade='all, delete-orphan', order_by='ProfilePost.created_at.desc()')
    
    def get_display_name(self):
        """Get display name - prefer user's nickname, fallback to musician name.
        Also syncs musician.name with user's display name if they differ (without committing)."""
        try:
            if self.user_id and self.user:
                display_name = self.user.get_display_name()
                if display_name:
                    # Sync musician.name with user's display name if they differ
                    if self.name != display_name:
                        self.name = display_name
                    return display_name
        except (AttributeError, Exception):
            # If user relationship doesn't exist or fails, fall back to name
            pass
        return self.name or 'Unknown'
    
    def __repr__(self):
        return f'<Musician {self.name}>'


class ProfilePost(db.Model):
    """Wall posts on musician profiles"""
    id = db.Column(db.Integer, primary_key=True)
    musician_id = db.Column(db.Integer, db.ForeignKey('musician.id'), nullable=False)
    content = db.Column(db.Text)  # Text content of the post
    image_path = db.Column(db.String(255))  # Path to uploaded image
    video_path = db.Column(db.String(255))  # Path to uploaded video
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    likes = db.relationship('PostLike', backref='post', lazy=True, cascade='all, delete-orphan')
    hearts = db.relationship('PostHeart', backref='post', lazy=True, cascade='all, delete-orphan')
    reposts = db.relationship('PostRepost', backref='post', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('PostComment', backref='post', lazy=True, cascade='all, delete-orphan', order_by='PostComment.created_at')
    
    def is_liked_by(self, user_id):
        """Check if post is liked by a specific user"""
        return any(like.user_id == user_id for like in self.likes)
    
    def is_hearted_by(self, user_id):
        """Check if post is hearted by a specific user"""
        return any(heart.user_id == user_id for heart in self.hearts)
    
    def is_reposted_by(self, user_id):
        """Check if post is reposted by a specific user"""
        return any(repost.user_id == user_id for repost in self.reposts)
    
    def __repr__(self):
        return f'<ProfilePost {self.id} by {self.musician_id}>'


class PostLike(db.Model):
    """Likes on profile posts"""
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('profile_post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='post_likes', lazy=True)
    
    # Unique constraint: one like per user per post
    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='unique_post_like'),)
    
    def __repr__(self):
        return f'<PostLike post:{self.post_id} user:{self.user_id}>'


class PostHeart(db.Model):
    """Hearts on profile posts"""
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('profile_post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='post_hearts', lazy=True)
    
    # Unique constraint: one heart per user per post
    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='unique_post_heart'),)
    
    def __repr__(self):
        return f'<PostHeart post:{self.post_id} user:{self.user_id}>'


class PostRepost(db.Model):
    """Reposts of profile posts"""
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('profile_post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='post_reposts', lazy=True)
    
    # Unique constraint: one repost per user per post
    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='unique_post_repost'),)
    
    def __repr__(self):
        return f'<PostRepost post:{self.post_id} user:{self.user_id}>'


class PostComment(db.Model):
    """Comments on profile posts"""
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('profile_post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='post_comments', lazy=True)
    
    def __repr__(self):
        return f'<PostComment {self.id} on post:{self.post_id} by user:{self.user_id}>'


class MusicianAvailability(db.Model):
    """Musician availability/unavailability dates"""
    id = db.Column(db.Integer, primary_key=True)
    musician_id = db.Column(db.Integer, db.ForeignKey('musician.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    is_available = db.Column(db.Boolean, default=True)  # True = available, False = unavailable
    notes = db.Column(db.String(500))  # Optional notes about availability
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint: one record per musician per date
    __table_args__ = (db.UniqueConstraint('musician_id', 'date', name='unique_musician_date'),)
    
    def __repr__(self):
        status = "Available" if self.is_available else "Unavailable"
        return f'<MusicianAvailability {self.musician_id} {self.date} {status}>'


class LeaveRequest(db.Model):
    """Leave requests that require Team Leader approval"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    musician_id = db.Column(db.Integer, db.ForeignKey('musician.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(500), nullable=False)  # Leave reason
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, approved, rejected
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Team Leader who reviewed
    reviewed_at = db.Column(db.DateTime, nullable=True)
    review_notes = db.Column(db.String(500), nullable=True)  # Optional notes from reviewer
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='leave_requests')
    musician = db.relationship('Musician', backref='leave_requests')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by], backref='reviewed_leaves')
    
    def __repr__(self):
        return f'<LeaveRequest {self.id} user:{self.user_id} date:{self.date} status:{self.status}>'


class SundayService(db.Model):
    """Sunday service schedule"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    theme = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='created_services')
    musicians = db.relationship('ServiceMusician', backref='service', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<SundayService {self.date}>'


class ServiceMusician(db.Model):
    """Junction table for service-musician assignments"""
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('sunday_service.id'), nullable=False)
    musician_id = db.Column(db.Integer, db.ForeignKey('musician.id'), nullable=False)
    instrument = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50))  # e.g., 'lead', 'backup', 'vocalist'
    
    def __repr__(self):
        return f'<ServiceMusician service:{self.service_id} musician:{self.musician_id}>'


class Practice(db.Model):
    """Practice session schedule"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time)
    location = db.Column(db.String(200))
    purpose = db.Column(db.String(200))  # Purpose of the practice
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='created_practices')
    musicians = db.relationship('PracticeMusician', backref='practice', lazy=True, cascade='all, delete-orphan')
    songs = db.relationship('PracticeSong', backref='practice', lazy=True, cascade='all, delete-orphan', order_by='PracticeSong.order')
    
    def __repr__(self):
        return f'<Practice {self.date}>'


class PracticeMusician(db.Model):
    """Junction table for practice-musician assignments"""
    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'), nullable=False)
    musician_id = db.Column(db.Integer, db.ForeignKey('musician.id'), nullable=False)
    instrument = db.Column(db.String(50), nullable=False)
    
    # Note: The 'musician' relationship is created automatically by the backref
    # in Musician.practice_assignments relationship
    
    def __repr__(self):
        return f'<PracticeMusician practice:{self.practice_id} musician:{self.musician_id}>'


class Song(db.Model):
    """Song with chord chart reference"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200))
    key = db.Column(db.String(10))  # e.g., 'C', 'G', 'Am'
    gender_key = db.Column(db.String(10))  # 'male' or 'female'
    file_path = db.Column(db.String(500))  # Path to JPG/PNG file
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='created_songs')
    
    def __repr__(self):
        return f'<Song {self.title}>'


class PracticeSong(db.Model):
    """Junction table for practice-song assignments"""
    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=True)  # Nullable for custom songs
    song_name = db.Column(db.String(200), nullable=True)  # Free text entry for songs not in database
    key = db.Column(db.String(20), nullable=True)  # Optional key (e.g., 'C', 'D', 'E', etc.)
    speed = db.Column(db.String(20))  # 'Fast', 'Mid', 'Slow'
    prepared_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    order = db.Column(db.Integer, default=0)  # Order in the lineup
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    song = db.relationship('Song', backref='practice_assignments', lazy=True)
    preparer = db.relationship('User', backref='prepared_lineups', lazy=True)
    
    def get_song_display_name(self):
        """Get the song name - either from song relationship or song_name field"""
        if self.song:
            return self.song.title
        return self.song_name or 'Unknown Song'
    
    def __repr__(self):
        return f'<PracticeSong practice:{self.practice_id} song:{self.song_id or self.song_name}>'


class Slide(db.Model):
    """PowerPoint slide with reference"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200))
    language = db.Column(db.String(20))  # 'english', 'tagalog', 'ilocano', 'others'
    file_type = db.Column(db.String(50))  # 'word', 'excel', 'csv', 'image', 'pdf', 'txt'
    file_path = db.Column(db.String(500))  # Path to file
    description = db.Column(db.Text)  # Description of the job aid
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='created_slides')
    
    def __repr__(self):
        return f'<Slide {self.title}>'


class EventAnnouncement(db.Model):
    """Event announcements for the dashboard"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.Text)  # Optional caption/description
    image_path = db.Column(db.String(255))  # Path to uploaded image/graphic
    is_active = db.Column(db.Boolean, default=True)  # Whether to display on dashboard
    display_order = db.Column(db.Integer, default=0)  # Order for displaying multiple announcements
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='created_announcements')
    
    def __repr__(self):
        return f'<EventAnnouncement {self.title}>'


class Notification(db.Model):
    """Notifications for users"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who receives the notification
    notification_type = db.Column(db.String(50), nullable=False)  # 'like', 'heart', 'share', 'comment', 'practice', 'leave_request'
    actor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who performed the action
    post_id = db.Column(db.Integer, db.ForeignKey('profile_post.id'), nullable=True)  # Related post (if applicable)
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'), nullable=True)  # Related practice (if applicable)
    comment_id = db.Column(db.Integer, db.ForeignKey('post_comment.id'), nullable=True)  # Related comment (if applicable)
    leave_request_id = db.Column(db.Integer, db.ForeignKey('leave_request.id'), nullable=True)  # Related leave request (if applicable)
    is_read = db.Column(db.Boolean, default=False)  # Whether the notification has been read
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='notifications')
    actor = db.relationship('User', foreign_keys=[actor_id], backref='actions')
    post = db.relationship('ProfilePost', backref='notifications')
    practice = db.relationship('Practice', backref='notifications')
    comment = db.relationship('PostComment', backref='notifications')
    leave_request = db.relationship('LeaveRequest', backref='notifications')
    
    def __repr__(self):
        return f'<Notification {self.id} for user:{self.user_id} type:{self.notification_type}>'


class SMSLog(db.Model):
    """SMS sending logs for tracking and auditing"""
    id = db.Column(db.Integer, primary_key=True)
    recipient_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # User who received the SMS
    recipient_phone = db.Column(db.String(20), nullable=False)  # Phone number the SMS was sent to
    recipient_name = db.Column(db.String(200), nullable=True)  # Name of the recipient
    message_type = db.Column(db.String(50), nullable=False)  # 'practice_assignment', 'practice_reminder_day', 'practice_reminder_hour'
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'), nullable=True)  # Related practice (if applicable)
    musician_id = db.Column(db.Integer, db.ForeignKey('musician.id'), nullable=True)  # Related musician (if applicable)
    message_content = db.Column(db.Text)  # The actual message sent
    status = db.Column(db.String(20), nullable=False)  # 'success', 'failed'
    error_message = db.Column(db.Text, nullable=True)  # Error message if failed
    sent_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # User who triggered the SMS (admin/worship leader)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # When the SMS was sent
    
    # Relationships
    recipient_user = db.relationship('User', foreign_keys=[recipient_user_id], backref='received_sms')
    practice = db.relationship('Practice', backref='sms_logs')
    musician = db.relationship('Musician', backref='sms_logs')
    sent_by = db.relationship('User', foreign_keys=[sent_by_user_id], backref='sent_sms')
    
    def __repr__(self):
        return f'<SMSLog {self.id} to:{self.recipient_phone} status:{self.status}>'


class ActivityLog(db.Model):
    """Activity log for tracking app events and milestones"""
    id = db.Column(db.Integer, primary_key=True)
    activity_type = db.Column(db.String(50), nullable=False)  # 'leave_filed', 'leave_approved', 'job_aid_uploaded', 'new_member', etc.
    actor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who performed the action
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Target user (for leave approvals, etc.)
    description = db.Column(db.Text, nullable=False)  # Human-readable description
    extra_data = db.Column(db.Text)  # JSON string for additional data (dates, file names, etc.)
    slide_id = db.Column(db.Integer, db.ForeignKey('slide.id'), nullable=True)  # Related job aid
    leave_request_id = db.Column(db.Integer, db.ForeignKey('leave_request.id'), nullable=True)  # Related leave request
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    actor = db.relationship('User', foreign_keys=[actor_id], backref='activities')
    target_user = db.relationship('User', foreign_keys=[target_user_id])
    slide = db.relationship('Slide', backref='activity_logs')
    leave_request = db.relationship('LeaveRequest', backref='activity_logs')
    
    def __repr__(self):
        return f'<ActivityLog {self.id} type:{self.activity_type} actor:{self.actor_id}>'


class UserPermission(db.Model):
    """Granular permissions for users (managed by admin)"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    permission_type = db.Column(db.String(50), nullable=False)  # 'edit_practices', 'edit_services', 'edit_songs', 'edit_slides', 'edit_announcements', etc.
    granted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Admin who granted the permission
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='permissions')
    grantor = db.relationship('User', foreign_keys=[granted_by], backref='granted_permissions')
    
    # Unique constraint: one permission type per user
    __table_args__ = (db.UniqueConstraint('user_id', 'permission_type', name='unique_user_permission'),)
    
    def __repr__(self):
        return f'<UserPermission user:{self.user_id} permission:{self.permission_type}>'


class Journal(db.Model):
    """Journal entries for users - mood board, prayers, devotion, gospel"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entry_type = db.Column(db.String(50), nullable=False)  # 'mood_board', 'prayer', 'answered_prayer', 'devotion', 'gospel'
    title = db.Column(db.String(200), nullable=True)  # Optional title / Scripture for devotion
    content = db.Column(db.Text, nullable=True)  # Main content / Observation for devotion
    application = db.Column(db.Text, nullable=True)  # Application field for devotion
    prayer_text = db.Column(db.Text, nullable=True)  # Prayer field for devotion
    image_path = db.Column(db.String(255), nullable=True)  # For mood board images
    mood_emojis = db.Column(db.String(500), nullable=True)  # Comma-separated emojis for mood board
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)  # Date of entry
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='journal_entries')
    
    def __repr__(self):
        return f'<Journal {self.id} user:{self.user_id} type:{self.entry_type}>'


class Task(db.Model):
    """Daily tasks for users"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task = db.Column(db.String(500), nullable=False)  # Task description
    priority = db.Column(db.Integer, default=1)  # Priority level (1=high, 2=medium, 3=low)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)  # When task was completed
    task_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)  # Date the task is for
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='tasks')
    
    def __repr__(self):
        return f'<Task {self.id} user:{self.user_id} task:{self.task[:30]} completed:{self.is_completed}>'


class TaskOption(db.Model):
    """Saved task options/templates for users"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_text = db.Column(db.String(500), nullable=False)  # Task description template
    priority = db.Column(db.Integer, default=2)  # Default priority (1=high, 2=medium, 3=low)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='task_options')
    
    def __repr__(self):
        return f'<TaskOption {self.id} user:{self.user_id} task:{self.task_text[:30]}>'


class Tool(db.Model):
    """Tool model for storing work tools with links, descriptions, and screenshots"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)  # Tool name
    link = db.Column(db.String(500), nullable=False)  # Tool URL
    description = db.Column(db.Text)  # Tool description
    screenshot = db.Column(db.String(255))  # Path to screenshot image
    developer_name = db.Column(db.String(200))  # Name of the developer who created the tool
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='tools')
    
    def __repr__(self):
        return f'<Tool {self.id} name:{self.name[:30]}>'


class Message(db.Model):
    """Chat message model for team communication"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # None = group chat, ID = private message
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')
    
    def __repr__(self):
        if self.recipient_id:
            return f'<Message {self.id} from user:{self.user_id} to user:{self.recipient_id}>'
        return f'<Message {self.id} by user:{self.user_id} (group)>'

