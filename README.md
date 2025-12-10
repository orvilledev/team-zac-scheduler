# Team Dashboard

A Flask web application for managing musician schedules for Sunday services and practices, with downloadable chord charts.

## Features

- **User Authentication**: Role-based access control (Admin, Worship Leader, Musician)
- **Musician Management**: Add, edit, and manage musician profiles with instruments
- **Sunday Service Scheduling**: Schedule services and assign musicians
- **Practice Scheduling**: Schedule practice sessions separately from services
- **Song Management**: Admin-only song catalog with downloadable chord chart JPG files
- **Dashboard**: Overview of upcoming services, practices, and statistics

## Requirements

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd DCC-PW-SCHEDULER
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the database:**
   The database will be automatically created on first run. The default admin user will be created:
   - Username: `admin`
   - Password: `admin123`
   
   **⚠️ IMPORTANT: Change the default admin password in production!**

6. **Run the application:**
   ```bash
   python app.py
   ```

8. **Access the application:**
   Open your browser and navigate to `http://localhost:5000`

## Usage

### Initial Setup

1. **Login** with the default admin credentials (username: `admin`, password: `admin123`)
2. **Add Musicians** - Go to Musicians page and add all musicians with their instruments
3. **Add Songs** - Upload chord chart JPG files to `static/chords/` directory, then add songs in the Songs page (admin only)
4. **Schedule Services** - Create Sunday service schedules and assign musicians
5. **Schedule Practices** - Create practice sessions and assign musicians

### User Roles

- **Admin**: Full access to all features including song management
- **Worship Leader**: Can manage musicians, services, and practices
- **Musician**: View-only access to schedules

### Adding Chord Charts

1. Place JPG files in the `static/chords/` directory
2. Go to Songs page (admin only)
3. Add a new song and enter the filename in the "Chord File Path" field (e.g., `song_name.jpg`)
4. Users can download chord charts from the Songs page

### Scheduling Musicians

1. Create a Sunday Service or Practice
2. Click "View" to see the detail page
3. Click "Add Musician" to assign musicians
4. Select musician, instrument, and optionally a role
5. Musicians can be removed from schedules as needed

## Project Structure

```
DCC-PW-SCHEDULER/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── forms.py               # WTForms for user input
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── musicians.html
│   ├── services.html
│   ├── practices.html
│   └── songs.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── chords/            # Chord chart JPG files go here
└── instance/
    └── database.db        # SQLite database (created automatically)
```

## Configuration

Edit `config.py` to customize:
- `SECRET_KEY`: Change for production (use environment variable)
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `UPLOAD_FOLDER`: Directory for chord files
- `MAX_CONTENT_LENGTH`: Maximum file upload size

## Security Notes

- Change the default admin password immediately
- Set a strong `SECRET_KEY` in production (use environment variable)
- Consider using PostgreSQL instead of SQLite for production
- Implement proper file upload validation if allowing uploads through the web interface

## Development

To run in development mode with auto-reload:
```bash
python app.py
```

The application runs in debug mode by default. Disable debug mode for production.

## Troubleshooting

- **Database errors**: Delete `instance/database.db` and restart the app to recreate the database
- **Import errors**: Ensure all dependencies are installed: `pip install -r requirements.txt`
- **Port already in use**: Change the port in `app.py` or stop the process using port 5000

## License

This project is for internal use.

