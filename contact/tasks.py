from celery import shared_task
from django.conf import settings
from loguru import logger
import requests


@shared_task
def send_email_notification_task(full_name, email, subject, message):
    """Send email notification via Postmark when contact form is submitted"""
    try:
        postmark_api_key = getattr(settings, 'POSTMARK_API_KEY', None)
        if not postmark_api_key:
            logger.error("POSTMARK_API_KEY not configured")
            return False

        # Postmark API endpoint
        url = "https://api.postmarkapp.com/email"
        
        # Get email addresses from settings
        from_email = getattr(settings, 'FROM_EMAIL', 'noreply@yourdomain.com')
        admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@yourdomain.com')
        
        # Email data
        email_data = {
            "From": from_email,
            "To": admin_email,
            "Subject": f"New Contact Form Submission: {subject}",
            "TextBody": f"""
New contact form submission received:

Name: {full_name}
Email: {email}
Subject: {subject}

Message:
{message}
            """.strip()
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": postmark_api_key
        }
        
        response = requests.post(url, json=email_data, headers=headers)
        
        if response.status_code == 200:
            logger.info(f"Email notification sent successfully for contact from {email}")
            return True
        else:
            logger.error(f"Failed to send email notification: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending email notification: {str(e)}")
        return False