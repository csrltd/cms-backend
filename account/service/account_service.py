from loguru import logger
from rest_framework_simplejwt.tokens import RefreshToken
from base.responses import APIResponse
from account.repository.user_repository import UserRepository


class AccountService:
    def __init__(self):
        self.repository = UserRepository()

    def register_user(self, data):
        try:
            repo_response = self.repository.create_user(data)
            if not repo_response.success:
                return APIResponse(False, repo_response.message, status=400)
            
            user = repo_response.data['user']
            otp_code = repo_response.data.get('otp_code')
            
            # Send OTP email
            if otp_code:
                self.send_otp_email(user, otp_code)
            
            return APIResponse(
                True, 
                "Account created successfully. Please check your email for verification code.",
                {"user_id": user.id, "email": user.email},
                201
            )
        except Exception as e:
            logger.error(f"Error registering user: {str(e)}")
            return APIResponse(False, "Account creation failed", status=500)

    def verify_email(self, email, otp_code):
        try:
            repo_response = self.repository.verify_user_otp(email, otp_code)
            if not repo_response.success:
                return APIResponse(False, repo_response.message, status=400)
            
            # Send welcome email
            self.send_welcome_email(repo_response.data)
            
            # Generate JWT tokens
            tokens = self.generate_jwt_tokens(repo_response.data)
            
            return APIResponse(
                True,
                "Account verified successfully",
                {
                    "user": {
                        "id": repo_response.data.id,
                        "email": repo_response.data.email,
                        "first_name": repo_response.data.first_name,
                        "last_name": repo_response.data.last_name,
                        "user_type": repo_response.data.user_type
                    },
                    "tokens": tokens
                }
            )
        except Exception as e:
            logger.error(f"Error verifying email: {str(e)}")
            return APIResponse(False, "Verification failed", status=500)

    def resend_otp(self, email):
        try:
            repo_response = self.repository.generate_new_otp(email)
            if not repo_response.success:
                return APIResponse(False, repo_response.message, status=400)
            
            user = repo_response.data['user']
            otp_code = repo_response.data.get('otp_code')
            
            # Send new OTP email
            if otp_code:
                self.send_otp_email(user, otp_code)
            
            return APIResponse(True, "Verification code sent")
        except Exception as e:
            logger.error(f"Error resending OTP: {str(e)}")
            return APIResponse(False, "Unable to send verification code", status=500)

    def login_user(self, email, password):
        try:
            repo_response = self.repository.authenticate_user(email, password)
            if not repo_response.success:
                return APIResponse(False, repo_response.message, status=401)
            
            # Generate JWT tokens
            tokens = self.generate_jwt_tokens(repo_response.data)
            
            return APIResponse(
                True,
                "Authentication successful",
                {
                    "user": {
                        "id": repo_response.data.id,
                        "email": repo_response.data.email,
                        "first_name": repo_response.data.first_name,
                        "last_name": repo_response.data.last_name,
                        "user_type": repo_response.data.user_type
                    },
                    "tokens": tokens
                }
            )
        except Exception as e:
            logger.error(f"Error logging in user: {str(e)}")
            return APIResponse(False, "Authentication failed", status=500)

    def send_otp_email(self, user, otp_code):
        """Send OTP email - accepts otp_code as parameter"""
        try:
            from account.tasks import send_otp_email_task
            send_otp_email_task.delay(user.id, otp_code)
        except Exception as e:
            logger.warning(f"Failed to queue OTP email: {str(e)}")

    def send_welcome_email(self, user):
        try:
            from account.tasks import send_welcome_email_task
            send_welcome_email_task.delay(user.id)
        except Exception as e:
            logger.warning(f"Failed to queue welcome email: {str(e)}")

    def generate_jwt_tokens(self, user):
        try:
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        except Exception as e:
            logger.error(f"Error generating JWT tokens: {str(e)}")
            return None