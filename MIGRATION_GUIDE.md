# Migration Guide: Breaking app.py into Blueprints

This guide explains how to complete the migration from the monolithic `app.py` to the blueprint-based architecture.

## Current Status

✅ **Completed:**
- Created blueprint structure (`app/blueprints/`)
- Created services directory (`app/services/`)
- Created utilities (`app/utils/`)
- Moved SMS service to `app/services/`
- Created application factory (`app/__init__.py`)
- Added Flask-Migrate to requirements
- Added Redis/Celery to requirements
- Added Flask-Caching to requirements
- Created Gunicorn configuration
- Created Nginx configuration
- Created deployment guide

⏳ **Still Needed:**
- Move routes from `app.py` to individual blueprints
- Update imports in all blueprint files
- Test all routes after migration

## Blueprint Organization

Routes should be organized into these blueprints:

1. **`auth.py`** - ✅ Created
   - `/login`
   - `/logout`

2. **`main.py`** - ✅ Created
   - `/` (redirects to dashboard)
   - `/dashboard`

3. **`musicians.py`** - ⏳ Needs routes from app.py
   - `/musicians/*` routes

4. **`services.py`** - ⏳ Needs routes from app.py
   - `/services/*` routes

5. **`practices.py`** - ⏳ Needs routes from app.py
   - `/practices/*` routes

6. **`songs.py`** - ⏳ Needs routes from app.py
   - `/songs/*` routes

7. **`slides.py`** - ⏳ Needs routes from app.py
   - `/slides/*` routes

8. **`notifications.py`** - ⏳ Needs routes from app.py
   - `/notifications/*` routes
   - `/notifications-page`

9. **`announcements.py`** - ⏳ Needs routes from app.py
   - `/announcements/*` routes

10. **`users.py`** - ⏳ Needs routes from app.py
    - `/users/*` routes
    - `/users/<id>/availability`

11. **`permissions.py`** - ⏳ Needs routes from app.py
    - `/permissions`

12. **`journal.py`** - ⏳ Needs routes from app.py
    - `/journal/*` routes

13. **`sms.py`** - ⏳ Needs routes from app.py
    - `/sms-success`
    - `/sms-logs`

14. **`api.py`** - ⏳ Needs routes from app.py
    - `/api/*` routes

## Steps to Complete Migration

### 1. Create Blueprint Files

Each blueprint file should follow this pattern:

```python
from flask import Blueprint
from app.utils.decorators import admin_required, worship_leader_required

bp = Blueprint('blueprint_name', __name__)

@bp.route('/route')
@login_required
def function_name():
    # Route logic here
    pass
```

### 2. Move Routes from app.py

For each route in `app.py`:
- Identify which blueprint it belongs to
- Move the route function to that blueprint
- Update `@app.route` to `@bp.route`
- Update imports to use blueprint context
- Update `url_for()` calls to use blueprint prefix (e.g., `url_for('auth.login')`)

### 3. Update Templates

In templates, update all `url_for()` calls:
- `url_for('login')` → `url_for('auth.login')`
- `url_for('dashboard')` → `url_for('main.dashboard')`
- etc.

### 4. Update Forms and Models Imports

Ensure all blueprints import from:
- `from models import ...`
- `from forms import ...`
- `from app.services.sms_service import ...`

### 5. Test Each Blueprint

After moving routes:
1. Start the application: `python run.py`
2. Test each route to ensure it works
3. Check for broken `url_for()` references
4. Verify database operations work correctly

## Common Issues

### Import Errors
- Make sure all blueprint files import necessary modules
- Use relative imports where appropriate: `from ..models import ...`

### Template Not Found
- Check that template paths are correct
- Templates should remain in `templates/` directory

### Database Issues
- Ensure `db` is imported correctly: `from models import db`
- Use `db.session` for database operations

### CSRF Token Issues
- CSRF protection is initialized in `app/__init__.py`
- Should work automatically for all routes

## Next Steps

1. Create stub files for remaining blueprints
2. Gradually move routes from `app.py` to blueprints
3. Test after each migration
4. Update `app.py` to be minimal (just create_app if needed)
5. Remove old `app.py` once migration is complete

## Example: Moving a Route

**Before (in app.py):**
```python
@app.route('/practices')
@login_required
def practices():
    practices_list = Practice.query.all()
    return render_template('practices.html', practices=practices_list)
```

**After (in app/blueprints/practices.py):**
```python
from flask import Blueprint, render_template
from flask_login import login_required
from models import Practice

bp = Blueprint('practices', __name__)

@bp.route('/')
@login_required
def index():
    practices_list = Practice.query.all()
    return render_template('practices.html', practices=practices_list)
```

**Template update:**
```html
<!-- Before -->
<a href="{{ url_for('practices') }}">Practices</a>

<!-- After -->
<a href="{{ url_for('practices.index') }}">Practices</a>
```

