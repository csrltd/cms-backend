from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from base.models import BaseModel
import hashlib


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    USER_TYPES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()

    def __str__(self):
        return self.email


class OTPToken(BaseModel):
    """
    Stores OTP tokens for various purposes (email verification, password reset, etc.)
    Uses hashed tokens for security and tracks verification attempts.
    """
    PURPOSE_CHOICES = (
        ('email_verification', 'Email Verification'),
        ('password_reset', 'Password Reset'),
        ('two_factor', 'Two Factor Authentication'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_tokens')
    token_hash = models.CharField(max_length=64, help_text='SHA-256 hash of OTP')
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0, help_text='Number of verification attempts')
    max_attempts = models.IntegerField(default=5, help_text='Maximum allowed attempts')
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'account_otp_tokens'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'purpose', 'is_used']),
            models.Index(fields=['expires_at']),
        ]
        verbose_name = 'OTP Token'
        verbose_name_plural = 'OTP Tokens'
    
    def __str__(self):
        return f"{self.user.email} - {self.purpose} - {self.created_at}"
    
    @staticmethod
    def hash_token(token):
        """Hash the OTP token using SHA-256"""
        return hashlib.sha256(token.encode()).hexdigest()
    
    def verify_token(self, token):
        """Verify if the provided token matches the stored hash"""
        return self.token_hash == self.hash_token(token)
    
    def is_valid(self):
        """Check if token is still valid"""
        return (
            not self.is_used and
            self.attempts < self.max_attempts and
            timezone.now() < self.expires_at
        )
    
    def increment_attempts(self):
        """Increment verification attempts"""
        self.attempts += 1
        self.save(update_fields=['attempts'])
    
    def mark_as_used(self):
        """Mark token as used"""
        self.is_used = True
        self.used_at = timezone.now()
        self.save(update_fields=['is_used', 'used_at'])