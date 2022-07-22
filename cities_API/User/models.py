from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """User creation manager"""

    def create_user(self, username, email, password):
        """Create base user"""

        if username is None:
            raise TypeError('No username provided.')

        if email is None:
            raise TypeError('No email provided.')

        if password is None:
            raise TypeError('No password provided.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """Create superuser"""

        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(db_index=True, unique=True, max_length=255)
    email = models.EmailField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.email



# Create your models here.
