import secrets
from django.utils import timezone
from datetime import timedelta
from loguru import logger
from base.responses import RepositoryResponse
from account.models import OTPToken


class OTPService:
    """
    Service for generating and verifying OTP tokens
    Provides cryptographically secure OTP generation and verification
    with brute force protection and rate limiting.
    """
    
    OTP_LENGTH = 6
    OTP_VALIDITY_MINUTES = 10
    MAX_ATTEMPTS = 5
    RESEND_COOLDOWN_SECONDS = 60  # 1 minute between resends
    
    @staticmethod
    def generate_otp():
        """
        Generate a cryptographically secure 6-digit OTP
        Uses secrets module instead of random for better security
        """
        return ''.join([str(secrets.randbelow(10)) for _ in range(OTPService.OTP_LENGTH)])
    
    @staticmethod
    def create_otp(user, purpose='email_verification'):
        """
        Create a new OTP token for a user
        
        Args:
            user: User instance
            purpose: Purpose of OTP (email_verification, password_reset, etc.)
        
        Returns:
            tuple: (otp_code, OTPToken instance) or (None, None) if failed
        """
        try:
            # Check if there's a recent OTP (prevent spam/abuse)
            recent_otp = OTPToken.objects.filter(
                user=user,
                purpose=purpose,
                created_at__gte=timezone.now() - timedelta(seconds=OTPService.RESEND_COOLDOWN_SECONDS)
            ).first()
            
            if recent_otp:
                logger.warning(f"OTP resend attempted too soon for {user.email} - Purpose: {purpose}")
                return None, None
            
            # Invalidate all previous unused OTPs for this purpose
            # This ensures only one active OTP per purpose
            OTPToken.objects.filter(
                user=user,
                purpose=purpose,
                is_used=False
            ).update(is_used=True)
            
            # Generate new OTP
            otp_code = OTPService.generate_otp()
            token_hash = OTPToken.hash_token(otp_code)
            
            # Create OTP token
            otp_token = OTPToken.objects.create(
                user=user,
                token_hash=token_hash,
                purpose=purpose,
                expires_at=timezone.now() + timedelta(minutes=OTPService.OTP_VALIDITY_MINUTES),
                max_attempts=OTPService.MAX_ATTEMPTS
            )
            
            logger.info(f"OTP created for {user.email} - Purpose: {purpose} - Expires: {otp_token.expires_at}")
            return otp_code, otp_token
            
        except Exception as e:
            logger.error(f"Error creating OTP for {user.email}: {str(e)}")
            return None, None
    
    @staticmethod
    def verify_otp(user, otp_code, purpose='email_verification'):
        """
        Verify an OTP token with brute force protection
        
        Args:
            user: User instance
            otp_code: OTP code to verify
            purpose: Purpose of OTP
        
        Returns:
            RepositoryResponse with success status and message
        """
        try:
            # Get the latest valid OTP for this purpose
            otp_token = OTPToken.objects.filter(
                user=user,
                purpose=purpose,
                is_used=False
            ).order_by('-created_at').first()
            
            if not otp_token:
                logger.warning(f"No valid OTP found for {user.email} - Purpose: {purpose}")
                return RepositoryResponse(
                    success=False,
                    message="No valid OTP found. Please request a new one."
                )
            
            # Check if token is expired
            if timezone.now() > otp_token.expires_at:
                logger.warning(f"Expired OTP attempt for {user.email} - Purpose: {purpose}")
                return RepositoryResponse(
                    success=False,
                    message="OTP has expired. Please request a new one."
                )
            
            # Check if max attempts exceeded
            if otp_token.attempts >= otp_token.max_attempts:
                logger.warning(f"Max attempts exceeded for {user.email} - Purpose: {purpose}")
                return RepositoryResponse(
                    success=False,
                    message="Maximum verification attempts exceeded. Please request a new OTP."
                )
            
            # Verify the token
            if otp_token.verify_token(otp_code):
                # Mark as used
                otp_token.mark_as_used()
                logger.info(f"OTP verified successfully for {user.email} - Purpose: {purpose}")
                return RepositoryResponse(
                    success=True,
                    message="OTP verified successfully",
                    data=otp_token
                )
            else:
                # Increment attempts
                otp_token.increment_attempts()
                remaining_attempts = otp_token.max_attempts - otp_token.attempts
                
                logger.warning(
                    f"Invalid OTP attempt for {user.email} - Purpose: {purpose} - "
                    f"Attempts: {otp_token.attempts}/{otp_token.max_attempts}"
                )
                
                if remaining_attempts > 0:
                    return RepositoryResponse(
                        success=False,
                        message=f"Invalid OTP. {remaining_attempts} attempt(s) remaining."
                    )
                else:
                    return RepositoryResponse(
                        success=False,
                        message="Maximum attempts exceeded. Please request a new OTP."
                    )
                    
        except Exception as e:
            logger.error(f"Error verifying OTP for {user.email}: {str(e)}")
            return RepositoryResponse(
                success=False,
                message="OTP verification failed"
            )
    
    @staticmethod
    def cleanup_expired_otps():
        """
        Delete expired and used OTP tokens
        Should be run as a periodic task (e.g., daily or every few hours)
        
        Returns:
            int: Number of deleted tokens
        """
        try:
            # Delete expired tokens
            expired_count = OTPToken.objects.filter(
                expires_at__lt=timezone.now()
            ).delete()[0]
            
            # Delete old used tokens (older than 7 days)
            old_used_count = OTPToken.objects.filter(
                is_used=True,
                used_at__lt=timezone.now() - timedelta(days=7)
            ).delete()[0]
            
            total_deleted = expired_count + old_used_count
            
            logger.info(
                f"Cleaned up {total_deleted} OTP tokens "
                f"({expired_count} expired, {old_used_count} old used)"
            )
            return total_deleted
        except Exception as e:
            logger.error(f"Error cleaning up OTPs: {str(e)}")
            return 0
    
    @staticmethod
    def get_user_otp_stats(user):
        """
        Get OTP statistics for a user (useful for monitoring/debugging)
        
        Args:
            user: User instance
        
        Returns:
            dict: Statistics about user's OTP usage
        """
        try:
            total_otps = OTPToken.objects.filter(user=user).count()
            active_otps = OTPToken.objects.filter(user=user, is_used=False, expires_at__gt=timezone.now()).count()
            failed_attempts = OTPToken.objects.filter(
                user=user,
                attempts__gte=OTPToken.objects.filter(user=user).first().max_attempts if total_otps > 0 else 5
            ).count()
            
            return {
                'total_otps_generated': total_otps,
                'active_otps': active_otps,
                'failed_verification_count': failed_attempts
            }
        except Exception as e:
            logger.error(f"Error getting OTP stats for {user.email}: {str(e)}")
            return {}
