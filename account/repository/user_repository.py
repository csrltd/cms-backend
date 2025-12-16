from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
import random
from loguru import logger
from base.responses import RepositoryResponse
from account.models import User


class UserRepository:
    def create_user(self, data):
        try:
            # Generate OTP
            otp_code = str(random.randint(100000, 999999))
            otp_expires_at = timezone.now() + timedelta(minutes=10)
            
            user = User.objects.create_user(
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password'],
                user_type=data.get('user_type', 'user'),
                is_verified=False,
                otp_code=otp_code,
                otp_expires_at=otp_expires_at
            )
            return RepositoryResponse(
                success=True,
                message="User created successfully",
                data=user
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
            
            if user.otp_code != otp_code:
                return RepositoryResponse(
                    success=False,
                    message="Invalid OTP code"
                )
            
            if user.otp_expires_at < timezone.now():
                return RepositoryResponse(
                    success=False,
                    message="OTP code expired"
                )
            
            user.is_verified = True
            user.otp_code = None
            user.otp_expires_at = None
            user.save()
            
            return RepositoryResponse(
                success=True,
                message="User verified successfully",
                data=user
            )
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
            
            otp_code = str(random.randint(100000, 999999))
            otp_expires_at = timezone.now() + timedelta(minutes=10)
            
            user.otp_code = otp_code
            user.otp_expires_at = otp_expires_at
            user.save()
            
            return RepositoryResponse(
                success=True,
                message="New OTP generated successfully",
                data=user
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