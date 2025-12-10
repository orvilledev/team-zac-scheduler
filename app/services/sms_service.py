"""
SMS Service - Disabled (Twilio removed)
"""
from flask import current_app


def check_message_status(message_sid):
    """
    Check the current status of a message (disabled)
    
    Returns:
        tuple: (None, None, None)
    """
    return None, None, None


def send_sms(to_number, message):
    """
    Send SMS (disabled - Twilio removed)
    
    Returns:
        tuple: (False, "SMS functionality has been disabled", None, None)
    """
    return False, "SMS functionality has been disabled", None, None


def format_phone_number(phone):
    """
    Format phone number to E.164 format
    
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
        digits = cleaned[1:]
    else:
        digits = cleaned
    
    if not digits:
        return None
    
    # Handle Philippines numbers (country code 63)
    if digits.startswith('63'):
        if len(digits) == 12 or len(digits) == 13:
            return '+' + digits
        else:
            return None
    elif digits.startswith('0'):
        remaining = digits[1:]
        if len(remaining) == 10 or len(remaining) == 11:
            return '+63' + remaining
        else:
            return None
    elif len(digits) == 10 or len(digits) == 11:
        return '+63' + digits
    else:
        if not cleaned.startswith('+'):
            if len(digits) >= 10:
                return '+63' + digits[-10:] if len(digits) > 10 else '+63' + digits
        return None


def send_practice_assignment_sms(practice, musician, is_new_assignment=True):
    """
    Send SMS notification when a musician is assigned to a practice (disabled)
    
    Returns:
        tuple: (False, "SMS functionality has been disabled", None, None)
    """
    return False, "SMS functionality has been disabled", None, None


def send_practice_reminder_sms(practice, musician, reminder_type='day_before'):
    """
    Send practice reminder SMS (disabled)
    
    Returns:
        tuple: (False, "SMS functionality has been disabled", None, None)
    """
    return False, "SMS functionality has been disabled", None, None
