from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin, UserManager
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import validators
import logging
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.contrib.auth.models import UserManager

logger = logging.getLogger(__name__)

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Invalid email provided")
        
        email= self.normalize_email(email)
        user= self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)    
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', 'admin')
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model extending Django's AbstractUser"""
    USER_TYPE_CHOICES = (
        ('donor', 'Donor'),
        ('campaign_owner', 'Campaign Owner'),
        ('admin', 'Admin'),
    )
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='donor')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    national_id = models.PositiveBigIntegerField(blank=True, null=True)
    email= models.EmailField(blank=True, 
                             db_index=True,
                             unique=True,
                             validators=[validators.EmailValidator(message="Enter a valid email address.")])
    profile_picture = models.FileField(upload_to='profile/', blank=True, null=True, storage=RawMediaCloudinaryStorage())
    password = models.CharField(max_length=128, blank=True, null=True)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff= models.BooleanField(default=False)
    is_superuser=  models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    objects= CustomUserManager()

    USERNAME_FIELD= 'email'
    EMAIL_FIELD= 'email'
    REQUIRED_FIELDS= []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        unique_together = ('email', 'national_id')
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['user_type']),  # Frequently filtered by role
            models.Index(fields=['is_active']),  # Often used in queries
            models.Index(fields=['phone_number']),  # For time-based queries
        ]

    def __str__(self):
        return f"{self.id} - {self.firstname} {self.lastname} - {self.email}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            if instance.user_type == 'donor':
              from .models import Donor
              Donor.objects.create(user=instance)
            elif instance.user_type == 'campaign_owner':
              from .models import Campaign_Owner
              Campaign_Owner.objects.create(user=instance, 
                                            organization_name= f'{instance.firstname} {instance.lastname}', 
                                            organization_description= f'Organization description for {instance.firstname} {instance.lastname}')
        except Exception as e:
            logger.error(f"Error creating profile for user {instance.email}: {e}")

class Campaign_Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    organization_name = models.CharField(max_length=255)
    organization_description = models.TextField()
    organization_website = models.URLField()
    organization_logo = models.FileField(upload_to='logo/', blank=True, null=True, storage=RawMediaCloudinaryStorage())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname} - {self.organization_name}"
    
class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname}"
