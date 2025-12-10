from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional

from config import Config

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Optional()])  # Optional - passwords disabled
    submit = SubmitField('Login')


class MusicianForm(FlaskForm):
    """Form for creating/editing musicians"""
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    mobile = StringField('Mobile', validators=[Optional(), Length(max=20)])
    outlook_email = StringField('Outlook Email', validators=[Optional(), Email(), Length(max=120)])
    whatsapp = StringField('WhatsApp', validators=[Optional(), Length(max=20)])
    instruments = SelectField('Role', validators=[Optional()],
                             choices=[
                                 ('', 'Select Role...'),
                                 ('case_manager', 'Case Manager'),
                                 ('shipment_coordinator', 'Shipment Coordinator'),
                                 ('data_analyst', 'Data Analyst'),
                                 ('team_leader', 'Team Leader')
                             ],
                             description='Case Manager: Manages customer cases, resolves issues, and ensures customer satisfaction. | Shipment Coordinator: Coordinates shipping operations, tracks packages, and manages logistics. | Data Analyst: Analyzes inventory data, sales trends, and generates reports. | Team Leader: Oversees team operations, coordinates workflows, and ensures productivity.')
    bio = TextAreaField('Bio / About Me', validators=[Optional(), Length(max=500)],
                       description='A short introduction about yourself')
    interests = StringField('Interests & Hobbies', validators=[Optional(), Length(max=300)],
                           description='Other interesting things about you')
    profile_picture = FileField('Profile Picture', validators=[Optional(), FileAllowed(Config.ALLOWED_IMAGE_EXTENSIONS, 'Images only!')],
                               description='Upload a profile picture (JPG, PNG)')
    banner = FileField('Banner Image', validators=[Optional(), FileAllowed(Config.ALLOWED_IMAGE_EXTENSIONS, 'Images only!')],
                      description='Upload a banner image (JPG, PNG)')
    submit = SubmitField('Save Changes')


class ProfileCustomizationForm(FlaskForm):
    """Form for Friendster-like profile customization"""
    background_color = StringField('Background Color', validators=[Optional(), Length(max=50)],
                                  description='Hex color code (e.g., #FFFFFF) or color name')
    text_color = StringField('Text Color', validators=[Optional(), Length(max=50)],
                            description='Hex color code for text (e.g., #000000)')
    link_color = StringField('Link Color', validators=[Optional(), Length(max=50)],
                            description='Hex color code for links (e.g., #0066CC)')
    profile_theme = SelectField('Profile Theme', validators=[Optional()],
                               choices=[
                                   ('default', 'Default'),
                                   ('dark', 'Dark Mode'),
                                   ('colorful', 'Colorful'),
                                   ('minimal', 'Minimal'),
                                   ('vintage', 'Vintage'),
                                   ('modern', 'Modern')
                               ])
    music_player_embed = TextAreaField('Music Player Embed Code', validators=[Optional()],
                                      description='Paste embed code from YouTube, Spotify, SoundCloud, etc.')
    custom_css = TextAreaField('Custom CSS', validators=[Optional()],
                              description='Add your own CSS to customize your profile further')
    submit = SubmitField('Save Customization')


class ProfilePostForm(FlaskForm):
    """Form for creating wall posts"""
    content = TextAreaField('What\'s on your mind?', validators=[Optional(), Length(max=1000)],
                           description='Share your thoughts, updates, or experiences')
    image = FileField('Upload Image', validators=[Optional(), FileAllowed(Config.ALLOWED_IMAGE_EXTENSIONS, 'Images only!')],
                     description='Upload an image (JPG, PNG, GIF)')
    video = FileField('Upload Video', validators=[Optional(), FileAllowed(Config.ALLOWED_VIDEO_EXTENSIONS, 'Videos only!')],
                    description='Upload a video (MP4, MOV, AVI)')
    submit = SubmitField('Post')


class PostCommentForm(FlaskForm):
    """Form for commenting on posts"""
    content = TextAreaField('Write a comment...', validators=[DataRequired(), Length(max=500)],
                           description='Share your thoughts')
    submit = SubmitField('Comment')


class ServiceForm(FlaskForm):
    """Form for creating/editing Sunday services"""
    date = StringField('Date', validators=[DataRequired()], description='YYYY-MM-DD format')
    theme = StringField('Theme', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Save Service')


class PracticeForm(FlaskForm):
    """Form for creating/editing practices"""
    date = StringField('Date', validators=[DataRequired()], description='YYYY-MM-DD format')
    time = StringField('Time', validators=[Optional()], description='HH:MM format (24-hour)')
    location = StringField('Location', validators=[Optional(), Length(max=200)])
    purpose = StringField('Purpose', validators=[Optional(), Length(max=200)])
    notes = TextAreaField('Notes', validators=[Optional()], description='Additional notes about the practice')
    submit = SubmitField('Save Practice')


class ServiceMusicianForm(FlaskForm):
    """Form for adding musicians to services"""
    musician_id = StringField('Musician', validators=[DataRequired()])
    instrument = StringField('Instrument', validators=[DataRequired(), Length(max=50)])
    role = StringField('Role', validators=[Optional(), Length(max=50)])
    submit = SubmitField('Add Musician')


class PracticeMusicianForm(FlaskForm):
    """Form for adding musicians to practices"""
    musician_id = SelectField('Musician', validators=[DataRequired()], choices=[])
    instrument = StringField('Instrument', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Add Musician')


class UserForm(FlaskForm):
    """Form for creating/editing users"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[Optional(), Length(min=6, max=128)],
                           description='Leave blank to keep current password or set default "password123"')
    nickname = StringField('Nickname', validators=[Optional(), Length(max=100)],
                          description='Display name throughout the app')
    mobile_number = StringField('Mobile Number', validators=[Optional(), Length(max=20)])
    role = SelectField('Role', validators=[DataRequired()],
                     choices=[
                         ('', 'Select Role...'),
                         ('admin', 'Admin'),
                         ('case_manager', 'Case Manager'),
                         ('shipment_coordinator', 'Shipment Coordinator'),
                         ('data_analyst', 'Data Analyst'),
                         ('team_leader', 'Team Leader')
                     ])
    submit = SubmitField('Save User')
    
    def validate_password_length(self, field):
        """Custom validator to handle optional passwords"""
        if field.data and len(field.data.strip()) > 0 and len(field.data.strip()) < 6:
            raise ValidationError('Password must be at least 6 characters long.')


class SlideForm(FlaskForm):
    """Form for creating/editing slides"""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    artist = SelectField('Contributor', validators=[Optional()], choices=[], coerce=str)
    description = TextAreaField('Description', validators=[Optional()], 
                               description='Description of the job aid')
    file_type = SelectField('File Type', validators=[Optional()],
                           choices=[
                               ('', 'Select File Type...'),
                               ('word', 'Word'),
                               ('excel', 'Excel'),
                               ('csv', 'CSV'),
                               ('image', 'Image'),
                               ('pdf', 'PDF'),
                               ('txt', 'Txt'),
                               ('powerpoint', 'PowerPoint')
                           ],
                           description='Select the type of file')
    slide_file = FileField('Upload File', validators=[Optional(), FileAllowed(Config.ALLOWED_SLIDE_EXTENSIONS, 'Invalid file type!')],
                          description='Upload a file (Word, Excel, CSV, PowerPoint, PDF, TXT, Images)')
    file_path = StringField('File Path (if already uploaded)', validators=[Optional(), Length(max=255)],
                           description='Leave blank if uploading new file')
    submit = SubmitField('Save File')


class EventAnnouncementForm(FlaskForm):
    """Form for creating/editing event announcements"""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)],
                       description='Title for the event announcement')
    caption = TextAreaField('Caption', validators=[Optional(), Length(max=500)],
                           description='Optional caption or description text')
    image = FileField('Upload Graphic/Image', validators=[Optional(), FileAllowed(Config.ALLOWED_IMAGE_EXTENSIONS, 'Images only!')],
                     description='Upload an image or graphic (JPG, PNG, GIF)')
    display_order = StringField('Display Order', validators=[Optional()],
                              description='Lower numbers appear first (default: 0)')
    is_active = SelectField('Status', validators=[DataRequired()],
                           choices=[
                               ('True', 'Active (Show on dashboard)'),
                               ('False', 'Inactive (Hide from dashboard)')
                           ])
    submit = SubmitField('Save Announcement')


class PermissionForm(FlaskForm):
    """Form for managing user permissions"""
    user_id = SelectField('User', validators=[DataRequired()], coerce=int,
                         description='Select a user to manage permissions for')
    edit_slides = BooleanField('Edit Job Aids', default=False,
                             description='Allow user to edit job aids')
    edit_announcements = BooleanField('Edit Announcements', default=False,
                                    description='Allow user to edit announcements')
    submit = SubmitField('Save Permissions')


class JournalForm(FlaskForm):
    """Form for creating/editing journal entries"""
    entry_type = SelectField('Entry Type', validators=[DataRequired()],
                            choices=[
                                ('mood_board', 'Mood Board')
                            ], description='Select the type of journal entry')
    title = StringField('Title', validators=[Optional(), Length(max=200)],
                       description='Optional title for this entry')
    content = TextAreaField('Content', validators=[Optional()],
                           description='Write your thoughts, prayers, or notes here')
    application = TextAreaField('Application', validators=[Optional()],
                               description='Application (for Daily Devotion)')
    prayer_text = TextAreaField('Prayer', validators=[Optional()],
                               description='Prayer (for Daily Devotion)')
    image = FileField('Image (for Mood Board)', validators=[Optional(), FileAllowed(Config.ALLOWED_IMAGE_EXTENSIONS, 'Images only!')],
                     description='Upload an image for mood board entries')
    mood_emojis = StringField('Mood Emojis', validators=[Optional()],
                              description='Selected emojis will appear here (for Mood Board only)')
    date = StringField('Date', validators=[DataRequired()],
                      description='Date for this entry (YYYY-MM-DD)')
    submit = SubmitField('Save Entry')


class ToolForm(FlaskForm):
    """Form for creating/editing tools"""
    name = StringField('Tool Name', validators=[DataRequired(), Length(max=200)],
                      description='Name of the tool')
    link = StringField('Tool Link', validators=[DataRequired(), Length(max=500)],
                      description='URL or link to the tool')
    description = TextAreaField('Description', validators=[Optional()],
                               description='Description of what the tool is used for')
    screenshot = FileField('Screenshot', validators=[Optional(), FileAllowed(Config.ALLOWED_IMAGE_EXTENSIONS, 'Images only!')],
                          description='Upload a screenshot of the tool (JPG, PNG, GIF)')
    developer_name = StringField('Developer Name', validators=[Optional(), Length(max=200)],
                                description='Name of the person who developed this tool')
    submit = SubmitField('Save Tool')