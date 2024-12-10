from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import EmailValidator

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import EmailValidator


# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class User(AbstractUser):
    username = None  # Remove the default username field
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Enter a valid university email.")],
    )
    university = models.ForeignKey(
        "project.University",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )
    region = models.ForeignKey(
        "project.Region",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="project_user_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="project_user_permissions",
        blank=True,
    )

    USERNAME_FIELD = "email"  # Use email as the unique identifier for authentication
    REQUIRED_FIELDS = []  # No additional required fields besides email

    objects = CustomUserManager()  # Assign the custom manager

    def __str__(self):
        return self.email

# models.py in the same app
class University(models.Model):
    name = models.CharField(max_length=255, unique=True)
    region = models.ForeignKey("Region", on_delete=models.CASCADE, related_name="universities")
    short_name = models.CharField(max_length=50, default="Unknown")  # Removed unique=True

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="post_images/")

    def __str__(self):
        return f"Image for {self.post.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_comments", blank=True)

    def __str__(self):
        return self.content[:20]

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_replies", blank=True)

    def __str__(self):
        return self.content[:20]

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageRoom(models.Model):
    creator = models.ForeignKey(User, related_name="created_rooms", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_rooms", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room between {self.creator.email} and {self.receiver.email}"


class Message(models.Model):
    room = models.ForeignKey(MessageRoom, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.sender.email} in Room {self.room.id}"