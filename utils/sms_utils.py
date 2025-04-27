import os
import streamlit as st
from twilio.rest import Client

def get_twilio_client():
    """
    Get Twilio client instance with credentials from session state or environment.
    
    Returns:
        Twilio Client instance
    """
    # Check if Twilio credentials are in session state
    account_sid = st.session_state.get('twilio_account_sid') or os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = st.session_state.get('twilio_auth_token') or os.environ.get('TWILIO_AUTH_TOKEN')
    
    if not account_sid or not auth_token:
        raise ValueError("Twilio credentials not found. Please configure Twilio integration.")
    
    return Client(account_sid, auth_token)

def send_twilio_message(to_phone_number, message):
    """
    Send SMS message using Twilio.
    
    Args:
        to_phone_number: Recipient phone number (with country code)
        message: Message text
    
    Returns:
        Twilio message SID
    """
    client = get_twilio_client()
    
    # Get Twilio phone number from session state or environment
    from_phone_number = st.session_state.get('twilio_phone_number') or os.environ.get('TWILIO_PHONE_NUMBER')
    
    if not from_phone_number:
        raise ValueError("Twilio phone number not found. Please configure Twilio integration.")
    
    # Send the message
    twilio_message = client.messages.create(
        body=message,
        from_=from_phone_number,
        to=to_phone_number
    )
    
    return twilio_message.sid

def configure_twilio_from_session():
    """
    Configure Twilio with credentials from session state.
    
    Returns:
        Boolean indicating if Twilio is configured
    """
    account_sid = st.session_state.get('twilio_account_sid')
    auth_token = st.session_state.get('twilio_auth_token')
    phone_number = st.session_state.get('twilio_phone_number')
    
    if account_sid and auth_token and phone_number:
        # Set environment variables for Twilio
        os.environ['TWILIO_ACCOUNT_SID'] = account_sid
        os.environ['TWILIO_AUTH_TOKEN'] = auth_token
        os.environ['TWILIO_PHONE_NUMBER'] = phone_number
        return True
    
    # Check if environment variables are set
    if (os.environ.get('TWILIO_ACCOUNT_SID') and 
        os.environ.get('TWILIO_AUTH_TOKEN') and 
        os.environ.get('TWILIO_PHONE_NUMBER')):
        return True
    
    return False

def check_twilio_configuration():
    """
    Check if Twilio is configured and test connection.
    
    Returns:
        Tuple of (is_configured, error_message)
    """
    try:
        is_configured = configure_twilio_from_session()
        
        if not is_configured:
            return False, "Twilio credentials not configured"
        
        # Test the connection by initializing the client
        client = get_twilio_client()
        return True, None
    
    except Exception as e:
        return False, str(e)