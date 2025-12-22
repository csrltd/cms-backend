from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from loguru import logger
from base.responses import RepositoryResponse
from account.models import User
from account.service.otp_service import OTPService


class UserRepository:
    def create_user(self, data):
        try:
            # Create user without OTP fields
            user = User.objects.create_user(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password'],
                user_type=data.get('user_type', 'user'),
                is_verified=False
            )
            
            # Generate OTP using OTP service
            otp_code, otp_token = OTPService.create_otp(user, 'email_verification')
            
            if not otp_code:
                # If OTP creation failed, still return user but log warning
                logger.warning(f"Failed to create OTP for {user.email}")
            
            return RepositoryResponse(
                success=True,
                message="User created successfully",
                data={'user': user, 'otp_code': otp_code}
            )
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to create user: {str(e)}"
            )

    def verify_user_otp(self, email, otp_code):
        try:
            user = User.objects.get(email=email)
            
            if user.is_verified:
                return RepositoryResponse(
                    success=False,
                    message="User already verified"
                )
            
            # Use OTP service to verify
            otp_response = OTPService.verify_otp(user, otp_code, 'email_verification')
            
            if otp_response.success:
                # Mark user as verified
                user.is_verified = True
                user.save(update_fields=['is_verified'])
                
                return RepositoryResponse(
                    success=True,
                    message="User verified successfully",
                    data=user
                )
            else:
                return otp_response
                
        except User.DoesNotExist:
            return RepositoryResponse(
                success=False,
                message="User not found"
            )
        except Exception as e:
            logger.error(f"Error verifying user OTP: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to verify OTP: {str(e)}"
            )

    def generate_new_otp(self, email):
        try:
            user = User.objects.get(email=email)
            
            if user.is_verified:
                return RepositoryResponse(
                    success=False,
                    message="User already verified"
                )
            
            # Generate new OTP using OTP service
            otp_code, otp_token = OTPService.create_otp(user, 'email_verification')
            
            if not otp_code:
                return RepositoryResponse(
                    success=False,
                    message="Please wait before requesting a new OTP"
                )
            
            return RepositoryResponse(
                success=True,
                message="New OTP generated successfully",
                data={'user': user, 'otp_code': otp_code}
            )
        except User.DoesNotExist:
            return RepositoryResponse(
                success=False,
                message="User not found"
            )
        except Exception as e:
            logger.error(f"Error generating new OTP: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Failed to generate new OTP: {str(e)}"
            )

    def authenticate_user(self, email, password):
        try:
            user = authenticate(username=email, password=password)
            if user is None:
                return RepositoryResponse(
                    success=False,
                    message="Invalid credentials"
                )
            
            if not user.is_verified:
                return RepositoryResponse(
                    success=False,
                    message="Please verify your email first"
                )
            
            return RepositoryResponse(
                success=True,
                message="User authenticated successfully",
                data=user
            )
        except Exception as e:
            logger.error(f"Error authenticating user: {str(e)}")
            return RepositoryResponse(
                success=False,
                message=f"Authentication failed: {str(e)}"
            )