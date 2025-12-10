"""
SMS Service for sending practice notifications via Twilio
"""
import os
from datetime import datetime, timedelta
from flask import current_app

try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False
    print("Warning: Twilio not installed. SMS functionality will be disabled.")


def check_message_status(message_sid):
    """
    Check the current status of a Twilio message
    
    Args:
        message_sid: Twilio message SID
        
    Returns:
        tuple: (status: str, error_code: str or None, error_message: str or None)
    """
    if not TWILIO_AVAILABLE or not message_sid:
        return None, None, None
    
    try:
        account_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
        auth_token = current_app.config.get('TWILIO_AUTH_TOKEN')
        
        if not account_sid or not auth_token:
            return None, None, None
        
        client = Client(account_sid, auth_token)
        message = client.messages(message_sid).fetch()
        
        status = getattr(message, 'status', None)
        error_code = getattr(message, 'error_code', None)
        error_message = getattr(message, 'error_message', None)
        
        return status, error_code, error_message
    except Exception as e:
        print(f"Error checking message status: {e}")
        return None, None, None


def send_sms(to_number, message):
    """
    Send SMS via Twilio using Messaging Service or Phone Number
    
    Args:
        to_number: Phone number in E.164 format (e.g., +1234567890)
        message: Message text to send
    
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    if not current_app.config.get('SMS_ENABLED', False):
        return False, "SMS is not enabled in configuration"
    
    if not TWILIO_AVAILABLE:
        return False, "Twilio library not installed"
    
    account_sid = current_app.config.get('TWILIO_ACCOUNT_SID')
    auth_token = current_app.config.get('TWILIO_AUTH_TOKEN')
    messaging_service_sid = current_app.config.get('TWILIO_MESSAGING_SERVICE_SID', '').strip()
    from_number = current_app.config.get('TWILIO_PHONE_NUMBER')
    
    if not account_sid or not auth_token:
        return False, "Twilio Account SID and Auth Token are required"
    
    # Prefer Messaging Service SID over phone number
    if not messaging_service_sid and not from_number:
        return False, "Either TWILIO_MESSAGING_SERVICE_SID or TWILIO_PHONE_NUMBER must be configured"
    
    try:
        client = Client(account_sid, auth_token)
        
        # Format phone number using the format_phone_number function
        formatted_number = format_phone_number(to_number)
        if not formatted_number:
            return False, f"Invalid phone number format: {to_number}"
        
        # Use Messaging Service SID if available (preferred method)
        if messaging_service_sid and messaging_service_sid.strip():
            # Use Messaging Service (recommended - works better with international numbers)
            message_obj = client.messages.create(
                body=message,
                messaging_service_sid=messaging_service_sid,
                to=formatted_number
            )
        else:
            # Fallback to phone number (may have restrictions on trial accounts)
            if not from_number:
                return False, "TWILIO_PHONE_NUMBER is required when Messaging Service SID is not configured"
            message_obj = client.messages.create(
                body=message,
                from_=from_number,
                to=formatted_number
            )
        
        # Get message SID and status
        message_sid = getattr(message_obj, 'sid', None)
        message_status = getattr(message_obj, 'status', None)
        
        # Check if message was actually accepted (not just queued)
        # Status can be: queued, sending, sent, delivered, undelivered, failed
        # For trial accounts, messages might be queued but not actually sent
        if message_status in ['failed', 'undelivered']:
            error_detail = getattr(message_obj, 'error_message', None) or getattr(message_obj, 'error_code', None)
            return False, f"Twilio message status: {message_status}. {error_detail or 'Message was not delivered.'}", message_sid
        
        # Return success with message SID and status
        # Note: 'sent' means Twilio sent to carrier, but 'delivered' confirms receipt
        return True, None, message_sid, message_status
    except Exception as e:
        error_msg = str(e)
        # Provide more helpful error messages
        if '21612' in error_msg or 'Unable to create record' in error_msg:
            return False, f"Twilio Error: Cannot send to this number. For trial accounts, the recipient number must be verified in your Twilio console. Error details: {error_msg}", None, None
        return False, f"Twilio Error: {error_msg}", None, None


def format_phone_number(phone):
    """
    Format phone number to E.164 format for Philippines
    
    Args:
        phone: Phone number string (various formats)
    
    Returns:
        str: Formatted phone number or None if invalid
    """
    if not phone:
        return None
    
    # Remove all non-digit characters except +
    cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
    
    # If it already starts with +, validate format
    if cleaned.startswith('+'):
        # Remove + temporarily for processing
        digits = cleaned[1:]
    else:
        digits = cleaned
    
    if not digits:
        return None
    
    # Handle Philippines numbers (country code 63)
    if digits.startswith('63'):
        # Already has country code
        if len(digits) == 12:  # +63XXXXXXXXXX (10 digits after country code)
            return '+' + digits
        elif len(digits) == 13:  # +639XXXXXXXXXX (11 digits after country code)
            return '+' + digits
        else:
            return None  # Invalid length
    elif digits.startswith('0'):
        # Remove leading 0 and add country code
        remaining = digits[1:]
        if len(remaining) == 10:  # Standard Philippines mobile (10 digits)
            return '+63' + remaining
        elif len(remaining) == 11:  # Some numbers have 11 digits
            return '+63' + remaining
        else:
            return None
    elif len(digits) == 10:
        # 10-digit number, assume Philippines
        return '+63' + digits
    elif len(digits) == 11:
        # 11-digit number, assume Philippines
        return '+63' + digits
    else:
        # Try to add +63 if it doesn't start with +
        if not cleaned.startswith('+'):
            if len(digits) >= 10:
                return '+63' + digits[-10:] if len(digits) > 10 else '+63' + digits
        return None


def send_practice_assignment_sms(practice, musician, is_new_assignment=True):
    """
    Send SMS notification when a musician is assigned to a practice
    
    Args:
        practice: Practice object
        musician: Musician object
        is_new_assignment: True if newly assigned, False if updated
    """
    user = musician.user if musician.user_id else None
    if not user or not user.mobile_number:
        return False, "User has no mobile number"
    
    phone = format_phone_number(user.mobile_number)
    if not phone:
        return False, "Invalid phone number format"
    
    # Format practice date and time
    date_str = practice.date.strftime('%B %d, %Y') if practice.date else 'TBD'
    time_str = practice.time.strftime('%I:%M %p') if practice.time else 'TBD'
    location_str = practice.location if practice.location else 'TBD'
    
    # Get instrument from assignment
    from models import PracticeMusician
    assignment = PracticeMusician.query.filter_by(
        practice_id=practice.id,
        musician_id=musician.id
    ).first()
    instrument = assignment.instrument if assignment else 'N/A'
    
    if is_new_assignment:
        message = f"Hi {user.get_display_name()}! You've been assigned to a practice session.\n\n"
    else:
        message = f"Hi {user.get_display_name()}! Your practice assignment has been updated.\n\n"
    
    message += f"Date: {date_str}\n"
    message += f"Time: {time_str}\n"
    message += f"Location: {location_str}\n"
    message += f"Instrument: {instrument}\n"
    
    if practice.purpose:
        message += f"Purpose: {practice.purpose}\n"
    
    message += "\nYou'll receive reminders 1 day before and 1 hour before the practice."
    
    result = send_sms(phone, message)
    # Unpack result - handle old (success, error), new (success, error, sid), and latest (success, error, sid, status) formats
    if len(result) == 4:
        return result
    elif len(result) == 3:
        return result[0], result[1], result[2], None  # Add None for status
    else:
        # Old format - add None for message_sid and status
        return result[0], result[1] if len(result) > 1 else None, None, None


def send_practice_reminder_sms(practice, musician, reminder_type='day_before'):
    """
    Send practice reminder SMS
    
    Args:
        practice: Practice object
        musician: Musician object
        reminder_type: 'day_before' or 'hour_before'
    """
    user = musician.user if musician.user_id else None
    if not user or not user.mobile_number:
        return False, "User has no mobile number"
    
    phone = format_phone_number(user.mobile_number)
    if not phone:
        return False, "Invalid phone number format"
    
    # Format practice date and time
    date_str = practice.date.strftime('%B %d, %Y') if practice.date else 'TBD'
    time_str = practice.time.strftime('%I:%M %p') if practice.time else 'TBD'
    location_str = practice.location if practice.location else 'TBD'
    
    # Get instrument from assignment
    from models import PracticeMusician
    assignment = PracticeMusician.query.filter_by(
        practice_id=practice.id,
        musician_id=musician.id
    ).first()
    instrument = assignment.instrument if assignment else 'N/A'
    
    if reminder_type == 'day_before':
        message = f"Reminder: Practice tomorrow!\n\n"
    elif reminder_type == 'hour_before':
        message = f"Reminder: Practice in 1 hour!\n\n"
    else:
        message = f"Reminder: Practice coming up!\n\n"
    
    message += f"Date: {date_str}\n"
    message += f"Time: {time_str}\n"
    message += f"Location: {location_str}\n"
    message += f"Instrument: {instrument}\n"
    
    if practice.purpose:
        message += f"Purpose: {practice.purpose}\n"
    
    message += "\nSee you there!"
    
    result = send_sms(phone, message)
    # Unpack result - handle old (success, error), new (success, error, sid), and latest (success, error, sid, status) formats
    if len(result) == 4:
        return result
    elif len(result) == 3:
        return result[0], result[1], result[2], None  # Add None for status
    else:
        # Old format - add None for message_sid and status
        return result[0], result[1] if len(result) > 1 else None, None, None

