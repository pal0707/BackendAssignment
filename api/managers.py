from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the Django User model.
    
    Provides methods for creating regular users and superusers.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Private method that creates a user with the given email, password, and extra fields.
        
        Args:
            email (str): The email of the user.
            password (str): The password of the user.
            **extra_fields: Additional fields for the user.
        
        Returns:
            User: The created user object.
        
        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates a regular user with the given email, password, and extra fields.
        
        Args:
            email (str): The email of the user.
            password (str, optional): The password of the user. Defaults to None.
            **extra_fields: Additional fields for the user.
        
        Returns:
            User: The created user object.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates a superuser with the given email, password, and extra fields.
        
        Args:
            email (str): The email of the superuser.
            password (str, optional): The password of the superuser. Defaults to None.
            **extra_fields: Additional fields for the superuser.
        
        Returns:
            User: The created superuser object.
        
        Raises:
            ValueError: If is_staff or is_superuser is not set to True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self._create_user(email, password, **extra_fields)
