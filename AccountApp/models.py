from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have an email or phone number")
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    bio = models.TextField(max_length=225)
    image = models.ImageField(upload_to='profile/user', blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OTP(models.Model):
    username = models.CharField(max_length=50)
    code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return self.created_at + timedelta(minutes=2) < timezone.now()

    def __str__(self):
        return f"OTP for {self.username}: {self.code}"

    class Meta:
        verbose_name = "One-Time Password"
        verbose_name_plural = "One-Time Passwords"
        ordering = ["-created_at"]