from django.db import models
from api.managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken

class User(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model that represents a user in the system.

    Inherits from the `AbstractBaseUser` and `PermissionsMixin` classes provided by Django.
    Defines fields and methods related to user authentication and authorization.

    Fields:
    - email: An email field that is unique for each user.
    - username: A character field for storing the username of the user.
    - first_name: A character field for storing the first name of the user.
    - last_name: A character field for storing the last name of the user.
    - is_active: A boolean field indicating whether the user is active or not.
    - is_staff: A boolean field indicating whether the user is a staff member or not.
    - date_joined: A datetime field indicating the date and time when the user joined the system.

    Methods:
    - tokens(): Generates and returns authentication tokens for the user.

    Example Usage:
    user = User.objects.create_user(email='example@example.com', password='password123', username='example')
    user.is_active = False
    user.save()
    """

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def tokens(self):
        """
        Generates and returns authentication tokens for the user.

        Returns:
        A dictionary containing the generated authentication tokens:
        - refresh: The refresh token as a string.
        - access: The access token as a string.
        """
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

class Post(models.Model):
    """
    Represents a model for a post in a system.

    Fields:
    - title (CharField): The title of the post.
    - content (TextField): The content of the post.
    - author (ForeignKey): The author of the post (a User instance).
    - created_at (DateTimeField): The date and time when the post was created.
    - is_active (BooleanField): Indicates whether the post is active or not.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """
        Returns a string representation of the post by returning its title.
        """
        return self.title
    
