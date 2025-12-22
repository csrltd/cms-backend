from celery import shared_task
from loguru import logger
from django.conf import settings
import requests
from account.models import User


@shared_task
def send_otp_email_task(user_id, otp_code):
    try:
        user = User.objects.get(id=user_id)
        
        if not settings.POSTMARK_API_KEY:
            logger.warning("POSTMARK_API_KEY not configured, skipping email")
            return
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Postmark-Server-Token': settings.POSTMARK_API_KEY
        }
        
        data = {
            'From': settings.FROM_EMAIL,
            'To': user.email,
            'Subject': 'Verify Your Email - CMS Backend',
            'TextBody': f'''
Hello {user.first_name},

Thank you for registering with CMS Backend!

Your verification code is: {otp_code}

This code will expire in 10 minutes.

Best regards,
CMS Backend Team
            '''.strip()
        }
        
        response = requests.post(
            'https://api.postmarkapp.com/email',
            json=data,
            headers=headers
        )
        
        if response.status_code == 200:
            logger.info(f"OTP email sent successfully to {user.email}")
        else:
            logger.error(f"Failed to send OTP email: {response.text}")
            
    except Exception as e:
        logger.error(f"Error sending OTP email: {str(e)}")


@shared_task
def send_welcome_email_task(user_id):
    try:
        user = User.objects.get(id=user_id)
        
        if not settings.POSTMARK_API_KEY:
            logger.warning("POSTMARK_API_KEY not configured, skipping email")
            return
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Postmark-Server-Token': settings.POSTMARK_API_KEY
        }
        
        data = {
            'From': settings.FROM_EMAIL,
            'To': user.email,
            'Subject': 'Welcome to CMS Backend!',
            'TextBody': f'''
Hello {user.first_name},

Welcome to CMS Backend! Your email has been successfully verified.

You can now log in and start using our platform.

Best regards,
CMS Backend Team
            '''.strip()
        }
        
        response = requests.post(
            'https://api.postmarkapp.com/email',
            json=data,
            headers=headers
        )
        
        if response.status_code == 200:
            logger.info(f"Welcome email sent successfully to {user.email}")
        else:
            logger.error(f"Failed to send welcome email: {response.text}")
            
    except Exception as e:
        logger.error(f"Error sending welcome email: {str(e)}")


@shared_task
def cleanup_expired_otps():
    """
    Periodic task to clean up expired and old used OTP tokens
    Should be run daily or every few hours via Celery Beat
    """
    try:
        from account.service.otp_service import OTPService
        deleted_count = OTPService.cleanup_expired_otps()
        logger.info(f"OTP cleanup task completed: {deleted_count} tokens deleted")
        return deleted_count
    except Exception as e:
        logger.error(f"Error in OTP cleanup task: {str(e)}")
        return 0